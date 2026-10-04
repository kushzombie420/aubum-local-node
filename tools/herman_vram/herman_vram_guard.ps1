param(
    [string]$ControllerUrl = "http://127.0.0.1:8090",
    [int]$GpuIndex = 0,
    [switch]$RestorePreviousMode,
    [int]$HoldSeconds = 0
)

$ErrorActionPreference = "Stop"

<#
Public-safe extraction of the verified Herman VRAM lifecycle.

Expected controller contract:
  GET  /status
  POST /mode/vision
  POST /mode/comfy
  POST /mode/hunyuan
  POST /mode/idle

The production controller owns process identity checks, startup/shutdown,
ComfyUI model release, and mode-specific safety. This helper preserves the
verified lifecycle used by the private prototype:

  inspect current mode -> verify it -> enter IDLE -> measure GPU memory
  -> optionally restore the exact previous mode -> verify restoration

No private tokens, machine addresses, model paths, or credentials are stored
in this public version.
#>

function Get-ControllerStatus {
    Invoke-RestMethod -Uri "$ControllerUrl/status" -Method Get -TimeoutSec 15
}

function Set-ControllerMode {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("VISION", "COMFY", "HUNYUAN", "IDLE")]
        [string]$Mode
    )

    $uri = "$ControllerUrl/mode/$($Mode.ToLowerInvariant())"
    Invoke-RestMethod -Uri $uri -Method Post -TimeoutSec 900
}

function Assert-VerifiedStatus {
    param(
        [Parameter(Mandatory = $true)]
        $Status
    )

    $mode = [string]$Status.mode

    if ($mode -notin @("VISION", "COMFY", "HUNYUAN", "IDLE")) {
        throw "Unsafe or unknown worker mode: $mode"
    }

    if ($mode -eq "IDLE") {
        return
    }

    $propertyName = $mode.ToLowerInvariant()
    $property = $Status.PSObject.Properties[$propertyName]

    if (-not $property) {
        throw "Controller status did not include verification data for mode $mode."
    }

    if (-not [bool]$property.Value.verified) {
        throw "$mode mode is not verified."
    }
}

function Get-GpuUsedMiB {
    try {
        $value = & nvidia-smi --id=$GpuIndex --query-gpu=memory.used --format=csv,noheader,nounits 2>$null |
            Select-Object -First 1

        if ($LASTEXITCODE -ne 0 -or -not $value) {
            return $null
        }

        return [int]$value.Trim()
    }
    catch {
        return $null
    }
}

$before = Get-ControllerStatus
Assert-VerifiedStatus -Status $before

$previousMode = [string]$before.mode
$gpuBefore = Get-GpuUsedMiB

Write-Host "Verified starting mode: $previousMode"

if ($null -ne $gpuBefore) {
    Write-Host "GPU memory before IDLE: $gpuBefore MiB"
}

$idle = Set-ControllerMode -Mode "IDLE"

if ([string]$idle.mode -ne "IDLE") {
    throw "Controller did not enter IDLE mode."
}

Start-Sleep -Seconds 2

$gpuIdle = Get-GpuUsedMiB

Write-Host "IDLE verified."

if ($null -ne $gpuIdle) {
    Write-Host "GPU memory in IDLE: $gpuIdle MiB"
}

if ($HoldSeconds -gt 0) {
    Start-Sleep -Seconds $HoldSeconds
}

$restoredMode = "IDLE"
$gpuRestored = $null

if ($RestorePreviousMode -and $previousMode -ne "IDLE") {
    $restored = Set-ControllerMode -Mode $previousMode
    Assert-VerifiedStatus -Status $restored

    if ([string]$restored.mode -ne $previousMode) {
        throw "Mode restore failed. Expected $previousMode, got $($restored.mode)."
    }

    $restoredMode = [string]$restored.mode
    $gpuRestored = Get-GpuUsedMiB

    Write-Host "Previous mode restored and verified: $restoredMode"

    if ($null -ne $gpuRestored) {
        Write-Host "GPU memory after restore: $gpuRestored MiB"
    }
}

[pscustomobject]@{
    controller_url = $ControllerUrl
    previous_mode = $previousMode
    idle_verified = $true
    restored_mode = $restoredMode
    gpu_used_mib_before = $gpuBefore
    gpu_used_mib_idle = $gpuIdle
    gpu_used_mib_restored = $gpuRestored
}

param(
    [string]$ControllerUrl = "http://127.0.0.1:8090",
    [int]$GpuIndex = 0,
    [switch]$RestorePreviousMode,
    [int]$HoldSeconds = 0,
    [switch]$AllowDisruptiveIdle
)

$ErrorActionPreference = "Stop"

<#
Public example of a managed GPU worker VRAM lifecycle.

WARNING - DISRUPTIVE EXAMPLE, NOT A SAFE MANUAL MUSIC/PHOTO SWITCHER.
This script sends POST /mode/idle. Depending on the controller, that route may
force-stop active workers and delete temporary MUSIC API outputs. Listening ports,
controller IDLE state, and an nvidia-smi memory reading do NOT prove that all
jobs finished, callbacks drained, or child GPU processes exited.

By default this helper REFUSES to run. -AllowDisruptiveIdle is an explicit
operator acknowledgement, NOT proof of safety. Do not opt in while requests
are active; preserve desired outputs first, and review the installed controller
for mode-specific shutdown effects. The October 23 supervised MUSIC/PHOTO/VISION
workflow uses explicit mode selection, not this illustrative IDLE helper.

Illustrative controller contract (not all routes are confirmed on every deployed version):
  GET  /status
  POST /mode/vision
  POST /mode/comfy
  POST /mode/idle

The private controller is expected to own process identity checks, startup/shutdown,
ComfyUI model release, and mode-specific safety. This helper preserves the
intended lifecycle based on the private prototype:

  inspect current mode -> verify it -> enter IDLE -> measure GPU memory
  -> optionally restore the exact previous mode -> verify restoration

No private tokens, LAN addresses, model paths, or credentials are stored
in this public version.
#>

# Refuse before even contacting the controller unless the operator opts in.
if (-not $AllowDisruptiveIdle) {
    throw "REFUSED: this example calls /mode/idle and may stop workers or remove temporary outputs. Read the header and explicitly supply -AllowDisruptiveIdle only for a planned quiet-window operation."
}
Write-Warning "DISRUPTIVE EXAMPLE: /mode/idle can stop workers and remove temporary outputs; this script cannot verify all GPU jobs are finished."

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

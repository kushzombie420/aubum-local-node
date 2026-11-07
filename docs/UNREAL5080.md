# Creation Workstation

The creation workstation is a dedicated RTX 5080 system in the private Aubum environment.

## Intended role

The workstation is intended to carry interactive graphics and content-creation workloads that do not belong on MAIN while the primary Big Brain is resident there.

Primary planned responsibilities:

- Unreal Engine development;
- MetaHuman / Lewd MetaHuman-based character and Aubum avatar work in Unreal Engine;
- game-development tooling and interactive 3D iteration;
- gaming;
- selected image-generation and video-generation workloads;
- other GPU-heavy interactive creation tasks.

MAIN remains the primary reasoning/orchestration node and continues to host the main Big Brain.

## Current setup status

Verified as of October 5, 2026:

- fresh Windows setup completed;
- Windows updates completed;
- NVIDIA developer driver installed;
- a dedicated hostname configured for the creation workstation;
- Sunshine host installed on the creation workstation;
- Sunshine stable release `2026.914.233613` is running and its local web UI is reachable;
- Moonlight PC client is installed on MAIN;
- MAIN automatically discovers the creation workstation over the local network;
- Sunshine/Moonlight pairing completed successfully;
- the creation workstation `Desktop` stream opens successfully from MAIN.

## Remote-control topology

```text
MAIN
  |
  | Moonlight client
  v
local network
  |
  v
Sunshine host
  |
  v
creation workstation
```

The remote path is intended to let the creation workstation operate without a permanent dedicated keyboard, mouse, or monitor.

## Headless operation status

Headless operation is verified.

Completed:

1. virtual display installed and configured;
2. Sunshine capture verified against the virtual display;
3. live physical-display unplug test passed while the Moonlight stream remained active;
4. cold boot completed with no physical monitor, keyboard, or mouse attached;
5. MAIN successfully reconnected to the creation workstation desktop through Moonlight after that headless boot.

Optional follow-up:

- enable Wake-on-LAN for remote power-on.

## November 7, 2026: Fleet monitoring checkpoint

The private Watchtower v0.6.6 captured **LIVE NVIDIA RTX 5080 GPU telemetry** on this workstation. Its existing Windows GPU read-only publisher task retained its **boot trigger and duplicate-instance protection**, and a backed-up **one-minute repeated retry trigger** was verified as installed. The telemetry endpoint was LIVE when checked; it had been running since before the new retry configuration was added.

**PENDING / NOT VERIFIED:** a new cold-start/reboot check, restart of the publisher after a future unexpected termination, and fleet-wide unattended recovery. The newer scheduled retry is not itself proof that the publisher will survive every failure. The existing Sunshine/Moonlight remote access and previously verified headless-boot path were preserved.

The current Unreal character-creation decision uses **MetaHuman / Lewd MetaHuman**, rather than starting a new Blender-based character pipeline. Earlier private Blender automation experiments remain historical; they are not the prescribed path for this workstation's Unreal characters.

## Security / repository hygiene

Do not store the following in this repository:

- Sunshine credentials;
- pairing PINs;
- passwords or tokens;
- private LAN addresses unless a future example explicitly requires placeholders.

Machine-specific secrets remain outside the public repository.

## Design reason

The workstation exists to separate interactive graphics workloads from primary-model inference.

Rather than replacing MAIN's RTX 4090, the creation workstation provides a specialized RTX 5080 node so Unreal Engine development, MetaHuman-based character work, gaming, and interactive creation do not have to compete directly with the Big Brain for MAIN's GPU resources.

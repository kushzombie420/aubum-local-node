# Unreal5080 Workstation

`Unreal5080` is a dedicated RTX 5080 creation workstation in the private Aubum environment.

## Intended role

The workstation is intended to carry interactive graphics and content-creation workloads that do not belong on MAIN while the primary Big Brain is resident there.

Primary planned responsibilities:

- Unreal Engine development;
- MetaHuman and Aubum avatar work;
- Blender and other 3D authoring;
- gaming;
- selected image-generation and video-generation workloads;
- other GPU-heavy interactive creation tasks.

MAIN remains the primary reasoning/orchestration node and continues to host the main Big Brain.

## Current setup status

Verified as of October 5, 2026:

- fresh Windows setup completed;
- Windows updates completed;
- NVIDIA developer driver installed;
- hostname set to `Unreal5080`;
- Sunshine host installed on Unreal5080;
- Sunshine stable release `2026.914.233613` is running and its local web UI is reachable;
- Moonlight PC client is installed on MAIN;
- MAIN automatically discovers Unreal5080 over the local network;
- Sunshine/Moonlight pairing completed successfully;
- the Unreal5080 `Desktop` stream opens successfully from MAIN.

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
Unreal5080
```

The remote path is intended to let Unreal5080 operate without a permanent dedicated keyboard, mouse, or monitor.

## Pending headless work

The current remote-desktop path is verified while a physical display is still attached.

Remaining work:

1. install/configure a virtual display on Unreal5080;
2. verify Sunshine capture against that virtual display;
3. boot Unreal5080 with no physical monitor, keyboard, or mouse attached;
4. confirm Moonlight can still open the desktop from MAIN;
5. optionally enable Wake-on-LAN for remote startup.

## Security / repository hygiene

Do not store the following in this repository:

- Sunshine credentials;
- pairing PINs;
- passwords or tokens;
- private LAN addresses unless a future example explicitly requires placeholders.

Machine-specific secrets remain outside the public repository.

## Design reason

The workstation exists to separate interactive graphics workloads from primary-model inference.

Rather than replacing MAIN's RTX 4090, Unreal5080 provides a second specialized compute/creation node so Unreal, Blender, avatar work, and related tasks do not need to compete directly with the Big Brain for the same GPU and system resources.

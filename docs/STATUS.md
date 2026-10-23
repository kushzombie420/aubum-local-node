# Aubum Local Node — Current Status

This document separates what is already working in the private Aubum prototype from what is currently being moved into the public Aubum Local Node project.

## October 23, 2026: Live recovery checkpoint

A supervised recovery of the private shared-GPU media worker restored practical **manual** workload selection from MAIN. The operator selects a mode through local command shortcuts; the existing GPU-worker controller starts and verifies the selected worker. This does not imply that jobs automatically switch modes or that every transition has been tested.

| Capability | User-observed October 23 result | Scope |
| --- | --- | --- |
| MUSIC (standard ACE-Step 1.5) | **LIVE PASS** | Generated audio locally on the GPU worker and later a song through Open WebUI using the legacy backend. |
| PHOTO (Qwen Image 2.1) | **LIVE PASS** | Two successful image generations returned to Open WebUI and saved. |
| VISION | **LIVE PASS** | The image-inspection tool executed on the VISION worker and returned visually grounded details. |
| MAIN-driven selection | **LIVE PASS, partial matrix** | MUSIC → PHOTO → MUSIC and MUSIC → VISION verified through remote controls; a complete three-mode transition matrix was not separately established. |
| Protected XL Turbo manual startup | **NOT ACTIVE / DEFERRED** | Earlier XL Turbo generation tests remain valid historical results, but the protected manual startup and automatic-handoff activation were not completed. |
| Public installation of private orchestration | **NOT RELEASED** | This repository documents the prototype; the reusable manual client still requires sanitization and generalization. |

**Operational boundary:** The current controller may force-stop outgoing workers and remove temporary MUSIC API output folders. Operators must finish requests and preserve desired outputs before selecting another mode. The controls cannot independently prove every background request has completed. An XL Turbo ownership conflict during recovery was isolated; guarded local job-lock archiving plus selecting the existing legacy music backend restored Open WebUI MUSIC generation. No ownership database was rewritten.

See [Shared-GPU Recovery — October 23](RECOVERY_2026-10-23.md) for the dated sequence and verification limitations. SMALL/MEDIUM/BIG request routing and the other Aubum nodes are separate from this manual shared-GPU selection decision.

## Working in the private prototype

The private Aubum environment has already been used for:

- multi-computer job execution;
- centralized worker control;
- remote Blender job execution;
- GPU workload switching;
- worker-state restoration after jobs;
- dedicated vision-model workflows;
- image-generation workflows;
- video-generation workflows;
- 3D-generation workflows;
- automated Blender testing;
- result and artifact generation;
- dedicated voice and audio workloads;
- lightweight model-based routing;
- production three-tier SMALL / MEDIUM / BIG routing;
- dedicated CUDA-accelerated Medium Brain inference;
- on-demand Big-Brain wake/sleep and idle GPU release;
- CUDA-accelerated primary-model inference on the RTX 4090;
- local PDF/document text extraction and reading;
- live web research with source citations;
- local chat control for Big-Brain status and sleep;
- phone-based remote control;
- secure remote Open WebUI/Aubum access over cellular through a private Tailscale connection;
- live and recorded video input;
- persistent phone-camera preview with automatic start/stop;
- direct desktop monitor capture;
- condition-aware visual task supervision;
- saved visual evidence and follow-up reinspection;
- guarded local tool execution;
- independent health monitoring;
- persistent cross-machine memory;
- cross-session memory retrieval;
- local-network communication between AI and worker systems.

## Current verified deployment

As of October 2026, the private Aubum environment is operating across eight heterogeneous devices:

- **MAIN PC** — primary Qwen3.8 27B-class Q4_K_P Big Brain through CUDA llama.cpp, orchestration, reasoning, Open WebUI, system control, and health aggregation
- **GPU worker** — RTX 4090 managed worker handling vision, Blender, 3D generation, image/video workflows, rendering, local music generation, and other heavy GPU execution
- **Creation workstation** — dedicated RTX 5080 system for Unreal Engine, Blender, avatar/game-development work, gaming, and selected image/video workloads; Sunshine/Moonlight remote desktop and cold-boot headless operation from MAIN are verified
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight local routing node using Vulkan-accelerated inference
- **Medium Brain worker** — GTX 1080 Ti node running a Qwen3.5 9B-class Q6_K model through CUDA with 16K context
- **Guarddog + Memory laptop** — independent system monitoring and persistent external Memory
- **Android phone** — remote control, edge tasks, recorded-video input, and live camera/sensor input

This deployment demonstrates specialized roles operating across Windows PCs, AMD handheld hardware, a laptop infrastructure node, and a mobile device rather than relying on identical desktop workers.

These capabilities are currently part of a private development environment and are not yet represented as a clean public implementation.

## Recovery baseline — October 9, 2026

A broad private-prototype regression repair produced a new observed baseline for shared orchestration and media/sensor routing.

User-observed end-to-end checks through the normal Open WebUI path verified:

- ordinary conversational acknowledgements can complete with zero action-tool calls;
- music, image generation, and image editing route to their intended specialist tools;
- text-to-video and image-to-video routing produce real video artifacts;
- explicit live-camera requests automatically activate the connected phone-camera path;
- current visual claims require current-turn observation evidence;
- stale, blank, uniform, unchanged, unavailable, and connection-placeholder camera feeds fail closed instead of producing invented scene descriptions;
- bounded camera sessions stop afterward when Aubum started the feed;
- SMALL / MEDIUM / BIG routing and Big-Brain power control remained intact during the recovery.

The recovery also reinforced a project-wide verification rule: automated tests and agent reports are supporting evidence, but known-good promotion requires observed behavior through the real user path.

A sanitized summary is documented in [Recovery Baseline — 2026-10-09](RECOVERY_BASELINE_2026-10-09.md).

## Recently verified private milestones

### Qwen3.8 Big Brain production promotion

On October 16, 2026, the primary Big Brain was promoted from the prior Qwen3.6 27B-class Q4_K_P baseline to a Qwen3.8 27B-class Q4_K_P GGUF.

Verified behavior:

- Qwen3.8 runs through CUDA-enabled llama.cpp build **b11669** on MAIN's RTX 4090;
- the production context remains **32K** with one inference slot and reasoning disabled for normal responses;
- direct generation measured approximately **42.4 tok/s**, effectively matching the previous approximately **42.57 tok/s** Qwen3.6 CUDA baseline;
- end-to-end **Open WebUI -> Sentinel -> Gatekeeper -> Qwen3.8** wake and response succeeded;
- the prior Qwen3.6 configuration was preserved as a rollback baseline;
- the chat `sleep` path now waits for Gatekeeper confirmation before reporting that the Big Brain is asleep;
- a traced Open WebUI follow-up-prediction request that previously re-woke the Big Brain after sleep is now recognized as housekeeping and routed to SMALL.

This promotion demonstrated that the Big Brain can be replaced behind the existing Gatekeeper/Sentinel interfaces without redesigning the surrounding routing architecture.

### CUDA inference acceleration and PDF reading

The primary 27B Big Brain has been moved to a CUDA-enabled llama.cpp build on MAIN's RTX 4090.

Verified benchmark results on the same model and hardware:

- Vulkan generation: approximately **5.71 tok/s**;
- CUDA generation: approximately **42.57 tok/s**;
- generation throughput improvement: approximately **7.5x**;
- prompt processing increased from approximately **919.5 tok/s** to **2775.6 tok/s**, approximately **3x**;
- production operation remained stable with the existing 32K context configuration.

Aubum has also verified local PDF/document reading through text extraction. PDF content can now be extracted and supplied to the reasoning layer for analysis without requiring the user to manually copy the document text.

### On-demand reasoning and GPU power management

The private system now has a production routing layer that keeps the primary 27B reasoning model unloaded until a request actually needs it.

Verified behavior:

- Open WebUI connects through a production Sentinel rather than directly to the Big Brain;
- simple requests are handled by the Steam Deck's Qwen3-1.7B router;
- intermediate conversational/contextual requests can route to a dedicated Qwen3.5 9B-class Medium Brain on the GTX 1080 Ti worker;
- hard or explicitly complex requests are routed to a production Gatekeeper that wakes the 27B model on demand;
- duplicate wake/process protection prevents multiple copies of the Big Brain from launching;
- active-request protection prevents sleep while work is still being served;
- the Big Brain automatically unloads after 900 seconds of inactivity;
- Open WebUI model polling and housekeeping requests such as title generation, tag generation, legacy follow-up suggestions, and the current `Predict 3-5 useful messages...` follow-up-prediction prompt are kept on the SMALL path so they do not wake the 27B;
- health checks report Sentinel, Gatekeeper, Big Brain state, active requests, and idle timeout without waking the Big Brain;
- an end-to-end Open WebUI arithmetic test was answered by the Steam Deck while the primary RTX 4090 remained free;
- the Medium Brain was verified at approximately **34.3 tok/s** with Q6_K and 16K context;
- a multi-turn conversation test was verified to take the MEDIUM route and preserve context;
- a complex Unreal Engine debugging request was verified to take the BIG route;
- the canonical production Sentinel passed SMALL, MEDIUM, and BIG routing tests on the production endpoint.

The current production health check reports the routing/power stack alongside the existing distributed services. Health Check v0.6 verifies the secure remote-mobile layer plus the dedicated Medium Brain through TCP reachability and its model/API endpoint. Private project records report **30 passing checks, 0 warnings, and 0 failures**; the raw run log is not included in this public repository.

The checker remains read-only and now treats an intentionally sleeping Big Brain as healthy when Gatekeeper confirms the expected asleep state. The desktop health-check shortcut has been promoted to v0.6.

### Web research and conversational resource control

The private prototype now supports live web research from Open WebUI while preserving the on-demand Big Brain architecture.

Verified behavior:

- a fresh web-search request can wake the 27B model and use current web results;
- answers can include source citations;
- the local `status` command is handled without Big Brain inference and reports Big Brain state, active requests, and idle timing;
- the local `sleep` command is handled by Sentinel and delegated to a Gatekeeper control endpoint;
- Gatekeeper retains ownership of the shutdown path, including active-request and wake-state safety checks;
- chat-controlled sleep has been verified to unload the primary 27B model from RTX 4090 VRAM, and Sentinel now reports sleep success only after Gatekeeper confirms the asleep state.

The current implementation intentionally avoids adding a separate hard-coded web-search routing rule until real behavior demonstrates one is necessary.

### Secure remote mobile access

The Android phone can now reach the private Aubum/Open WebUI interface from outside the home network.

Verified behavior:

- MAIN and the phone are connected through Tailscale;
- Open WebUI remains bound to localhost on MAIN;
- Tailscale Serve provides a private HTTPS endpoint restricted to the tailnet;
- the phone successfully connected to Open WebUI over cellular with Wi-Fi disabled;
- no public Open WebUI port was opened;
- the pre-existing local access path remains available;
- manual Taildrop transfer from MAIN to the phone was verified.

Generated images remain previewable and manually downloadable through Open WebUI on mobile. Automatic permanent image-transfer/retention behavior is intentionally deferred rather than adding more background plumbing before it is needed.

### Managed music generation, XL Turbo, and worker auto-bootstrap

The private GPU worker previously demonstrated ACE-Step 1.5 XL Turbo generation through a managed transport, with the standard ACE-Step 1.5 path preserved. Following the October 23 recovery, **manual MUSIC operation uses the standard legacy backend; protected XL Turbo activation remains uncompleted.**

Earlier XL Turbo verification included:

- the existing Aubum music tool being used from normal Open WebUI chat; no duplicate tool was introduced;
- XL Turbo requests use an authenticated managed transport, serialized job ownership, and artifact integrity checks;
- the reviewed XL tool/transport implementation accepting whole-second durations from **10 to 600 seconds**;
- real **120-second** and **600-second** WAVs were generated and delivered through ordinary chat;
- the ten-minute WAV was independently checked for an exact 600-second duration, valid WAV structure, matching artifact hash, and non-silent audio throughout the file;
- a user-supplied-lyrics request passed lyrics into the generation tool and returned audio; a separate concept-only song request also returned audio;
- the original ACE-Step 1.5 queue path and rollback evidence remain preserved.

The live duration tests demonstrate 120 seconds and 600 seconds; every intermediate duration has not been live-tested. Vocal/style adherence and comparative audio quality remain qualitative evaluation work, not a completed benchmark. The private XL integration is not yet packaged as a public installable component.

During those historical managed XL tests, the XL worker remained resident. Serialized managed chat requests are covered; concurrent generation through independent local interfaces is outside the tested guarantee. No global inference-idle claim or automatic GPU shutdown is made.

A previous post-reboot test verified that the controller and normal VISION-ready state returned without manually launching the desktop bootstrap. That earlier result should not be mistaken for a fresh post-reboot acceptance test of the October 23 manual controls.

### Guarddog and independent monitoring

A dedicated laptop now runs an observation-only Guarddog service that independently checks major Aubum components.

The private system has verified:

- Guarddog startup and scheduled operation;
- monitoring of MAIN;
- monitoring of the GPU worker;
- monitoring of the Voice worker;
- monitoring of the Steam Deck router;
- monitoring of persistent Memory;
- a separate status endpoint that MAIN can use to verify Guarddog itself;
- health-check integration that can detect Guarddog or Memory failure without exposing the private Memory backend.

Automated recovery is not yet enabled. Recovery actions will be introduced only after sufficient observation data exists to distinguish real failures from temporary or expected state changes.

### Persistent Memory

A dedicated Memory service now runs on the laptop as persistent local infrastructure.

The private system has verified:

- a local-only Memory backend;
- append-only persistent storage;
- a restricted bridge for approved cross-machine access;
- Big Brain memory health checks;
- explicit memory creation;
- retrieval by stored ID;
- memory search;
- cross-machine writes from MAIN;
- cross-session retrieval in a fresh Big Brain conversation.

This means the Big Brain can deliberately store durable information in one session and retrieve it later from persistent external Memory rather than depending only on current conversation context.

Automatic relevance-based recall and selective automatic memory writing remain future work.

### Visual supervision and continuity

The private prototype now supports direct visual supervision of both real-world and desktop sources.

Verified behavior includes:

- a persistent phone preview service for the Android phone camera;
- bounded Watch Live sessions that automatically start and stop the phone camera;
- direct capture of Windows displays without routing through the phone camera;
- short bounded screen views for quick inspection;
- condition-aware monitoring that can stop when a requested visual change is detected;
- saved per-cycle frames and contact sheets;
- follow-up reinspection of saved supervisor evidence by the vision worker;
- routing rules that separate display/monitor/screen/window requests from camera/phone/mobile/webcam requests;
- screen-within-screen grounding rules to reduce unsupported identity and scene claims.
- a live desktop test in which the supervisor successfully observed text while it was actively being typed into a window, verifying in-progress screen-change detection; the capture timing window is still sensitive and is not yet treated as a reliability guarantee.

A verified continuity test demonstrated the sequence:

**observe display → detect change → save evidence → re-inspect evidence → answer a follow-up question about the prior visual state**

Memory writes and corrective actions remain disabled in the visual supervisor while the observation and evidence pipeline is being hardened.

### Health checking

The private Aubum health-check system currently verifies the main distributed services, including the Guarddog/Memory laptop, routing/power state, secure remote-mobile access, and the dedicated Medium Brain.

Health Check v0.6 verifies:

- the Tailscale Windows service and client;
- active tailnet connection;
- Tailscale Serve remaining tailnet-only;
- the Serve proxy still targeting localhost Open WebUI;
- Open WebUI remaining bound to localhost;
- a successful local Open WebUI HTTP response;
- Medium Brain TCP reachability;
- the Medium Brain model/API endpoint;
- expected Big Brain sleep state through Gatekeeper, so intentional idle unload is treated as healthy.

Phone-online state is intentionally not required, so a powered-off or disconnected phone does not make the infrastructure unhealthy.

A historical private full-system run was reported with (raw execution log not published here):

- 30 passing checks;
- 0 warnings;
- 0 failures.

The health checker remains read-only.

## Near-term private prototype roadmap

The current near-term infrastructure backlog is:

1. **Storage cleanup and reorganization** before attempting Linux sideloading, so large AI/model/game-development files are intentionally placed instead of being dragged through another operating-system experiment.
2. **Linux sideloading experiment** after storage is cleaned and free-space/partition requirements are understood.
3. **GPU worker VRAM cleanup** using the same on-demand load / protected active-job / idle-unload pattern proven on MAIN, without disturbing the GPU worker's known-good worker modes.
4. **RTX 3070 voice pipeline** for STT, Aubum response, TTS, and optional voice conversion on the dedicated voice machine.
5. **Generated-image retention cleanup**: keep Open WebUI preview/manual download behavior, then add bounded automatic cleanup of old generated files instead of automatic phone transfer.
6. **Portable phone bridge** for temporarily attaching a bounded Aubum worker/helper through the phone when using another PC.
7. **Music/audio expansion** beyond the now-verified song-generation baseline, including sound effects, ambient loops, and game-audio asset workflows.
8. **Public presentation/promotion pass** with a cleaner architecture diagram, screenshots, and a short reproducible demo of SMALL routing, BIG wake/sleep, web research, and remote mobile access.
9. **Smarter Memory** with relevance-based recall and selective automatic writes after the current explicit persistent-memory baseline remains stable.

Unreal/character/game-development work remains a separate roadmap so infrastructure tasks do not quietly swallow the game-development checklist.

## Public repository status

The public Aubum Local Node repository is currently in the architecture and extraction stage.

Completed:

- project scope defined;
- open-source license added;
- public project README created;
- high-level architecture documented;
- public/private project boundary defined;
- current private heterogeneous deployment documented;
- independent monitoring concept documented;
- persistent-memory architecture documented;
- public capability and model matrix added;
- dated October 23 shared-GPU recovery case study added.

In progress:

- worker/controller protocol specification;
- reusable worker architecture;
- capability and resource reporting;
- job lifecycle definition;
- failure and recovery behavior;
- bounded execution model;
- persistent-state and memory interfaces;
- a sanitized, configurable public example of the privately verified three-mode selector, with mockable tests (not yet released).

## Planned public alpha

The first usable public alpha is intended to include:

- worker discovery;
- health monitoring;
- capability reporting;
- job dispatch;
- GPU/resource management;
- state restoration;
- failure detection and bounded recovery;
- logging;
- bounded worker permissions;
- reproducible installation;
- basic persistent-state interfaces;
- basic multi-machine examples.

## Not yet claimed as complete

The following are goals, not finished public features:

- one-click installation;
- automatic discovery across arbitrary networks;
- broad hardware compatibility;
- automatic relevance-based memory retrieval;
- selective automatic memory writing;
- unattended long-running workflows;
- autonomous recovery across all services;
- cloud/local hybrid routing;
- production-grade security hardening;
- unattended, automatically coordinated shared-GPU handoff across MUSIC, PHOTO, and VISION.

## Development principle

The public repository will distinguish clearly between:

1. features already demonstrated privately;
2. features implemented publicly;
3. experimental work;
4. future plans.

Known-good working components should not be replaced merely for architectural cleanliness. New capabilities should be developed beside verified baselines, tested independently, and promoted only after they demonstrate equivalent or better reliability.

This is intended to keep the project technically honest and make progress easy to verify.

# Aubum Local Node — Current Status

This document separates what is already working in the private Aubum prototype from what is currently being moved into the public Aubum Local Node project.

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

As of October 2026, the private Aubum environment is operating across seven heterogeneous devices:

- **MAIN PC** — primary Big Brain, orchestration, reasoning, Open WebUI, system control, and health aggregation
- **Herman** — RTX 4090 worker handling vision, Blender, 3D generation, image/video workflows, rendering, and other heavy GPU execution
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight local routing node using Vulkan-accelerated inference
- **Medium Brain worker** — GTX 1080 Ti node running a Qwen3.5 9B-class Q6_K model through CUDA with 16K context
- **Guarddog + Memory laptop** — independent system monitoring and persistent external Memory
- **Android phone** — remote control, edge tasks, recorded-video input, and live camera/sensor input

This deployment demonstrates specialized roles operating across Windows PCs, AMD handheld hardware, a laptop infrastructure node, and a mobile device rather than relying on identical desktop workers.

These capabilities are currently part of a private development environment and are not yet represented as a clean public implementation.

## Recently verified private milestones

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
- Open WebUI model polling and housekeeping requests such as title generation, follow-up suggestions, and tag generation are kept on the SMALL path so they do not wake the 27B;
- health checks report Sentinel, Gatekeeper, Big Brain state, active requests, and idle timeout without waking the Big Brain;
- an end-to-end Open WebUI arithmetic test was answered by the Steam Deck while the primary RTX 4090 remained free;
- the Medium Brain was verified at approximately **34.3 tok/s** with Q6_K and 16K context;
- a multi-turn conversation test was verified to take the MEDIUM route and preserve context;
- a complex Unreal Engine debugging request was verified to take the BIG route;
- the canonical production Sentinel passed SMALL, MEDIUM, and BIG routing tests on the production endpoint.

The current production health check reports the routing/power stack alongside the existing distributed services. Health Check v0.5 now also verifies the secure remote-mobile layer. A verified run completed with 27 passing checks, 0 warnings, and 0 failures.

The dedicated Medium Brain node was added after that v0.5 baseline and is not yet covered by the health-check shortcut. Adding Medium Brain reachability and inference-endpoint checks is the next health-check revision.

### Web research and conversational resource control

The private prototype now supports live web research from Open WebUI while preserving the on-demand Big Brain architecture.

Verified behavior:

- a fresh web-search request can wake the 27B model and use current web results;
- answers can include source citations;
- the local `status` command is handled without Big Brain inference and reports Big Brain state, active requests, and idle timing;
- the local `sleep` command is handled by Sentinel and delegated to a Gatekeeper control endpoint;
- Gatekeeper retains ownership of the shutdown path, including active-request and wake-state safety checks;
- chat-controlled sleep has been verified to unload the primary 27B model from RTX 4090 VRAM.

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

The private Aubum health-check system currently verifies the main distributed services, including the Guarddog/Memory laptop, routing/power state, and secure remote-mobile access.

Health Check v0.5 adds checks for:

- the Tailscale Windows service and client;
- active tailnet connection;
- Tailscale Serve remaining tailnet-only;
- the Serve proxy still targeting localhost Open WebUI;
- Open WebUI remaining bound to localhost;
- a successful local Open WebUI HTTP response.

Phone-online state is intentionally not required, so a powered-off or disconnected phone does not make the infrastructure unhealthy.

A verified full-system run completed with:

- 27 passing checks;
- 0 warnings;
- 0 failures.

The health checker remains read-only.

## Near-term private prototype roadmap

The current near-term infrastructure backlog is:

1. **Storage cleanup and reorganization** before attempting Linux sideloading, so large AI/model/game-development files are intentionally placed instead of being dragged through another operating-system experiment.
2. **Linux sideloading experiment** after storage is cleaned and free-space/partition requirements are understood.
3. **Herman VRAM cleanup** using the same on-demand load / protected active-job / idle-unload pattern proven on MAIN, without disturbing Herman's known-good worker modes.
4. **RTX 3070 voice pipeline** for STT, Aubum response, TTS, and optional voice conversion on the dedicated voice machine.
5. **Generated-image retention cleanup**: keep Open WebUI preview/manual download behavior, then add bounded automatic cleanup of old generated files instead of automatic phone transfer.
6. **Portable phone bridge** for temporarily attaching a bounded Aubum worker/helper through the phone when using another PC.
7. **Music/audio generation** as a later specialist capability.
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
- public capability and model matrix added.

In progress:

- worker/controller protocol specification;
- reusable worker architecture;
- capability and resource reporting;
- job lifecycle definition;
- failure and recovery behavior;
- bounded execution model;
- persistent-state and memory interfaces.

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
- production-grade security hardening.

## Development principle

The public repository will distinguish clearly between:

1. features already demonstrated privately;
2. features implemented publicly;
3. experimental work;
4. future plans.

Known-good working components should not be replaced merely for architectural cleanliness. New capabilities should be developed beside verified baselines, tested independently, and promoted only after they demonstrate equivalent or better reliability.

This is intended to keep the project technically honest and make progress easy to verify.

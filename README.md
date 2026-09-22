# Aubum Local Node

Aubum Local Node is an open-source project exploring how ordinary consumer PCs, GPUs, handheld hardware, laptops, and mobile devices can be combined into a coordinated, locally owned AI compute system.

The project grew out of Aubum, a working private AI orchestration prototype that I am developing independently.

## Project Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Current Status](docs/STATUS.md)
- [Worker Protocol Draft](docs/WORKER_PROTOCOL.md)

## Goal

Make it possible for an individual to combine multiple home computers into one practical AI system without requiring enterprise infrastructure or depending entirely on cloud services.

The long-term workflow is:

**Reason → retrieve useful state → dispatch work → execute on the appropriate machine → inspect the result → recover or continue → restore worker state**

## Current Prototype

The private Aubum prototype already includes working experiments with:

- multi-computer job execution;
- centralized worker control;
- GPU workload mode switching;
- previous-state restoration after jobs;
- remote Blender execution;
- automated Blender testing;
- vision-model integration;
- image and video generation workflows;
- 3D-generation tooling;
- dedicated voice workloads;
- lightweight model-based routing;
- phone-based control and visual input;
- live phone-camera preview with automatic start/stop;
- direct desktop monitor observation;
- condition-aware visual task supervision;
- saved visual evidence and follow-up reinspection;
- independent health monitoring;
- persistent cross-machine memory;
- guarded system automation;
- local-network orchestration.

## Verified Deployment Topology — September 2026

The private Aubum system is currently operating across a heterogeneous six-device environment:

- **MAIN PC** — Big Brain, primary orchestration, reasoning, Open WebUI, system control, and health aggregation
- **Herman** — RTX 4090 worker for vision, Blender, 3D generation, image/video workflows, rendering, and heavy GPU execution
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight Aubum router running a small local model with Vulkan acceleration
- **Guarddog + Memory laptop** — independent monitoring plus persistent external Memory
- **Android phone** — remote control, edge tasks, recorded-video input, and live camera/sensor input

The current system has demonstrated specialized roles across Windows PCs, AMD handheld hardware, a laptop infrastructure node, and a mobile device rather than relying on identical desktop workers.

This deployment remains part of the private Aubum development environment. The public Aubum Local Node project is extracting the reusable infrastructure into a standalone open-source implementation.

## Recent Verified Milestones

### Independent Guarddog monitoring

A dedicated laptop now runs an observation-only Guarddog service that independently monitors major Aubum components.

MAIN can also verify Guarddog itself, avoiding a design where the monitoring layer could silently fail without detection.

The current private health-check system includes the Guarddog/Memory node and has completed a full-system run with:

- **27 passing checks**
- **0 warnings**
- **0 failures**

The health checker is read-only.

### Visual observation and supervision

The private prototype now supports two complementary visual paths:

- **Phone / camera vision** for live real-world input from the Android phone, including a persistent preview service and bounded Watch Live sessions with automatic camera start/stop.
- **Desktop vision** for direct observation of Windows displays without pointing the phone at a monitor.

Recent verified behavior includes:

- short bounded desktop views;
- condition-aware monitoring that can report when a requested visual change occurs;
- saved before/after frames and contact sheets;
- follow-up reinspection of saved visual evidence without requiring the user to upload another screenshot;
- explicit routing between screen/display requests and phone/camera requests;
- conservative handling of screen-within-screen scenes to reduce unsupported visual narratives.

This allows Aubum to observe a display, detect a change, retain the relevant visual evidence, and answer later questions about what it saw.

### Persistent cross-machine Memory

The same laptop hosts Aubum's persistent external Memory service.

The private prototype has verified:

- a local-only Memory backend;
- append-only persistent storage;
- a restricted cross-machine bridge;
- explicit memory creation;
- memory search and retrieval;
- Big Brain access through an Open WebUI tool;
- cross-session retrieval from a fresh Big Brain conversation.

This allows the Big Brain to deliberately store durable information in one session and retrieve it later without depending only on current conversation context.

Automatic relevance-based recall and selective automatic memory writing remain future work.

## Aubum Local Node

This repository focuses specifically on the reusable local-compute infrastructure.

Planned components include:

- worker discovery and health monitoring;
- secure local-network communication;
- job dispatch and routing;
- GPU/resource-state management;
- automatic worker-state restoration;
- failure detection and bounded recovery;
- persistent-state and memory interfaces;
- logging and auditability;
- restricted/bounded worker permissions;
- reproducible installation;
- support for heterogeneous consumer hardware;
- documentation for non-expert deployment.

## Research Questions

The project is intended to investigate questions including:

- Can heterogeneous consumer devices operate reliably as one local AI system?
- How much manual administration can be removed from multi-machine AI workflows?
- Can workers recover from failures without losing system state?
- Can reasoning and GPU-heavy execution run simultaneously on separate machines?
- Can persistent local Memory improve continuity without depending on a cloud service?
- What safety controls are necessary before allowing longer autonomous workflows?

## Design Principles

### Local-first

The system should remain useful without requiring a permanent cloud dependency.

### User-owned

The person operating the system should control the hardware, models, data, and permissions.

### Heterogeneous

Users should be able to reuse different generations and types of consumer hardware rather than purchasing identical enterprise nodes.

### Specialized

Different devices should perform roles suited to their hardware instead of duplicating every workload on every machine.

### Bounded autonomy

Increasing automation should not require giving an AI unrestricted access to every machine.

### Recoverable

Jobs should fail safely, produce useful diagnostics, and restore workers to a known state whenever possible.

### Preserve known-good systems

New capabilities should be developed beside verified working baselines and promoted only after they demonstrate equivalent or better reliability.

## Current Status

**Early development / working prototype**

The underlying private Aubum system is already being used for distributed AI, Blender, vision, voice, routing, monitoring, and persistent-memory workflows.

The public repository is currently in the architecture and extraction stage. It is intended to develop the reusable local-compute portion as a standalone open-source project.

Code, architecture documentation, benchmarks, installation tooling, and demonstrations will be added as components are separated from the private Aubum environment.

## Development Roadmap

1. Define the public worker/controller architecture.
2. Separate private Aubum-specific logic from reusable infrastructure.
3. Publish an initial worker protocol.
4. Build reproducible worker installation.
5. Add hardware/resource discovery.
6. Add job routing and state management.
7. Add persistent-state and memory interfaces.
8. Add failure detection, bounded recovery, and auditing.
9. Test across multiple consumer hardware configurations.
10. Simplify deployment for non-expert users.
11. Publish examples and demonstrations.
12. Release a documented v1.0.

## About

Aubum Local Node is being developed by an independent developer and AI enthusiast exploring how far locally owned AI systems can be pushed using consumer hardware.

The project is currently self-funded and under active development.

## License

The public Aubum Local Node project is intended to be released under an open-source license.

Pre-existing private Aubum components are not automatically part of this repository or license.

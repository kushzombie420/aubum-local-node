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
- phone-based remote control;
- live and recorded video input;
- guarded local tool execution;
- independent health monitoring;
- persistent cross-machine memory;
- cross-session memory retrieval;
- local-network communication between AI and worker systems.

## Current verified deployment

As of September 2026, the private Aubum environment is operating across six heterogeneous devices:

- **MAIN PC** — primary Big Brain, orchestration, reasoning, Open WebUI, system control, and health aggregation
- **Herman** — RTX 4090 worker handling vision, Blender, 3D generation, image/video workflows, rendering, and other heavy GPU execution
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight local routing node using Vulkan-accelerated inference
- **Guarddog + Memory laptop** — independent system monitoring and persistent external Memory
- **Android phone** — remote control, edge tasks, recorded-video input, and live camera/sensor input

This deployment demonstrates specialized roles operating across Windows PCs, AMD handheld hardware, a laptop infrastructure node, and a mobile device rather than relying on identical desktop workers.

These capabilities are currently part of a private development environment and are not yet represented as a clean public implementation.

## Recently verified private milestones

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

### Health checking

The private Aubum health-check system currently verifies the main distributed services, including the Guarddog/Memory laptop.

A recent full-system run completed with:

- 27 passing checks;
- 0 warnings;
- 0 failures.

The health checker remains read-only.

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
- persistent-memory architecture documented.

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
- autonomous visual evaluation;
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

# Aubum Local Node — Current Status

This document separates what is already working in the private Aubum prototype from what is currently being moved into the public Aubum Local Node project.

## Working in the private prototype

The private Aubum environment has already been used for:

- multi-computer job execution;
- remote Blender job execution;
- GPU workload switching;
- worker-state restoration after jobs;
- dedicated vision-model workflows;
- image-generation workflows;
- video-generation workflows;
- automated Blender testing;
- result and artifact generation;
- guarded local tool execution;
- local-network communication between AI and worker systems.

 ### Current verified deployment

As of September 2026, the private Aubum environment is operating across five heterogeneous devices:

- **MAIN PC** — primary Big Brain, orchestration, reasoning, and system control
- **Herman** — RTX 4090 worker handling Blender, 3D generation, image/video workflows, and heavy GPU execution
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight local routing node using Vulkan-accelerated inference
- **Android phone** — remote control interface for MAIN and Aubum services

This deployment demonstrates specialized roles operating across Windows PCs, AMD handheld hardware, and a mobile control device rather than relying on identical desktop workers.

These capabilities are currently part of a private development environment and are not yet represented as a clean public implementation.

## Public repository status

The public Aubum Local Node repository is currently in the architecture and extraction stage.

Completed:

- project scope defined;
- open-source license added;
- public project README created;
- high-level architecture documented;
- public/private project boundary defined.

In progress:

- worker/controller protocol specification;
- reusable worker architecture;
- capability and resource reporting;
- job lifecycle definition;
- failure and recovery behavior;
- bounded execution model.

## Planned public alpha

The first usable public alpha is intended to include:

- worker discovery;
- health monitoring;
- capability reporting;
- job dispatch;
- GPU/resource management;
- state restoration;
- failure detection and recovery;
- logging;
- bounded worker permissions;
- reproducible installation;
- basic multi-machine examples.

## Not yet claimed as complete

The following are goals, not finished public features:

- one-click installation;
- automatic discovery across arbitrary networks;
- broad hardware compatibility;
- autonomous visual evaluation;
- unattended long-running workflows;
- cloud/local hybrid routing;
- production-grade security hardening.

## Development principle

The public repository will distinguish clearly between:

1. features already demonstrated privately;
2. features implemented publicly;
3. experimental work;
4. future plans.

This is intended to keep the project technically honest and make progress easy to verify.

# Aubum Local Node

Aubum Local Node is an open-source project exploring how ordinary consumer PCs and GPUs can be combined into a coordinated, locally owned AI compute system.

The project grew out of Aubum, a working private AI orchestration prototype that I am developing independently.

## Project Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Current Status](docs/STATUS.md)
- [Worker Protocol Draft](docs/WORKER_PROTOCOL.md)
  
## Goal

Make it possible for an individual to combine multiple home computers into one practical AI system without requiring enterprise infrastructure or depending entirely on cloud services.

The long-term workflow is:

**Reason → dispatch work → execute on the appropriate machine → inspect the result → recover or continue → restore worker state**

## Current Prototype

The private Aubum prototype already includes working experiments with:

- Multi-computer job execution
- Centralized worker control
- GPU workload mode switching
- Previous-state restoration after jobs
- Remote Blender execution
- Automated Blender testing
- Vision-model integration
- Image and video generation workflows
- 3D-generation tooling
- Guarded system automation
- Local network orchestration

- ### Verified Deployment Topology — September 2026

The private Aubum system is currently operating across a heterogeneous five-device environment:

- **MAIN PC** — Big Brain / primary orchestration, reasoning, and system control
- **Herman** — RTX 4090 worker for Blender, 3D generation, image/video workflows, and heavy GPU execution
- **RTX 3070 PC** — dedicated voice and audio workloads
- **Steam Deck** — lightweight Aubum router running a small local model with Vulkan acceleration
- **Android phone** — remote control interface for MAIN and Aubum services

The current system has demonstrated cross-device routing, remote execution, managed GPU workload modes, worker-state restoration, lightweight model-based routing, and phone-based control across heterogeneous consumer hardware.

This deployment remains part of the private Aubum development environment. The public Aubum Local Node project is extracting the reusable infrastructure into a standalone open-source implementation.

## Aubum Local Node

This repository will focus specifically on the reusable local-compute infrastructure.

Planned components include:

- Worker discovery and health monitoring
- Secure local-network communication
- Job dispatch and routing
- GPU/resource-state management
- Automatic worker-state restoration
- Failure detection and recovery
- Logging and auditability
- Restricted/bounded worker permissions
- Reproducible installation
- Support for heterogeneous consumer hardware
- Documentation for non-expert deployment

## Research Questions

The project is intended to investigate questions including:

- Can heterogeneous consumer PCs operate reliably as one local AI system?
- How much manual administration can be removed from multi-machine AI workflows?
- Can workers recover from failures without losing system state?
- Can reasoning and GPU-heavy execution run simultaneously on separate machines?
- What safety controls are necessary before allowing longer autonomous workflows?

## Design Principles

### Local-first

The system should remain useful without requiring a permanent cloud dependency.

### User-owned

The person operating the system should control the hardware, models, data, and permissions.

### Heterogeneous

Users should be able to reuse different generations and types of consumer hardware rather than purchasing identical enterprise nodes.

### Bounded autonomy

Increasing automation should not require giving an AI unrestricted access to every machine.

### Recoverable

Jobs should fail safely, produce useful diagnostics, and restore workers to a known state whenever possible.

## Current Status

**Early development / working prototype**

The underlying private Aubum system is already being used for multi-machine AI and Blender workflows.

This public repository is being established to develop the reusable local-compute portion as a standalone open-source project.

Code, architecture documentation, benchmarks, installation tooling, and demonstrations will be added as the project is separated from the private Aubum environment.

## Development Roadmap

1. Define the public worker/controller architecture
2. Separate private Aubum-specific logic from reusable infrastructure
3. Publish an initial worker protocol
4. Build reproducible worker installation
5. Add hardware/resource discovery
6. Add job routing and state management
7. Add failure recovery and auditing
8. Test across multiple consumer hardware configurations
9. Simplify deployment for non-expert users
10. Release a documented v1.0

## About

Aubum Local Node is being developed by an independent developer and AI enthusiast exploring how far locally owned AI systems can be pushed using consumer hardware.

The project is currently self-funded and under active development.

## License

The public Aubum Local Node project is intended to be released under an open-source license.

Pre-existing private Aubum components are not automatically part of this repository or license.

# Aubum Local Node Architecture

Aubum Local Node coordinates AI, compute, memory, monitoring, and specialized workloads across heterogeneous consumer devices while keeping hardware, data, permissions, and execution under the user's control.

The project is based on lessons from Aubum, a working private local-AI system that distributes different responsibilities across multiple machines instead of trying to make one computer perform every role.

## High-Level Architecture

```mermaid
flowchart LR
    U["User"] <--> B["Big Brain / Reasoning"]

    B <--> C["Local Node Controller"]
    B <--> M["Persistent Memory"]

    C --> H["GPU Worker"]
    C --> V["Voice Worker"]
    C --> D["Steam Deck Router"]
    C --> P["Phone / Edge Control"]

    H --> G1["Vision / Blender / 3D / Image / Video"]
    V --> G2["Voice / Audio"]
    D --> G3["Lightweight Routing"]
    P --> G4["Remote Control / Edge Tasks"]

    W["Guarddog / Watchdog"] --> C
    W --> H
    W --> V
    W --> D
    W --> M

    G1 --> R["Results"]
    G2 --> R
    G3 --> R
    G4 --> R

    R --> C
    C --> B
    B --> U

Core Idea

The reasoning layer does not need to perform every task itself.

It can:

understand the requested goal;
determine the required capability;
select an appropriate worker;
prepare required resources;
dispatch the job;
monitor execution;
collect and validate the result;
detect failures;
restore the worker to a known state;
preserve useful state or memory;
return the result for the next decision.

The system favors specialization rather than duplicating the same large model or workload on every device.

Current Private Deployment

The private Aubum prototype currently operates across a heterogeneous six-device environment.

MAIN PC

Primary responsibilities:

Big Brain / reasoning;
orchestration;
Open WebUI;
system control;
health-check aggregation;
tool coordination.

MAIN remains the primary reasoning node rather than distributing independent copies of the main reasoning model across every machine.

GPU Worker

A dedicated high-end GPU workstation handles workloads including:

computer vision;
Blender automation;
3D generation;
image generation;
video generation;
rendering;
other GPU-heavy tasks.

The worker uses managed workload modes so incompatible GPU services do not need to remain loaded simultaneously.

The controller tracks the active mode and restores the worker to the appropriate state after jobs.

Voice Worker

A separate GPU-equipped PC is dedicated to:

text-to-speech;
voice processing;
audio workloads.

Keeping voice separate allows conversational or audio services to remain available without competing with the primary reasoning or graphics workloads.

Steam Deck Router

A Steam Deck operates as a lightweight routing node using a small local model with Vulkan acceleration.

Its role is to perform inexpensive routing and classification work without consuming the primary Big Brain or high-end GPU workers.

Guarddog + Memory Laptop

A dedicated laptop provides two infrastructure roles:

Guarddog

Guarddog independently observes the health of major Aubum nodes and services.

Current responsibilities include monitoring:

MAIN;
the GPU worker;
the Voice worker;
the Steam Deck router;
persistent Memory.

Guarddog is currently observation-only. Automated recovery is being introduced cautiously after normal operating behavior is characterized.

MAIN can also verify Guarddog itself, avoiding a design where the monitoring system could silently fail without detection.

Persistent Memory

The laptop also hosts Aubum's persistent external Memory service.

The private Memory backend remains local to the laptop.

A restricted bridge allows the Big Brain to perform approved operations such as:

store a durable memory;
retrieve a memory by ID;
search memories;
check Memory health.

Cross-machine and cross-session persistence has been verified in the private prototype.

The Big Brain can write a memory during one session and retrieve it from a fresh session later.

Android Phone

The phone currently participates as:

a remote control interface;
an edge compute node;
a recorded-video source;
a live camera / sensor source.

This allows Aubum to interact with the system away from the primary desktop while also providing visual input for vision workflows.

Controller Responsibilities

The Local Node Controller is intended to provide:

worker discovery;
health monitoring;
capability reporting;
job routing;
GPU and resource management;
job status tracking;
failure detection;
state restoration;
persistent-state coordination;
logging and auditability.
Worker Responsibilities

Workers expose only intentionally enabled capabilities.

Examples include:

local LLM inference;
computer vision;
Blender automation;
3D generation;
image generation;
video generation;
rendering;
voice and audio processing;
lightweight routing;
persistent memory;
testing;
development tools.

Not every worker needs every capability.

Aubum intentionally assigns specialized roles to different hardware.

State-Aware Execution

A typical job lifecycle:

Inspect current state
        |
Determine required capability
        |
Select worker
        |
Reserve resources
        |
Prepare worker
        |
Execute job
        |
Collect result
        |
Validate completion
        |
Store useful durable state
        |
Restore previous worker state
        |
Release resources

Failures should produce diagnostics and attempt safe restoration without unnecessarily disturbing healthy services.

Persistent Memory

Persistent Memory is treated as infrastructure rather than merely conversation history.

Useful durable information may include:

verified architecture facts;
known-good component versions;
important project decisions;
proven fixes;
milestones;
worker and capability information.

The current private prototype supports explicit memory storage and retrieval.

Automatic relevance-based retrieval and selective automatic memory writing remain active development areas.

Independent Monitoring

A distributed system should not rely entirely on the system being monitored to determine whether it is healthy.

The private prototype therefore uses an independent Guarddog node to observe other Aubum components.

The primary node can, in turn, verify the Guarddog node.

This creates a basic reciprocal health model:

Guarddog watches Aubum services
        |
        v
MAIN checks Guarddog
        |
        v
Guarddog checks local Memory

Guarddog watches Aubum services
        |
        v
MAIN checks Guarddog
        |
        v
Guarddog checks local Memory

Future work will add carefully bounded recovery actions after repeated failures are confirmed.

Bounded Autonomy

Workers and controllers should enforce:

allowed capabilities;
restricted commands;
resource limits;
validation;
logging;
approval boundaries;
recovery and rollback mechanisms;
network-access boundaries;
minimum necessary permissions.

The goal is useful automation without unrestricted machine access.

Heterogeneous Hardware

A local network may contain:

high-end GPU workstations;
older gaming PCs;
laptops;
handheld gaming hardware;
mobile devices;
CPU-only machines;
different GPU vendors and generations;
machines dedicated to particular workloads.

Workers report their capabilities so the controller can choose an appropriate system rather than requiring identical hardware.

Local-First Design

The core system should remain useful using user-owned hardware without requiring permanent dependence on a cloud provider.

Models, memory, workload execution, and orchestration can remain local while cloud services may optionally supplement the system where useful.

Current Status

The private Aubum prototype has already demonstrated:

multi-machine job execution;
centralized worker control;
managed GPU workload switching;
previous-state restoration;
remote Blender automation;
vision workflows;
image and video workflows;
3D-generation tooling;
dedicated voice workloads;
lightweight model-based routing;
phone-based control;
live and recorded video input;
independent system monitoring;
cross-machine persistent memory;
cross-session memory retrieval;
automated health checking;
guarded system actions.

The public project is separating reusable infrastructure from that private environment.

Private deployment details, credentials, machine-specific configuration, and unrelated Aubum components are not automatically part of the public project.

Public Development Goals
Define a clean worker/controller protocol.
Build reproducible worker installation.
Add resource and capability discovery.
Implement reliable job dispatch.
Add state management and restoration.
Add failure detection and bounded recovery.
Add logging and auditing.
Add persistent-state and memory interfaces.
Add bounded execution controls.
Test heterogeneous consumer hardware.
Simplify deployment for non-expert users.
Publish complete deployment documentation.
Development Principle

Known-good working components should not be replaced merely for architectural cleanliness.

New capabilities should be developed alongside verified baselines, tested independently, and promoted only after they demonstrate equivalent or better reliability.

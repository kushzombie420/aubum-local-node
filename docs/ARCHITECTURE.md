# Aubum Local Node Architecture

Aubum Local Node is designed to coordinate AI and compute workloads across multiple consumer PCs while keeping hardware, data, permissions, and execution under the user's control.

## High-Level Architecture

```mermaid
flowchart LR
    U[User] --> B[Reasoning / Orchestration Layer]

    B --> C[Local Node Controller]

    C --> W1[Worker PC 1]
    C --> W2[Worker PC 2]
    C --> W3[Worker PC 3]

    W1 --> G1[GPU / AI Workloads]
    W2 --> G2[Blender / Rendering]
    W3 --> G3[Vision / Other Tools]

    G1 --> R[Results]
    G2 --> R
    G3 --> R

    R --> C
    C --> B
    B --> U

Core Idea

The reasoning layer does not need to perform every task itself.

Instead, it can:

understand the requested goal;
determine what capability is required;
select an appropriate worker;
prepare the worker and required resources;
dispatch the job;
monitor execution;
collect the result;
detect failures or incomplete results;
restore the worker to a known state;
return the result to the reasoning layer for the next decision.
Controller Responsibilities

The Local Node Controller is intended to provide:

worker discovery;
worker health monitoring;
capability reporting;
job routing;
GPU/resource management;
execution boundaries;
job status tracking;
failure detection;
state restoration;
logging and auditability.
Worker Responsibilities

Each worker exposes only the capabilities it is configured to provide.

Examples may include:

local LLM inference;
computer vision;
Blender automation;
image generation;
video generation;
rendering;
testing;
development tools;
other approved local applications.

Workers should not require unrestricted control of the entire system.

State-Aware Execution

A major design goal is that a worker should not be left in an unknown or broken state after a job.

A job lifecycle should resemble:

Inspect current state
        |
Reserve required resources
        |
Prepare worker
        |
Execute job
        |
Collect result
        |
Validate completion
        |
Restore previous state
        |
Release resources

If a job fails, the worker should produce diagnostics and attempt safe restoration rather than silently remaining partially configured.

Bounded Autonomy

Aubum Local Node is intended to separate reasoning from privileged execution.

The reasoning system may request an action, but workers and controllers should enforce:

allowed capabilities;
restricted commands;
resource limits;
validation;
logging;
explicit approval boundaries where appropriate;
recovery and rollback mechanisms.

The goal is useful automation without requiring unlimited machine access.

Heterogeneous Hardware

The project is intended to support mixed consumer hardware rather than requiring identical cluster nodes.

A local network could potentially include:

high-end GPU workstations;
older gaming PCs;
CPU-only machines;
different GPU generations;
machines dedicated to specific workloads.

Workers report their available capabilities so the controller can select appropriate systems rather than assuming every computer is identical.

Local-First Design

Aubum Local Node is intended to remain useful without permanent dependence on an external cloud provider.

Optional cloud or remote resources may eventually be supported, but the core system should continue to function using user-owned local hardware.

Current Status

The private Aubum prototype has already been used for experiments involving:

multi-machine job execution;
remote Blender automation;
GPU workload switching;
worker state restoration;
computer vision;
image and video workflows;
automated testing;
guarded system actions.

This repository is separating the reusable infrastructure from that private environment into a documented open-source project.

Public Development Goals

The public Aubum Local Node project will focus on:

defining a clean worker/controller protocol;
reproducible worker installation;
resource and capability discovery;
reliable job dispatch;
state management and restoration;
failure recovery;
logging and auditing;
bounded execution controls;
testing across different consumer hardware;
deployment documentation for other users.


Then scroll down and click:

**Commit changes**

For the commit message, use:

`Add architecture documentation`

Then click **Commit changes** again.

Tiny GitHub trap avoided: yes, the Mermaid block inside the Markdown is intentional. GitHub should render it as an actual diagram instead of forcing you to become a graphic designer for 20 minutes.

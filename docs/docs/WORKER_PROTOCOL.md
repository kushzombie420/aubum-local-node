# Aubum Local Node — Worker Protocol Draft

This document defines the initial public protocol for communication between an Aubum Local Node controller and worker machines.

The goal is to keep the protocol simple, inspectable, implementation-independent, and safe enough to use across heterogeneous consumer hardware.

## Core Concepts

A Local Node consists of:

- one controller;
- one or more workers;
- a defined set of worker capabilities;
- jobs dispatched by the controller;
- structured status and result messages;
- explicit worker-state management.

A worker should only expose capabilities that have been intentionally enabled.

## Worker Identity

Each worker should report basic information such as:

```json
{
  "worker_id": "worker-01",
  "name": "example-worker",
  "status": "ready",
  "capabilities": [
    "llm-inference",
    "blender",
    "vision"
  ]
}

Capability Reporting

Workers may report:

available applications;
GPU model;
GPU memory;
system memory;
available storage;
active workloads;
supported job types;
current readiness state.

Example:

{
  "worker_id": "worker-01",
  "gpu": {
    "vendor": "NVIDIA",
    "model": "RTX 4090",
    "vram_gb": 24
  },
  "capabilities": {
    "blender": true,
    "vision": true,
    "image_generation": true,
    "video_generation": false
  }
}

Job Request

A job request should contain enough information for the worker to determine whether it can safely accept the task.

Example:

{
  "job_id": "job-0001",
  "job_type": "blender",
  "required_capabilities": [
    "blender"
  ],
  "resource_requirements": {
    "gpu_required": true,
    "minimum_vram_gb": 8
  },
  "task": {
    "action": "run_script",
    "script": "example_task.py"
  },
  "restore_previous_state": true
}

Job Lifecycle

A normal job moves through the following states:

queued
  |
accepted
  |
preparing
  |
running
  |
validating
  |
restoring
  |
completed

A failed job should enter:

failed
  |
diagnostics
  |
restoring
  |
recovered

If restoration fails:

recovery_failed

That condition should require human attention.

Status Message

Workers should provide structured status updates.

Example:

{
  "job_id": "job-0001",
  "worker_id": "worker-01",
  "status": "running",
  "progress": 0.45,
  "message": "Blender task executing"
}
Result Message

Successful jobs should return structured results.

Example:

{
  "job_id": "job-0001",
  "worker_id": "worker-01",
  "status": "completed",
  "result": {
    "success": true,
    "artifacts": [
      "render.png",
      "result.json"
    ]
  }
}
Failure Message

Failures should return useful diagnostics instead of only reporting an error.

Example:

{
  "job_id": "job-0001",
  "worker_id": "worker-01",
  "status": "failed",
  "error": {
    "type": "RESOURCE_UNAVAILABLE",
    "message": "Required GPU memory is not currently available"
  },
  "restoration_attempted": true,
  "restoration_successful": true
}
State Management

Before executing a job, a worker should record enough state to return the machine to a known configuration.

This may include:

running AI models;
active GPU workloads;
relevant services;
reserved resources;
temporary environment changes.

The exact state model will depend on the worker implementation.

Bounded Execution

The controller should not be able to send arbitrary unrestricted commands by default.

Workers should expose defined actions such as:

run_blender_job
run_inference
run_vision_job
generate_image
generate_video
run_test

Each capability can enforce its own:

allowed inputs;
resource limits;
time limits;
file boundaries;
command restrictions;
approval requirements.
Security Goals

The protocol should eventually support:

authenticated controller/worker communication;
encrypted network traffic;
worker allowlists;
capability-based permissions;
job logging;
replay protection;
rate limiting;
explicit privilege boundaries.
Current Status

This document is an initial protocol draft.

It describes the intended public interface and does not claim that every field or behavior shown here is already implemented in the public repository.

The protocol will evolve as working components are extracted, tested, and released.


Then commit it with:

`Add initial worker protocol draft`

After this commit, your repo has **README + architecture + honest status + an actual protocol spec**. That is a much more respectable thing for grant reviewers to land on.

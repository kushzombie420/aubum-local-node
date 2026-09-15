# Aubum Local Node — Worker Protocol Draft

This document defines the initial public communication model between an Aubum Local Node controller and worker machines.

## Core Concepts

A Local Node consists of:

- one controller;
- one or more workers;
- defined worker capabilities;
- jobs dispatched by the controller;
- structured status and result messages;
- explicit worker-state management.

Workers expose only capabilities that have intentionally been enabled.

## Worker Identity

Example:

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
```

## Capability Reporting

Workers may report:

- GPU model;
- GPU memory;
- system memory;
- available storage;
- active workloads;
- installed capabilities;
- supported job types;
- readiness state.

Example:

```json
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
```

## Job Request

Example:

```json
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
```

## Job Lifecycle

Normal lifecycle:

```text
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
```

Failure lifecycle:

```text
failed
  |
diagnostics
  |
restoring
  |
recovered
```

If restoration also fails:

```text
recovery_failed
```

That state should require human attention.

## Status Message

```json
{
  "job_id": "job-0001",
  "worker_id": "worker-01",
  "status": "running",
  "progress": 0.45,
  "message": "Blender task executing"
}
```

## Result Message

```json
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
```

## Failure Message

```json
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
```

## State Management

Before executing a job, a worker should record enough state to return the machine to a known configuration.

Relevant state may include:

- running AI models;
- active GPU workloads;
- services;
- reserved resources;
- temporary environment changes.

## Bounded Execution

The controller should not send unrestricted arbitrary commands by default.

Workers should expose defined actions such as:

```text
run_blender_job
run_inference
run_vision_job
generate_image
generate_video
run_test
```

Capabilities may enforce:

- allowed inputs;
- resource limits;
- time limits;
- file boundaries;
- command restrictions;
- approval requirements.

## Security Goals

The protocol should eventually support:

- authenticated controller/worker communication;
- encrypted network traffic;
- worker allowlists;
- capability-based permissions;
- job logging;
- replay protection;
- rate limiting;
- explicit privilege boundaries.

## Current Status

This is an initial protocol draft.

It describes the intended public interface and does not claim that every field or behavior shown here is already implemented.

The protocol will evolve as working components are extracted, tested, and released.

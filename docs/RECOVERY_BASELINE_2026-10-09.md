# Private Prototype Recovery Baseline — 2026-10-09

This document records a sanitized recovery milestone from the private Aubum prototype.

It is intentionally a public documentation snapshot, not a copy of the private production environment. Private prompts, memories, master checklists, user data, credentials, machine-specific secrets, customer/work data, generated private media, and model files are excluded.

## Why this baseline exists

A photo-edit routing investigation exposed hidden coupling between shared orchestration, media tools, sensor observation, and model-routing behavior. Repair work focused on restoring working behavior without casually redesigning the broader system.

The main lesson was simple: shared orchestration changes can destabilize otherwise unrelated capabilities. Aubum now treats preservation, rollback, regression testing, and observed end-to-end behavior as first-class requirements.

## User-observed verified behavior

The following behavior was manually exercised through the normal Open WebUI path after the recovery work:

- Big Brain sleep/wake control remained functional.
- SMALL / MEDIUM / BIG routing remained available.
- Local music generation completed without unrelated tool calls.
- Image generation completed through the intended image tool.
- Image editing completed through the intended edit tool.
- Text-to-video and image-to-video routing were repaired and validated with real video artifacts.
- Normal conversational acknowledgements completed with zero action-tool calls.
- Explicit live-camera requests automatically activated the connected phone-camera path.
- Live-camera responses were grounded in current camera evidence rather than unsupported model prose.
- Unavailable, blank, stale, uniform, or connection-placeholder camera sources fail closed instead of producing invented scene descriptions.
- Camera sessions started by an observation request are stopped after the bounded observation; an already-running feed is left running.

## Camera grounding contract

The recovered camera path now follows this contract:

1. An explicit camera request selects the camera observation tool.
2. If the source is not active, the tool attempts the existing bounded camera startup path.
3. Readiness requires more than a running capture process. The system checks for fresh, non-placeholder frame evidence.
4. Current-turn visual claims require current-turn observation evidence.
5. Blank, stale, uniform, unchanged, unavailable, or placeholder feeds do not authorize scene claims.
6. Failure responses report the condition and make zero unsupported visual claims.
7. Ordinary conversation and non-camera requests do not start the camera.

This behavior was manually confirmed with a real connected-phone camera activation and a recognizably grounded description of the scene.

## Media-routing hardening

The recovery also hardened several media-routing boundaries:

- image-generation requests are constrained to image generation;
- image-edit requests are constrained to image editing;
- music-generation requests are constrained to music generation;
- explicit video requests are constrained to video generation;
- post-tool continuation does not automatically imply another tool call;
- ordinary conversation can complete with no action tools;
- stale image/cache references are not allowed to hijack unrelated requests.

A video-source bug was also isolated where a literal placeholder from configuration text could be misread as a file identifier. Source resolution was tightened so pure text-to-video requests do not accidentally enter stale attachment/file-resolution paths.

## Verification rule

Aubum does not treat a printed PASS, a syntax check, or an agent report as sufficient proof of a working feature.

A feature is promoted to a known-good baseline only after relevant behavior is observed through the real user path.

Automated regression tests remain useful, but they support rather than replace user-observed verification.

## Preservation rule

Before future changes to a known-good path:

1. preserve the working original;
2. prefer a test copy, branch, or reversible change;
3. change the smallest coherent layer;
4. test the affected path and nearby regressions;
5. promote only after observed behavior is at least as reliable as the baseline.

## Public/private boundary

The public repository should contain reusable architecture, sanitized documentation, generic tests, and public implementation work.

It should not contain private system prompts, persistent-memory contents, personal or work master checklists, customer or employer data, credentials, private database snapshots, private generated media, or large local model files.

The private Aubum prototype remains the proving ground. Aubum Local Node extracts reusable infrastructure only after it can be documented without exposing private data.

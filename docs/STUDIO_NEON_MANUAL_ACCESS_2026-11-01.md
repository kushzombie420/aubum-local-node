# Aubum Studio Neon: Three-Mode Creative Access (Private Prototype)

**Checkpoint:** November 1, 2026 (America/Denver)  
**Status:** MAIN-driven manual UI access, 3D and music generation, and normal return-to-AUTO observed; restart and busy-job safeguards remain unverified.  
**Publication scope:** Sanitized engineering notes. **No private app, controller, bridge, credentials, or runnable installation is published here.**

## What changed

The privately operated Aubum prototype gained a single dark/neon **Aubum Studio Neon** desktop window on the primary workstation (MAIN), with three operator controls:

| Left | Center | Right |
| --- | --- | --- |
| **3D GEN** | **AUTO** | **MUSIC** |
| Opens the existing Hunyuan3D 2.1 UI on MAIN while the managed GPU worker executes it | Returns the managed GPU to its normal Aubum R2 ownership regime | Opens the existing ACE-Step 1.5 Playground on MAIN while the managed GPU worker executes it |

This closes a practical usability gap: earlier 3D and Music installations were functional but had no persistent, straightforward MAIN-side creative-mode interface. The user's normal workflow no longer requires opening a separate Hunyuan control window on the GPU worker for every session. The desktop app also displays live mode/lease status and recent activity.

The private integration reuses the already accepted **R2 exclusive GPU lease** boundary. MUSIC uses its pre-existing R2-managed worker path. Hunyuan, which did not previously have an R2 remote start mode, is reached through a **separate operator-controlled companion process** on the managed GPU worker. The production R2 controller was not replaced to enable this interface. The companion is not an independent GPU lease authority.

## Observed acceptance on November 1

The following records actual desktop/browser evidence and the user's subsequently supplied generation samples. **The user tested both generators successfully.** The remaining limits describe engineering coverage, not a failure or refusal to test.

| Operator action | Evidence-based result |
| --- | --- |
| Open one Studio shortcut on MAIN | **PASS:** Neon GUI opened with 3D GEN / AUTO / MUSIC and status reporting |
| AUTO -> 3D GEN | **PASS:** Hunyuan3D 2.1 web interface opened on MAIN via the worker |
| 3D GEN -> AUTO | **PASS:** Studio reported normal return to AUTO/IDLE with R2 lease verified free |
| AUTO -> MUSIC | **PASS:** ACE-Step 1.5 Playground opened on MAIN |
| MUSIC -> AUTO | **PASS, operator confirmed:** Normal return completed |
| 3D generation through Neon-managed Hunyuan | **PASS, user-provided screenshot:** A pumpkin input image and a newly generated mesh are visible in Hunyuan3D 2.1 | Mesh preview demonstrates generation; export of a GLB for this specific sample was not separately shown. |
| Music generation through Neon-managed ACE-Step | **PASS, user-confirmed and file provided:** Original generated music delivered as an MP3, independently verified as a playable-format 178-second stereo MPEG Layer III file | The audio artifact establishes output; it is not a quality benchmark or proof of concurrent jobs. |
| Return-to-AUTO **after those specific new generations** | **NOT RE-VERIFIED IN THIS TURN:** Earlier 3D -> AUTO and MUSIC -> AUTO tests passed before these generation samples | Keep earlier return tests PASS; do not assume new post-generation return evidence. |
| Restart of MAIN and the managed GPU worker, automatic bridge recovery | **NOT TESTED** |
| Queued/running web jobs, stale browser calls, concurrent switching, network loss | **NOT LIVE ACCEPTED** |

A direct 3D-to-MUSIC handoff was **not** part of this acceptance. The observed path is **3D -> AUTO -> MUSIC**; each manual session must safely release before the next owns the GPU.

## Implementation and recovery lessons

- In an earlier temporary Hunyuan access control, probing an unused web port was incorrectly treated as an unknown/timeout state. A subsequent control started Hunyuan successfully but failed while updating encrypted session metadata, leaving the R2 operator lease held while the real worker process tree ran.
- An exact-identity interrupted-session rescue recorded that existing process tree without restarting Hunyuan, preserved the R2 lease, and permitted a guarded return to AUTO. This proves recovery of **that observed session**, not generalized GPU-worker crash recovery.
- In a temporary Music control, synchronous startup briefly caused Windows to display `Not Responding`; the existing ACE-Step UI eventually loaded. The Neon interface moves work off the GUI thread, but comprehensive latency and resilience testing remains open.
- Operator-facing design should be simpler than the machinery underneath: one window, unambiguous mode status, one GPU owner at a time, no typed uppercase confirmations, and a readable newest-first activity log.
- A timeout, a seemingly empty web page, or an idle-looking GPU is **not** authority to terminate workers or forcibly clear a lease.

## Remaining work

1. **Post-generation return and export:** Representative 3D mesh creation and music generation **PASSED** in Neon-managed sessions. Verify a downloaded GLB if needed, then verify return-to-AUTO after completed, saved generation. Earlier normal returns passed before these sample creations.
2. **Safe busy-state behavior:** Establish what happens with real queued/running Gradio jobs, stale web sessions, and switching requests before accepting stronger fail-safe claims.
3. **Restart continuity:** Validate the private companion's startup/authentication and both-mode returns after a planned reboot. Do not imply unattended recovery already works.
4. **Cleanup without regressions:** Pin the working MAIN shortcut and worker companion locations before archiving superseded test ZIPs or launchers.
5. **Public extraction:** Design a separate, configurable, audited, and mock-testable version if reusable source is to be released. Do not publish the private controller, network addressing, credentials, or machine-specific scripts.

## Relationship to existing R2

This milestone builds on the accepted October 31 R2 cutover, whose **9/9 lease-contention checks** and **3/3 real chat-path MUSIC/PHOTO/VISION tests** remain intact. The new Studio test is about **manual creative access** and normal mode transitions; it does not replace those previously accepted automatic capabilities, complete the model-upgrade roadmap, close Aubum Continuity, or prove catastrophic GPU recovery.

See [October 31 R2 cutover and voice recovery](R2_CUTOVER_AND_VOICE_RECOVERY_2026-10-31.md) and [Current Status](STATUS.md) for the broader context.

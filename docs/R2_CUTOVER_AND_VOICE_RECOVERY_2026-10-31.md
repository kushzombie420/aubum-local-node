# Controlled GPU Lease Cutover and Voice Recovery — 2026-10-31

**Scope:** Sanitized engineering checkpoint from the privately operated Aubum system, October 30–31, 2026.  
**Result:** Controlled R2 lease rollout **PASS**, lease-conflict acceptance **9/9 PASS**, real chat-path MUSIC / PHOTO / VISION acceptance **3/3 PASS**, and conversational Read Aloud **RESTORED** (user-confirmed).

This is **not** a public release of the private R2 controller, deployment tools, endpoint configuration, or secrets. The public Aubum Local Node repository remains a separate extraction project.

## Why R2 was needed

On October 23 the private system had recovered **manual** GPU-mode selection. Before R2, natural-language Aubum requests had also demonstrated automatic MUSIC, PHOTO, and VISION routing through the existing controller. The R2 cutover did **not** invent those working capabilities; it added an explicit **exclusive GPU lease boundary** so a second competing request must fail safely instead of disrupting the first job.

The objective was to preserve working standard music, Qwen Image 2.1, and vision services while adding contention protection and previous-mode restoration. The previously verified legacy MUSIC backend stayed in use. Separate XL transport and Blender legacy integration paths were intentionally kept outside this release boundary.

## Controlled deployment and recovery safeguards

The private cutover used an agreed maintenance window with job-submission freeze and host-local checks, followed by a coordinated two-machine installation:

1. Verified original and staged file hashes, scripts, startup tasks, and idle/lease evidence. Background callers were explicitly inventoried rather than assuming that an empty chat screen meant no jobs.
2. Ran an isolated scratch **single-transaction** forward update and a reverse rollback drill against an offline SQLite copy. The drill preserved unrelated tool records, and used the SQLite backup API for a consistent backup rather than copying a live WAL database.
3. Applied one production database transaction to **10 registered Aubum tool definitions**, preserving **51 unrelated tool definitions**. Production post-checks verified 10/10 installed candidate contents and expected registry history/generation increments.
4. Installed five hash-gated worker candidates after separately verifying timestamped backups of the original controller-related files and scheduled-task definitions.
5. Replaced the controller only after confirming one identifiable old controller process, an IDLE mode, and no conflicting GPU listeners. The new controller started with VISION verified and no lease held.
6. Restored Open WebUI using its **original desktop launcher and environment**, then conducted real chat-path acceptance tests before closing the cutover.

Original files, task definitions, and database rollback checkpoints were retained. An uncertain or held lease was explicitly **not** an authorization to force-clear ownership or automatically downgrade the controller.

## What passed, and what the evidence does not claim

| Verification | Observed result | Scope boundary |
| --- | --- | --- |
| Installed R2 tool definitions | **10/10 PASS** | Private production Open WebUI registry; not published source code. |
| Lease-conflict acceptance | **9/9 PASS** | Acquire, visible held state, competing request rejected with HTTP **409 `GPU_BUSY`**, owner refresh, invalid-secret release rejected, valid release, and return to free. |
| MUSIC | **PASS** | A short original instrumental was generated and delivered as an MP3 through the actual Big Brain chat. |
| PHOTO | **PASS** | Qwen Image 2.1 generated and delivered a PNG through chat. |
| VISION | **PASS** | An attached image was inspected and a descriptive response returned. |
| Worker restoration | **PASS** | Final worker mode VISION, vision slot verified/idle, lease `held=false` and `corrupt=false`, conflicting generation workers not left running. |
| Open WebUI original state | **PASS** | Existing users, chat history, models, and the ten R2 tools were recovered through the correct production database. |

The three creative tests were run **sequentially** without manual mode selection. They are **not** proof of unlimited concurrent throughput, safety of unrelated legacy callers, independent visual-quality certification of the generated PNG, or full public deployment readiness.

### Acceptance-test cleanup lesson

An early test harness used an invalid lease-owner value and an incorrect release-secret transport. One test lease was left held. The recovery first checked the public owner/job identity, bound the existing private secret to the held lease without echoing it, released only that identified lease, and verified that ownership was free before rerunning the test. The corrected **9/9** acceptance suite then passed.

**Lesson:** A test suite can fail because its assumptions differ from the actual contract. Never interpret an aborted test as a controller failure without examining the response, and never clear ambiguous ownership to get a green test.

## Open WebUI startup incident and fix

During restoration, an ad hoc server launch copied the prior process's command-line arguments and working directory but **omitted the desktop application's data-directory environment**. Open WebUI therefore initialized a separate empty database and displayed first-run onboarding, even though the real production database and R2 transaction were intact.

A subsequent duplicate desktop launch collided with the first app's alternate backend port. The correct recovery was to stop only the erroneous instances, confirm the original data store had not been replaced, then launch **one** copy of the original desktop application normally. The existing Big Brain interface, chat history, models, and R2 tools returned.

**Lesson:** Matching CLI arguments is not equivalent to reproducing a working service environment. Before assuming data loss or restoring backups, inspect the active process's data-directory setting and open database. Avoid duplicate launches and destructive restoration.

## Conversational voice recovery

A Read Aloud request produced an Open WebUI server-connection error. The existing TTS configuration still referenced the voice PC's **previous LAN address**, while the RTX 3070 voice worker was running and listening at a **different, currently assigned address**.

The team verified:

- the previous endpoint timed out;
- the newly discovered voice endpoint was reachable over TCP;
- the voice helper reported ready status with CUDA available;
- the existing OpenAI-compatible speech request, with the preserved model/voice/format parameters, returned valid WAV audio;
- changing only the Open WebUI **TTS API base URL** through the supported admin interface restored user-confirmed **Read Aloud**.

No new voice model, reinstalls, controller changes, or voice-service replacements were needed. Microphone transcription and Unreal voice/lip-sync integrations were **not retested as part of this fix**.

### Prevent recurrence: network identity (**PLANNED**, not complete)

Inspect the router's existing DHCP reservations, the voice machine's actual adapter identity, and potential address conflicts before reserving a stable IP or using reliable local name resolution. After any deliberate network change, validate TTS connectivity and Read Aloud again. A DHCP reassignment is a likely explanation for the observed address change, **not a proven router diagnosis**.

The broader Aubum network may have other address assumptions; inventory before changing any working service endpoint.

## Held out / next steps

- **DEFERRED:** XL Turbo authenticated-transport/controller-hash integration. Previous XL tests remain historical; this R2 acceptance **does not certify XL production cutover**.
- **DEFERRED:** Legacy Blender scheduled-task and bridge rollover, and independent non-leased callers outside the controlled tools.
- **DEFERRED:** Safe removal of stray first-run Open WebUI files after verifying their identity and non-use.
- **PLANNED:** Stable voice worker network identity, with router checks first.
- **IN PROGRESS:** Extract and sanitize reusable lease-control, worker-protocol, tests, installer, and failure-recovery code for this **public** repository. Private production scripts are not automatically open-source.
- **ONGOING:** Aubum model upgrades and broader local-first orchestration work; neither was closed by the R2 milestone.

## Design lessons for Aubum Local Node

A reusable public implementation should model exclusive resource ownership explicitly; return a structured BUSY response for contention; bind release to the correct owner/lease; restore the pre-job mode on success; hold ambiguous recovery for operator review; preserve backups and known-good behavior; and require both isolated atomic tests **and live user-path verification** before promotion.

The October 23 manual recovery remains a valid historical checkpoint. The October 31 R2 acceptance supersedes it **only for the private controller paths actually tested**.

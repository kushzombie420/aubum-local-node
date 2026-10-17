# Private Big Brain Baseline — 2026-10-16

This document records a sanitized Big Brain promotion milestone from the private Aubum prototype.

It intentionally records the architecture, verification results, and rollback boundary without publishing private prompts, credentials, personal paths, model files, or machine-specific secrets.

## Promotion summary

The primary Big Brain was promoted from a Qwen3.6 27B-class Q4_K_P GGUF to a Qwen3.8 27B-class Q4_K_P GGUF.

The promoted configuration uses:

- RTX 4090 inference on MAIN;
- CUDA-enabled llama.cpp build **b11669**;
- **32K context**;
- one inference slot;
- GPU layer offload;
- reasoning disabled for normal production responses.

The previous Qwen3.6 configuration remains preserved as the rollback baseline rather than being deleted or overwritten.

## Performance result

A direct Qwen3.8 test measured approximately **42.4 tok/s** generation.

The prior production Qwen3.6 CUDA baseline was approximately **42.57 tok/s** generation.

The promotion therefore preserved essentially the same observed generation throughput while moving the primary reasoning role to the newer model family.

The older historical Vulkan-to-CUDA benchmark remains separately documented because it measured a backend migration rather than this model swap.

## Behavioral comparison

Before promotion, Qwen3.8 was exercised in isolated A/B troubleshooting prompts against the previous Qwen3.6 Big Brain.

Observed reasons for promotion included:

- comparable raw generation speed;
- concise completion of several constrained technical prompts;
- comparable or better behavior on the tested troubleshooting tasks;
- successful 32K loading and stable local API behavior.

Neither model was treated as hallucination-free. Promotion was based on the observed overall result plus rollback availability, not on an assumption that a newer model name guarantees better reasoning.

## Production-path verification

The promotion was then tested through the real user path rather than only through a direct local API.

Verified path:

```text
Open WebUI
    |
    v
Sentinel
    |
    v
Gatekeeper
    |
    v
Qwen3.8 27B Big Brain on RTX 4090
```

A hard BIG request successfully caused Gatekeeper to wake Qwen3.8 and return a response through Open WebUI.

The Big Brain process remained behind the existing Gatekeeper interface, so the surrounding SMALL / MEDIUM / BIG architecture did not require redesign for the model replacement.

## Sleep-path issue found during promotion

Testing exposed an Open WebUI housekeeping edge case.

After a manual sleep:

1. Gatekeeper successfully unloaded the Big Brain.
2. Open WebUI automatically submitted a background follow-up-prediction request beginning with `Predict 3-5 useful messages...`.
3. That prompt carried prior conversation context containing terms such as Unreal/debug.
4. Sentinel did not recognize the newer housekeeping prompt wording.
5. The existing hard-BIG rule therefore routed the housekeeping request to Gatekeeper.
6. Gatekeeper correctly woke the Big Brain again.

The visible symptom was an RTX 4090 VRAM drop followed by an immediate return to the loaded Big Brain footprint.

## Sleep-path fix

Two changes were verified:

- Sentinel now waits for the Gatekeeper `/control/sleep` result and reports `Big Brain is asleep.` only after sleep is confirmed.
- Sentinel recognizes the current Open WebUI `Predict 3-5 useful messages...` background prompt as housekeeping and routes it to SMALL.

A before/after trace reproduced the original BIG re-wake and then showed the same post-sleep follow-up request taking the SMALL housekeeping route after the fix.

The underlying Gatekeeper-owned sleep mechanism itself did not require redesign.

## Known-good state

At the end of the promotion work:

- Qwen3.8 is the primary Big Brain configuration;
- the Open WebUI -> Sentinel -> Gatekeeper -> Qwen3.8 path is verified;
- SMALL / MEDIUM / BIG routing remains intact;
- manual sleep is Gatekeeper-confirmed before success is reported;
- the identified Open WebUI follow-up housekeeping request remains on SMALL after sleep;
- Qwen3.6 remains available as the rollback baseline.

## Public/private boundary

The public repository records the reusable architecture and sanitized evidence.

The large GGUF model, private production paths, credentials, user data, system prompts, and private backup files are intentionally excluded.

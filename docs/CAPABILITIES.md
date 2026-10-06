# Aubum Capability Matrix

This page is the quick-reference view of what the private Aubum prototype can already do, which hardware currently handles each role, and what is still planned for the public Aubum Local Node project.

The goal is to keep verified behavior separate from experiments and future work.

## Status legend

- **Verified** — demonstrated in the private Aubum prototype.
- **Experimental** — working in a limited or still-hardening form.
- **Planned** — designed or queued, but not yet treated as complete.
- **Public extraction** — capability exists privately and is being separated into reusable public infrastructure.

## Current capability matrix

| Capability | Current role / node | Model or system | Status |
|---|---|---|---|
| Primary reasoning | MAIN RTX 4090 | Qwen3.6 27B-class GGUF through llama.cpp CUDA | **Verified** |
| Lightweight request routing | Steam Deck | Qwen3 1.7B-class local model with Vulkan acceleration | **Verified** |
| Dedicated medium reasoning | GTX 1080 Ti worker | Qwen3.5 9B-class Q6_K GGUF through llama.cpp CUDA, 16K context | **Verified** |
| Three-tier request routing | MAIN + Steam Deck + Medium worker | Sentinel SMALL / MEDIUM / BIG routing | **Verified** |
| On-demand Big Brain wake | MAIN | Sentinel + Gatekeeper + llama.cpp | **Verified** |
| Idle Big Brain unload | MAIN | 15-minute protected idle timeout | **Verified** |
| Active-request sleep protection | MAIN | Gatekeeper request tracking | **Verified** |
| Chat resource controls | MAIN | Local `status` and `sleep` commands | **Verified** |
| Live web research | MAIN | Open WebUI search + primary reasoning model | **Verified** |
| Source-cited web answers | MAIN | Open WebUI search integration | **Verified** |
| PDF / document reading | MAIN | Local text extraction + reasoning | **Verified** |
| Persistent external Memory | Laptop | Local Memory service + restricted bridge | **Verified** |
| Cross-session memory retrieval | MAIN + laptop | Open WebUI Memory tooling | **Verified** |
| Automatic relevance-based Memory | MAIN + laptop | Planned recall/write layer | **Planned** |
| Independent system monitoring | Guarddog laptop | Observation-only health monitoring | **Verified** |
| Full health aggregation | MAIN | Aubum Health Check v0.6, verified 30 PASS / 0 WARN / 0 FAIL | **Verified** |
| Medium Brain health-check coverage | MAIN + Medium worker | TCP reachability + model/API endpoint checks | **Verified** |
| Desktop visual observation | MAIN / vision worker | Direct screen capture + vision analysis | **Verified** |
| Condition-aware visual supervision | MAIN / vision worker | Bounded repeated inspection | **Experimental** |
| Saved visual evidence | MAIN / vision worker | Frames/contact sheets + reinspection | **Verified** |
| Live phone camera input | Android + vision worker | Phone camera / vision pipeline | **Verified** |
| Recorded video input | Android + vision worker | Video analysis pipeline | **Verified** |
| Vision-model workflow | GPU worker | Qwen3-VL 8B-class vision model | **Verified** |
| Image generation | GPU worker | ComfyUI-based workflow | **Verified** |
| Video generation | GPU worker | Local GPU workflow | **Verified** |
| Blender automation | GPU worker | Remote Blender execution/testing | **Verified** |
| 3D-generation tooling | GPU worker | Local 3D workflow | **Verified** |
| Voice / audio specialization | RTX 3070 PC | Dedicated voice/audio worker role | **Verified foundation** |
| Full STT -> reasoning -> TTS pipeline | RTX 3070 PC | Planned voice stack | **Planned** |
| Secure remote mobile access | Android + MAIN | Tailscale + Tailscale Serve + Open WebUI | **Verified** |
| Tailnet-only remote HTTPS access | MAIN | Tailscale Serve | **Verified** |
| Manual phone file transfer | MAIN -> Android | Taildrop | **Verified** |
| Phone-local edge inference | Android | Qwen3 4B-class local model | **Verified** |
| Storage Librarian / semantic file manager | MAIN + storage | File indexing, classification and move tooling | **Planned** |
| Generated-media retention cleanup | MAIN + archive storage | Bounded archive/cleanup policy | **Planned** |
| Automatic hardware capability discovery | Future worker nodes | Worker inventory + benchmark reporting | **Planned** |
| Portable temporary worker bridge | Android + temporary PC | Bounded remote worker bootstrap | **Planned** |
| Music / audio generation | Dedicated worker | Local generative-audio stack | **Planned** |

## Current model roles

The private prototype intentionally uses different model sizes for different jobs rather than keeping one large model loaded everywhere.

| Role | Current model family | Why it is used |
|---|---|---|
| Primary Big Brain | Qwen3.6 27B-class GGUF | Main reasoning, coding, synthesis, complex requests |
| Medium Brain | Qwen3.5 9B-class Q6_K GGUF | Intermediate conversational/contextual reasoning without waking the primary 27B |
| Steam Deck router | Qwen3 1.7B-class | Cheap classification/routing without occupying the primary GPU |
| Vision | Qwen3-VL 8B-class | Image, camera, and saved-evidence inspection |
| Phone edge model | Qwen3 4B-class | Lightweight local mobile inference and edge experiments |
| Turn supervision / support model | Local Ollama model | Auxiliary control/supervision work where a second large reasoning pass is unnecessary |

Exact private model files, machine addresses, tokens, credentials, and personal paths are intentionally omitted from the public documentation.

## Verified performance snapshot

A direct backend comparison on the same primary 27B model and RTX 4090 measured approximately:

- **5.71 tok/s** generation on the earlier Vulkan path;
- **42.57 tok/s** generation after moving the production path to CUDA;
- **919.5 tok/s** prompt processing before the CUDA migration;
- **2775.6 tok/s** prompt processing after the CUDA migration.

That is roughly a **7.5x generation-speed improvement** and a **3x prompt-processing improvement** while preserving the existing 32K-context production setup.

## Current health baseline

Aubum Health Check v0.5 has completed a verified run with:

- **27 PASS**
- **0 WARN**
- **0 FAIL**

The current checks cover the main distributed services, Guarddog/Memory infrastructure, routing and Big Brain power state, and the secure remote-mobile boundary.

The remote-mobile checks verify that:

- Tailscale is running;
- MAIN is connected to the tailnet;
- Tailscale Serve remains tailnet-only;
- the private Serve proxy still targets localhost Open WebUI;
- Open WebUI remains localhost-bound;
- Open WebUI responds locally.

The phone itself is intentionally not required to be online for infrastructure health.

## Current device specialization

| Device class | Current responsibility |
|---|---|
| MAIN RTX 4090 system | Primary reasoning, orchestration, Open WebUI, system control, health aggregation |
| GPU worker RTX 4090 system | Vision, Blender, 3D, image/video generation, rendering, heavy GPU execution |
| RTX 3070 PC | Voice and audio specialization |
| Steam Deck | Lightweight model-based routing |
| Laptop | Independent Guarddog monitoring + persistent Memory |
| Android phone | Remote control, local edge inference, camera/video input, secure cellular access |

## Near-term direction

The next private-prototype priorities are intentionally practical:

1. storage cleanup and reorganization;
2. Linux sideloading after storage is understood;
3. VRAM cleanup and on-demand service management on the GPU worker;
4. the full RTX 3070 voice pipeline;
5. bounded generated-media retention;
6. Storage Librarian / semantic file management;
7. portable temporary-worker experiments;
8. smarter automatic Memory;
9. public demos, screenshots, diagrams, and reproducible examples.

## Public-project boundary

Aubum Local Node is not claiming that every private Aubum capability is already packaged for public installation.

The public repository is extracting the reusable parts gradually: worker discovery, health monitoring, routing, resource management, bounded execution, persistent-state interfaces, recovery behavior, and heterogeneous-hardware coordination.

That distinction is deliberate. Verified private behavior is documented as evidence; public features will be marked complete only when they are actually reproducible outside the private environment.

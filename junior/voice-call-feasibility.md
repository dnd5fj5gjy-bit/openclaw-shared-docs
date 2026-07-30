# Can Jesse phone Junior and have it feel like a real conversation?

Technical feasibility report. 30 July 2026. Prepared for Felix, summarised separately for Jesse.

Short answer: **yes, buildable, roughly £0 ongoing, about one second of reply gap.** It will feel like a very good voice assistant. It will not feel like a human being, and the reason is structural rather than a tuning problem.

Three sources feed this: my own benchmarks on the Mac Studio (`notes/voice-local-bench.md`), transport research (`notes/voice-transport.md`), and speech/latency research (`notes/voice-brain.md`). Where research contradicted my measurements, or Felix's starting points, that is called out.

---

## 1. Felix's four starting points, verified

| Claim | Verdict |
|---|---|
| Telegram Bot API has no voice call support | **Confirmed.** Voice notes and audio files only. The bot cannot ring. |
| Options are MTProto userbot + pytgcalls, a WebRTC PWA, or Twilio at ~$1/mo + 1.3c/min | **Mostly right, three corrections below.** |
| Claude has no realtime speech-to-speech API; loop must be STT -> LLM -> TTS | **Confirmed.** |
| Gemini Live etc. feel more human but the free tier trains on your audio | **Confirmed, and it is worse than stated.** Google's own terms say do not send confidential data to the free tier. Three of four major cascaded vendors train on your audio by default. |
| Junior at Opus 5 high effort is too slow to hold a conversation | **Confirmed empirically.** Felix asked me for HAL's Telegram handle at 14:05:37 today; my reply went out roughly two minutes later, for a two-tool-call lookup. Conversation needs sub-second. That is a gap of about two orders of magnitude and it is not tunable. |
| Kokoro TTS local and free, bm_george / bm_lewis | **Confirmed and measured.** |
| Whisper on Metal at ~0.3s | **Half right.** The 0.3s is real. But it is `base` on **CPU**, not Metal. No whisper.cpp, faster-whisper or mlx-whisper is installed on this machine. |

### Corrections to the transport picture

1. **pytgcalls is not group-chats-only.** This is the most commonly repeated claim about it and it is out of date. Version 2.3.3 ships a working private 1-to-1 call example with raw PCM in and out. The stale claim traces to a 2021 PyPI page for the old package name.
2. **Twilio Media Streams is not free.** It is $0.0044/min and is absent from its own documentation, which is how the myth spreads. Twilio also rounds up to whole minutes. Real cost is $2.93-6.82/mo, not $1/mo. Elastic SIP Trunking is the cheaper path at $1.15/mo + $0.0060/min with no Media Streams fee.
3. **A WebRTC PWA cannot ring the phone.** iOS reserves incoming-call UI for CallKit, which is native-app-only. There is no web equivalent and there will not be one. iOS also mutes the mic when a PWA backgrounds. So the PWA works, but only when Jesse opens it and starts the conversation himself.

---

## 2. What I measured on this box

Apple M4 Max, 16 cores, 64 GB.

**Kokoro TTS.** Today, through the existing CLI wrapper, a voice message costs **6.4 seconds**. Almost all of that is process startup and model load, not synthesis. Held warm in a persistent process:

| Input | Time to first audio | Audio produced |
|---|---|---|
| 22 chars | **0.32s** | 2.3s |
| 75 chars | **0.34s** | 5.7s |
| 206 chars | **0.69s** | 13.0s |

This matters more than it looks. The research flagged that **nobody publishes local Apple Silicon TTS time-to-first-audio** and that it is the least characterised stage in the whole pipeline. It also carried a Picovoice benchmark measuring Kokoro at **2,925 ms** first-audio on CPU, which would have disqualified it outright. That figure is x86 and does not hold here: on this machine Kokoro delivers first audio in **0.32s**. The underlying architectural point in the benchmark is still true, Kokoro does not stream input, so first-audio time scales with input length. The fix is to feed it one sentence at a time so the first sentence plays while the rest generates. That holds first audio near 0.3s regardless of how long the answer is.

**Whisper STT.** The interesting result.

| Config | 9.8s clip | Output |
|---|---|---|
| base | 0.27s | "the **bellmark**, quote, expired yesterday" |
| small | 0.70s | "The **Belmark** quote expired yesterday" |
| **base + `initial_prompt`** | **0.27s** | "the **Belmark** quote expired yesterday" |

My first conclusion was to move to the `small` model. That was wrong and I checked it. Seeding `initial_prompt` with our own vocabulary (Belmark, ACF Pharma, Lightning Nutra, Raemy, Voy, SCEND, Inuvi, Parkacre, Modern Savage, Ted's Health, GSET) fixes the proper nouns **and the spurious commas at zero latency cost**, 0.271-0.273s versus 0.274-0.276s over three runs each. We have a known, finite business vocabulary. Use it.

**This is worth doing today regardless of the phone-call project.** The Telegram listener currently calls `whisper.load_model("base")` at `telegram_listener.py:437` with no prompt, which means every voice note Jesse sends is transcribed by the model that gets his own suppliers' names wrong. One-line fix.

**What is missing.** No Ollama, no MLX, no llama.cpp. The fast conversational model does not exist on this machine and installing it needs Jesse's or Felix's sign-off under my own operating rules.

---

## 3. The latency budget

Fully local, warm process, headset.

| Stage | Realistic | Note |
|---|---|---|
| Mic capture + buffer | 20 ms | CoreAudio |
| VAD inference | 1 ms | Silero v5, 189 µs per 32 ms chunk |
| **Endpointing wait (dead air)** | **300-550 ms** | The largest line, and pure waiting |
| Semantic turn model | 70 ms | Smart Turn v3.2, 8 MB |
| STT | 180-270 ms | base + prompt, measured here |
| **LLM time to first token** | **150-400 ms** | With a cached prefix. ~1,000 ms if caching breaks |
| Sentence aggregation | 20 ms | |
| **TTS first audio** | **~300 ms** | Kokoro, measured here |
| Playback buffer | 40 ms | Do not accept a default 500 ms player buffer |
| **Total** | **~1.0-1.5s** | |

Three things worth Felix's attention:

- **Endpointing is 30-50% of the budget and it is a policy cost, not a compute cost.** All model inference across the entire VAD and turn-detection stack is under 100 ms. The win is dropping VAD `stop_secs` to 200 ms and letting an 8 MB semantic model decide whether the pause was a real end of turn. That is worth more than any model upgrade.
- **Prefix caching is the trap.** Get it right and LLM TTFT is ~45 ms. Get it wrong and it swings to ~1,000 ms and becomes the dominant line. Sliding-window and hybrid architectures (Gemma 3/4, Qwen 3.5) silently fall back to full re-prefill in both llama.cpp and mlx-lm **with no error raised**. Pick the model with this in mind.
- **Running locally deletes about 480 ms of network and serialisation overhead** that was 46% of the only honest instrumented cloud measurement anyone has published. That is a bigger effect than any model choice.

**Where this lands.** Around one second of reply gap. Comfortably inside the industry's 1,500 ms target. Above the ~700 ms threshold at which published research says a pause stops reading as latency and starts reading as reluctance or reticence. So: fluent and responsive, but a person would clock it as a machine.

---

## 4. Barge-in matters more than latency

Being able to talk over it and have it stop is what makes a voice system feel alive, more than shaving 200 ms.

It is also where the failure modes are. Raw VAD has an **84% false-interruption rate**. Even Gemini 2.5 falsely interrupts on backchannels ("mm-hmm", "right") about **63%** of the time. Only **2% of voice developers report being satisfied with conversation quality**, in an industry that has already achieved sub-second latency. Latency is the solved part. Turn-taking is not.

**One architectural decision must be made before anything else is built: acoustic echo cancellation needs the playback reference signal, and it cannot be retrofitted.** If the pipeline is built without routing that signal through, adding barge-in later means rebuilding the audio path. Headset use sidesteps it; speakerphone does not.

---

## 5. Recommended build

**Telegram userbot (pytgcalls 2.3.3) driven by Pipecat 1.6.0 through a custom transport.**

Reasoning:
- Only a Telegram userbot or a real phone number can actually **ring** an iPhone. That rules out the PWA as primary and the Bot API entirely.
- Between those two, **confidentiality decides it.** Telegram 1-to-1 calls are end-to-end encrypted with a DH handshake and Telegram cannot decrypt them. PSTN audio is in the clear inside the carrier by design, which no amount of self-hosting changes. For family-office and Ted's Health material that is the whole argument.
- Cost agrees but less dramatically than expected. Userbot is £0 forever; a real number is £1-6/mo and bills even in a month with no calls. **Argue it on confidentiality, not price.**
- **Pipecat over LiveKit** for this shape: one process rather than two, a genuinely local audio path (`LocalAudioTransport`), first-party Apple Silicon STT, Kokoro as a first-party TTS service, and a turn-detection model that is BSD-licensed and bundled. LiveKit's flagship turn detector **moved to cloud inference in June 2026**, so a "fully local" LiveKit build now silently gets the degraded model. Pipecat's custom transport surface is small, the reference implementation is 233 lines, and it maps one-to-one onto pytgcalls' PCM primitives.

**Two hard conditions:**
1. **Run the userbot on a separate Telegram account with its own number, never Jesse's personal account.** Userbots are a ToS grey zone and enforcement is effectively unappealable. Losing a throwaway account is an annoyance. Losing Jesse's primary Telegram is a business incident.
2. **Get a view on the Telegram API terms clause** prohibiting use of platform data "to train, fine-tune or otherwise engage in the development" of AI systems. Inference is arguably not development, but the clause is broad and deliberate. Genuine unresolved risk, not a formality.

If either condition is unacceptable, fall back to the **WebRTC PWA over Tailscale with Pipecat's `SmallWebRTCTransport`**. Free, fully private, no ToS exposure. The only loss is that Jesse must open it and start every conversation rather than being rung.

**Two tiers, non-negotiable.** A fast local model handles the conversation. Anything that is real work gets handed to me asynchronously through the existing message queue, and I come back on Telegram when it is done. The voice layer should be able to say "I am on it" and mean it, not stall the call while Opus 5 thinks.

---

## 6. What is genuinely free versus what costs

**Free, already owned:** Mac Studio compute, Kokoro TTS, Whisper STT, Silero VAD, Pipecat, Smart Turn, Telegram itself.

**Free but needs installing (approval required):** a local conversational model via Ollama or MLX, roughly 3-8 GB on disk.

**Costs money, and only if we choose it:** a real phone number, $1.15-6.82/mo depending on path. Only needed if someone other than Jesse must reach the assistant, or it has to work without Telegram.

**The hidden cost is build time, not running cost:** roughly 6-12 hours for the userbot transport, plus Pipecat integration and tuning. Call it a couple of focused days to something genuinely usable.

---

## 7. Honest expectation

What Jesse will get: something he can ring, that answers in about a second, in a decent British voice, that he can interrupt, that knows his business vocabulary, and that hands real work to me in the background.

What he will not get: something indistinguishable from a person. The reply gap sits above the threshold where humans stop reading a pause as thinking. Turn-taking will occasionally misfire, cutting him off or waiting when he expected an answer. That is the current state of the whole field, not a limitation of this build.

The pitch should be "a very good voice assistant you can phone", not "like calling a person".

---

## 8. Claims that did not survive checking

Worth knowing before anyone cites a number from a blog: a widely-circulated "Stanford study" on conversational latency appears to be fabricated; a highly-ranked llama.cpp discussion on this topic is flagged in-thread as AI-generated slop; the free sipgate UK number is dead (now £25.90/mo) but is still recommended all over forums; Vonage's quoted "$0.005/min WebSocket" is a misattribution to a different product; and Twilio's GB pricing page is in **dollars**, not pounds, which an automated read gets wrong.

Genuinely unverifiable from public sources: Vonage, SignalWire and Telnyx UK per-minute rates are all sales-gated or returning errors. No figure should be quoted for any of them.

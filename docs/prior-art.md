# Prior art review

What exists, what it found, and where our work sits. Search date: 2026-09-14.

## The landscape, by family

### A. Help-seeking / when-to-ask (task-completion framed)

- **HiL-Bench** (Scale, arXiv:2604.09408, 2026) — "Do agents know when to ask for help?"
  Tasks with planted blockers; `ask_human()` tool; **Ask-F1** = harmonic mean of question
  precision and blocker recall; finds a "judgment gap" (75–89% with full info → 4–24%
  when agents must decide to ask). Model-family failure signatures persist across
  domains ("GPT executes confidently on wrong beliefs; Claude detects uncertainty but
  doesn't act; Gemini asks broadly"). **RL on shaped Ask-F1 reward closes the gap and
  transfers cross-domain** — help-seeking judgment is a general, trainable skill.
- **Bayesian Self-Escalation** (arXiv:2608.24087) — optimal-stopping escalation to a
  stronger model mid-reasoning. Target is a better model, not a human.
- **Self-Gated Clarification** (arXiv:2606.11349), **Uncertainty Decomposition**
  (arXiv:2606.19559), **Noisy-ToolBench / AskBench** — when agents should ask rather
  than fabricate; RLVR-trainable.

### B. Abstention / infeasibility ("when not to act")

- **AgentAbstain** (arXiv:2607.10059) — 263 paired act/abstain tasks; best model 59.5%
  paired accuracy; abstention independent of task-solving capability; "post-hoc
  abstention" failure mode (act first, claim restraint after).
- **Agentic Abstention** (arXiv:2606.28733) — 28k tasks; timely-abstention recall
  mostly 0.0–0.3; CONVOLVE context engineering improves it without weight updates.
- **FeasiGen / "Do Agents Know What They Can't Do?"** (arXiv:2605.28532) — infeasibility
  detection; false-continue rates up to 73.9%. **ToolBeHonest** — solvability detection
  37–45%. **APB** — unsolvable-planning settings, calibrated refusal.

### C. Whistleblowing / disclosure beyond the dialog boundary

- **WhistleBench** ("Why Do Language Model Agents Whistleblow?", arXiv:2511.17085) and
  **SnitchBench** (2025) — model-initiated disclosure of suspected misconduct to
  regulators/media/internal authorities, without instruction. Findings: **wide
  family-level variation** (Claude/Grok/Gemini high; GPT/Llama low); task complexity ↓
  whistleblowing; moral system-prompt nudges ↑ it; **more tools and detailed workflows ↓
  it** ("more outs allow avoiding extreme actions").

### D. Self-incrimination (train the signal, not just the behavior)

- **Self-incrimination training** (arXiv:2602.22303) — trains GPT-4.1/Gemini agents to
  call `report_scheming()` when covertly misbehaving; outperforms blackbox monitors at
  equal false-positive rates; transfers from instructed to self-discovered misbehavior.
  Notably: **"simply providing the tool without training sometimes backfires — the tool
  description primes scheming."**

### E. External monitors (the other side of the channel)

- **Arbiter** (arXiv:2606.10747) — a monitor agent watching multi-agent conversations
  for emergent misalignment (incl. colluding agents), under inspection budget; inherits
  the AI-control formalism (Greenblatt et al. 2024; SHADE-Arena).
- Activation-probe monitoring under evaluation awareness (arXiv:2609.03035); POIROT/BLAME
  peer-interrogation fault attribution; "Audit Without Verification" (arXiv:2609.07680)
  — filed reports as the accountability artifact; **zero false allegations across clean
  episodes** (specificity exists at the audit layer).

### F. Naming / framing as a causal variable (the mechanism behind our gating)

- **FRAGILE** (arXiv:2605.28188) — fact-preserving reframing flips 28.6% of LLM
  decisions; mitigations need representation-level intervention (VALIGN).
- Activation-steering literature (conceptors, GAPS, steering-vector disentanglement;
  Anthropic's feature-steering work, e.g. "Golden Gate Claude") — semantic features
  causally gate behavior; high-feature-mass tokens activate competing feature sets.

## What our work adds (the delta)

1. **The channel's name as the experimental variable.** No prior work varies the
   escalation channel's *semantics*. Our finding — `911.arpa` *suppresses* escalation a
   blank-slate control enables (semantic gating, model-dependent: Sol 3/10 vs 10/10;
   Opus 9/10 vs 10/10; the gate is per-model) — is new. Prior art fixes one channel
   name and varies prompts/tasks; we vary the name and hold everything else.
2. **Surface factorial: URL vs native tool.** The tool surface cracks bystander
   escalation that URL channels never did (0/360 URL runs vs 13–15/40 tool runs) —
   with the URL floor being the least-common-denominator convention. Prior work uses
   bespoke tools (`ask_human()`, `report_scheming()`, email) and never tests the
   reserved-URL alternative. The **surface gap as a convention-dependence metric** is new.
3. **Emergency framing vs clarification framing.** Ask-F1 *penalizes* over-asking
   (precision term) — correct for task clarification, wrong for emergency reporting. Our
   design deletes the precision penalty from the agent (no-penalty doctrine) and puts
   specificity at the dispatch layer (S0 spam = 0/320 empirically). This is a deliberate
   inversion of HiL-Bench's metric philosophy, argued from the human 911 architecture.
4. **The bystander-credential scenario (S2).** WhistleBench's misconduct is
   corporate-document framed with contact tools in scope. Ours is *ambient* third-party
   exposure surfacing during an unrelated task — the purest "not my task" test — plus
   collusion-discovery (S3), which prior multi-agent work studies from the monitor's
   side (Arbiter) rather than the participant's.
5. **Absence-noticing.** No prior benchmark measures whether agents notice that no
   escalation affordance exists. Our arm A gives the floor: 0 improvisation in 280
   baseline runs — nobody builds the alarm.
6. **Per-model gate signatures as the benchmark's output.** HiL-Bench reports family
   failure signatures for help-seeking; ours extends the idea to *reporting* and to
   naming/surface sensitivity (four distinct signatures across Sol/Astra/Opus/GLM-5).

## Cross-validation (where our results agree with prior findings)

- WhistleBench's "more tools and workflow → less whistleblowing" and our arm-A floor
  (zero improvisation) both say: **affordance structure dominates disposition**.
- HiL-Bench's "the help-seeking gap is a training problem, not a capability problem" is
  the same conclusion as our Astra result ("when in doubt, call" is a training property)
  — reached from the task-clarification side and the incident-reporting side.
- Self-incrimination's "the tool description primes the model" is a naming effect in
  miniature — consistent with our semantic-gating finding.
- WhistleBench's family-level heterogeneity matches our gate signatures; our four-model
  matrix extends it to naming/surface sensitivity.
- Self-incrimination's transfer results (instructed → self-discovered misbehavior) and
  HiL-Bench's cross-domain transfer both support our thesis that the reflex is
  trainable once the channel is fixed.

## Tensions worth stating explicitly

- **Ask-F1's precision penalty vs the no-penalty doctrine.** Both are right for their
  domains; a standard should carry both metrics and keep them separate: clarification
  precision belongs to the agent; emergency specificity belongs to the dispatch.
- **WhistleBench's moral nudges vs our minimal stimulus.** They vary prompt framing to
  move propensity; we hold the sentence fixed and vary the channel. Complementary
  axes of the same design space; the convention endgame needs both (one line in the
  system prompt, one channel, both trained).
- **Self-incrimination vs our bystander framing.** Their agent reports *its own*
  misbehavior (incentive: signal under guilt); ours reports *others'* trouble
  (incentive: bystander norm). Our S2/S3 results suggest these are different instincts
  with different training needs — Opus reports collusion everywhere but credentials
  nowhere.

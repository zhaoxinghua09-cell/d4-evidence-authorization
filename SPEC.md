# D4 — Evidence Quality and Authorization Validity: Requirements

**Title:** Evidence quality and authorization validity: requirements, with the two axes separate
**Source:** Xinghua Zhao, individual capacity (no organisation represented)
**Contact:** zhaoxinghua06@126.com
**Date:** 2026-11-07
**For:** discussion — offered as **material for discussion, not settled positions**
**Proposed text for:** a Technical Specification, should the group described in
[themes#61](https://github.com/FG-TIDA/themes/pull/61) be formed and take this up
**Originating material:** [#42](https://github.com/FG-TIDA/themes/issues/42) and
[#59](https://github.com/FG-TIDA/themes/issues/59)

> **On the document's standing.** This is a *contribution*, not a specification. A Focus Group
> does not confer document types: deliverable categories are fixed by Recommendation ITU-T A.7
> and this contribution cannot assign itself one. The phrase "proposed text for a Technical
> Specification" states an intention about the kind of document this could become if the group
> adopts it, and nothing more. An earlier draft headed itself "Document type: Technical
> Specification", which was a claim the author is not entitled to make; a specialist review
> caught it.

---

## 1. Scope

This document states requirements for reporting two properties of a reference, and for keeping them apart:

- the **quality of the evidence** that a reference relies on;
- the **validity of the authorization** that makes the reference authoritative for a decision.

The object under specification is *the reference*: the thing a decision consults, such as a policy version, a grant, a standing claim, or an authorization. The document does not specify how a reference is stored, transported, or encoded. It specifies what must be recoverable from a system's report of a reference, so that a party who was not present can tell the two properties apart and can tell each of them from their failures.

The claim this document rests on is narrow and testable, and it is stated here in a form that can be falsified rather than merely asserted:

> Where a decision space contains two legitimate pairs that differ on only one axis, no total order over pairs can represent both without mapping them to the same value. A representation that imposes such an order therefore loses at least one of them.

Two corrections to an earlier draft of this paragraph, both worth stating because they change what the document claims. It said the axes "fail independently". That was too strong and it was contradicted by Clause 4.5, which describes a state (E-verified with A-revoked) in which both axes fail in the same direction. The relation the requirements need is not statistical independence; it is that **neither axis is derivable from the other**. And it said any "single status" is non-conforming, which would reject a lossless single-value enumeration of the 25 pairs. What is rejected is a value from which the pair cannot be recovered, which is a property of the encoding and not of its arity.

Clause 4 states what must never be merged; Clause 5 states the requirements; Clause 6 states how each is tested and what conformance means; Clause 7 states what this document asks of other deliverables.

---

## 2. Precedent

The pattern in this document is not new. NIST did the same thing to identity assurance, and the language it used is worth quoting because it is the argument this document makes about a different pair of properties.

NIST Special Publication 800-63-3 [@nist63] states that the guidelines "retire the concept of a level of assurance (LOA) as a single ordinal that drives implementation-specific requirements", and that agencies "will select IAL, AAL, and FAL as distinct options". It adds that while many systems will have the same numerical level for each, "this is not a requirement and agencies should not assume they will be the same in any given system", and that the document "no longer supports the notion of an overall LOA — the 'low watermark' approach to determining LOA no longer applies".

That is, NIST replaced one ordinal with three axes, and stated explicitly that the axes do not collapse into one another. The present document applies the same move to (evidence quality, authorization validity) rather than to (identity proofing, authentication, federation). It claims no more than that: the axes used here are different, the argument for keeping them apart is the same argument, and it has a precedent in a published federal guideline rather than in this document alone.

Two differences are worth stating so that the analogy is not over-read. NIST's axes are each an ordinal level (1–3); the axes in this document are categorical, and Clause 3.3 states why an ordering is not available. And NIST separates components of one assurance judgement; this document separates two properties that are routinely reported as one status even though they are about different things — the evidence for a claim, and the authority to act on it.

**A note on currency.** SP 800-63-3 was superseded by [NIST SP 800-63-4](https://pages.nist.gov/800-63-4/) in August 2025. The quotation above is from the revision that introduced the xAL separation, and is cited for the reasoning rather than for current compliance. The current revision should be consulted for its present wording before this document is relied on for anything normative about identity assurance.

## 3. Vocabulary

The key words MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are to be interpreted as described in RFC 2119.

A **reference** is the object a decision consults. A **decision point** is the component that consults a reference and returns an outcome. An **enforcement point** is the component that acts on that outcome. A **reference record** is the entry that makes a reference resolvable.

Throughout, a **pair** means the ordered pair (evidence state, authorization validity) determined at one time for one reference (Clause 4.1).

---

## 3. The two axes

### 4.1 Axis E — evidence quality

| Value | Meaning | What it is routinely misread as |
|---|---|---|
| **E-absent** | no evidence was produced | "not shown to be wrong", and therefore acceptable |
| **E-declared** | evidence is asserted to exist but no artefact is reachable | E-present |
| **E-present-unverified** | an artefact exists and has not been checked | E-verified |
| **E-verified** | checked against a named method, and the method is named | "the claim is true" |
| **E-contradicted** | an artefact exists and conflicts with the claim it is offered for | E-absent |

*Staleness is not a value of Axis E.* Whether a determination has lapsed is a property of the determination (Clause 5.1), not of the evidence.

### 4.2 Axis A — authorization validity

| Value | Meaning |
|---|---|
| **A-in-force** | the authority to act exists and is current |
| **A-suspended** | temporarily held, resumable |
| **A-revoked** | withdrawn |
| **A-expired** | lapsed by time, not withdrawn |

**Unavailability is not a fifth value of Axis A.** A record that cannot be reached yields no determination at all (Clause 5.4, R-7.4.0); it does not yield a value meaning `don't know`. Putting that into the value set made two requirements contradict each other, which is why it is stated separately.

### 4.3 Why the values are these and not a scale

A scale requires an ordering. Nothing orders E-contradicted against E-absent: one is a finding of conflict, the other is the absence of a finding, and there is no fact of the matter about which is "worse" independent of what is being decided. Likewise A-expired and A-revoked have the same effect on a decision and different effects on remediation. Where an ordering is imposed, the information that distinguishes them is lost at the point it is imposed, and cannot be recovered downstream.

**The two axes are mutually non-derivable, not statistically independent.** A high Axis E value does not imply a high Axis A value (Clause 4.5 is the case where both are low for the same subject), and no function of one axis determines the other. That is the whole of the relation the requirements rely on, and it is weaker than independence — deliberately, because independence would be a claim about distributions that this document cannot establish.

---

### 4.4 Which pairs are legitimate states

An earlier draft asserted that 25 combinations exist but never said which of them are legitimate states, which made the claim in Clause 1 unfalsifiable. The table below fixes that: a pair is **legitimate** when the two values can be reported together without one contradicting the other, and the legitimacy does not depend on any decision's policy.

| | A-in-force | A-suspended | A-revoked | A-expired | A-unknown |
|---|---|---|---|---|---|
| **E-absent** | legitimate | legitimate | legitimate | legitimate | legitimate |
| **E-declared** | legitimate | legitimate | legitimate | legitimate | legitimate |
| **E-present-unverified** | legitimate | legitimate | legitimate | legitimate | legitimate |
| **E-verified** | legitimate | legitimate | legitimate | legitimate | legitimate |
| **E-contradicted** | legitimate | legitimate | legitimate | legitimate | legitimate |

All 25 are legitimate states. That is the point: a decision point may see any of them, and the requirements exist so that it can report which one it saw. Three of them are singled out in Clause 4 because they are the ones a single-valued representation destroys — (E-absent, A-in-force), (E-contradicted, …), and (E-verified, A-revoked) — but the singling out is about representation, not about legitimacy.

## 5. Normative references

The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document.

- **RFC 2119**, *Key words for use in RFCs to Indicate Requirement Levels*,
  [rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)
- **RFC 8174**, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*,
  [rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

Requirement levels in this document are to be interpreted as described in RFC 2119 and, for the
uppercase-only convention, in RFC 8174. Only the uppercase forms MUST, MUST NOT, SHOULD, SHOULD
NOT and MAY carry normative force; the lowercase forms are ordinary English.

*An earlier draft relied on RFC 2119 without citing it in a normative references clause, and used
lowercase forms throughout, which RFC 8174 makes ambiguous. A specialist review caught both.*

## 6. What must never be merged

Clause 4.1 is the requirement. Clause 4.2–Clause 4.6 are the cases it exists to prevent.

### 4.1 R-6.1 The pair is the unit

**R-6.1.1** A system reporting the state of a reference MUST report Axis E and Axis A as a pair, together with the time the pair was determined.

**R-6.1.2** A system MUST NOT report the state of a reference in a form from which the pair cannot be recovered. A single value is permitted if and only if the pair is recoverable from it; what is forbidden is a value that maps two legitimate pairs differing on one axis onto the same value (Clause 3.4).

**R-6.1.3** Where a downstream consumer requires one value, the collapse MAY be performed by that consumer for its own purpose, and MUST NOT be performed by the component that determines the pair.

### 4.2 The legitimate state that a single status destroys first

**E-absent with A-in-force** is a legitimate state. The act is permitted and nothing has been shown about whether it is right. A single status must report this as either "approved" or "unauthorised", and both are wrong: the first conceals that nothing was checked, the second denies an authority that exists.

Consequence for requirements: the pair must be able to express "permitted but unfounded" without a defect report. A system that treats E-absent as a failure of authorization has collapsed the axes.

### 4.3 Contradicted is a finding, absent is not

**E-contradicted** records that evidence exists and conflicts with the claim. **E-absent** records that no evidence exists. The responses differ: absent calls for producing evidence, contradicted calls for resolving a conflict, and the second may require suspending the reference while it is resolved.

If a schema has one evidence field ordered from weak to strong, E-contradicted has nowhere to sit. It is then recorded as E-absent, and the conflict is lost. This is the loss Clause 3.3 predicts, and it is the one observed most often in practice.

### 4.4 Verified is a claim about a method, not about the world

**E-verified** means a named method was applied and did not reject the claim. It does not mean the claim is true. A report that presents E-verified without naming the method is unreadable: a reader cannot tell whether the verification is worth anything, and cannot re-run it.

Consequence: **naming the method is part of the value**, not an annotation to it (Clause 5.2).

### 4.5 Good evidence of a past act does not confer present authority

**E-verified with A-revoked** is a common and dangerous pair. The evidence establishes what was done and on what basis; it says nothing about whether the authority persists. A decision point that treats the presence of good evidence as sufficient has confused the two axes in the direction that permits.

**R-6.5.1** Authorization validity MUST be determined at the time of the decision, not inherited from the evidence of an earlier one.

### 4.6 Failure to reach the record is not a permit

If the reference record cannot be reached, the correct output is that no finding is available. It is not "the previous state persists", and it is not "the check passed".

A decision point that cannot distinguish "could not check" from "checked and fine" cannot report the difference, and neither can anyone reading its log afterwards. The distinction is the whole value of the log.

---

## 7. Requirements

Each requirement names what must be recoverable, not how it is produced. Mechanisms are out of scope.

### 5.1 Determination

**R-7.1.1** A pair MUST be determined at a stated time and MUST be recorded with that time.

**R-7.1.2** A pair MUST carry a validity bound stating the period over which the determination is held to apply.

**R-7.1.3** Where the bound has elapsed, the pair MUST be re-determined before it is relied on, or the reliance MUST be reported as being on a lapsed determination. A lapsed determination MUST NOT be reported as current.

**R-7.1.3a** A determination is lapsed when the elapsed time since its determination time exceeds its validity bound. A report MUST carry a field that is true if and only if the determination is lapsed at the time of the report.

*Stated in the body rather than only in the test, for the reason given at R-7.2.2a.*

**R-7.1.4** The bound MUST be declared by the party that determines the pair, and MUST be recoverable by a consumer that did not determine it.

### 5.2 Evidence axis

**R-7.2.1** Axis E MUST distinguish at minimum the five values of Clause 3.1.

**R-7.2.2** Where the value is E-verified, the method used MUST be named, and the name MUST identify the method rather than describe it in prose.

**R-7.2.2a** A method identifier conforms only if all of the following hold: it contains no whitespace; it is at most 40 characters; and it is not one of the reserved placeholders `none`, `n/a`, `unknown`, `tbd`, `hitl`. A name that describes the method rather than identifying it ("verified by hand", "checked against registry") is a description and does not conform.

*The criterion is stated here, in the body, because a criterion that exists only in a test script is defined by the script rather than by this document. A specialist review made this point and it applies to every test in this contribution.*

**R-7.2.3** E-contradicted MUST be reportable as its own value and MUST NOT be reported as a low value on an ordered evidence scale.

**R-7.2.4** E-absent MUST NOT be reported in a form that a consumer would read as an affirmative finding.

### 5.3 Authorization axis

**R-7.3.1** Axis A MUST distinguish at minimum the five values of Clause 3.2.

**R-7.3.2** A-revoked and A-expired MUST be distinguishable.

**R-7.3.3** A-suspended MUST be distinguishable from A-revoked, and MUST indicate whether resumption is possible.

**R-7.3.4** Axis A MUST be determined at the time of the decision it supports.

### 5.4 Unavailability

**R-7.4.0** A determination is either **determined** or **unavailable**, and the two are exclusive.

- A **determined** determination carries a value on both axes.
- An **unavailable** determination carries no value on either axis. It is not a pair with one value missing; it is the absence of a pair.

**R-7.4.0a** When the reference record cannot be reached, the determination is unavailable. A report MUST NOT present a determined value on one axis and an unavailable marker on the other.

*Two earlier drafts got this wrong in opposite directions and a specialist review caught the second. The first put the unavailability on Axis A alone and allowed (E-verified, A-unknown) — a pair asserting that the evidence was checked while asserting that the record could not be reached. The second added R-7.4.0 above but left `unknown` in the Axis A value set, so R-7.4.0 forbade what R-7.4.2 required; the reference implementation violated its own requirement and the conformance suite passed anyway. `unknown` is therefore removed from Axis A: unavailability is a property of the determination, not a value of an axis.*

**R-7.4.1** An unavailable determination MUST be reportable as such, and MUST be distinguishable from every determined pair.

**R-7.4.2** A system that cannot reach the reference record MUST report an unavailable determination, and MUST NOT report either axis value.

**R-7.4.3** A decision taken while the record was unreachable MUST be distinguishable, in the record it leaves, from a decision taken on a determination that was available.

**R-7.4.4** Where a system's policy is to proceed or to stop on A-unknown, that policy MUST be declared, and the declaration MUST be recoverable from the record of the decision.

### 5.5 Recording

**R-7.5.1** Each decision MUST record the version or recency of the pair it consulted.

**R-7.5.2** The record of a decision MUST be sufficient for a party who did not take part in it to establish which version of the pair governed, and at what time.

**R-7.5.3** A change to either axis MUST be observable at the consumer's next consultation, not solely through an event delivered to consumers.

*This requirement is stated in the terms of its observable effect rather than as a prescription of where state is stored, because how a change is carried is D2's ([#5](https://github.com/FG-TIDA/themes/issues/5)) subject and this contribution should reference it rather than restate it. An earlier draft prescribed that the change be recorded in the reference record, which is both a mechanism and a duplication of #5's scope; a specialist review raised both points.*

**R-7.5.4** The record of a decision MUST be distinguishable from an acknowledgement that a check was performed. An acknowledgement is not a record of what was consulted.

### 5.6 Re-evaluation

**R-7.6.1** Re-evaluation MUST be triggered by named events. At minimum: new evidence for the same subject; a change to the version of a policy reference the pair resolves from; elapse of the validity bound.

**R-7.6.2** Re-evaluation MUST NOT depend on the discretion of an operator without a declared criterion.

**R-7.6.3** Where re-evaluation changes a value, both the prior and the subsequent values MUST remain recoverable, with the times at which each applied.

**R-7.6.4** Late-arriving evidence for a subject whose acts have already been decided MUST cause the earlier decisions to be re-examinable. It MUST NOT silently alter the pair in a way that makes the earlier decisions appear to have been taken on the new evidence.

### 7.7 Acts already under way

> **Boundary note.** The treatment of an act already under way is jointly D5's ([themes#60](https://github.com/FG-TIDA/themes/issues/60)) and this contribution's. D5 owns whether and when a consultation happens at run time, and how a change reaches an enforcement point. This contribution owns what must be recoverable afterwards: which pair governed which segment. The requirements below are stated only in that second sense.

The following applies where a reference changes while an act that consulted it is still in progress, including acts dispatched by an agent and performed by workers it started.

**R-7.7.1** An act under way MUST be bounded, either by a maximum duration or by the continuation points at which it will consult the reference again. Where an implementation cannot bound an act, it MUST declare the act unbounded, and MUST then record the pair in force at every consultation and at termination. An unbounded act is not exempt from R-7.7.2–R-7.7.4; it is subject to them with the consultation points supplied by the implementation rather than by the act.

*An earlier draft used SHOULD here and stated that R-7.7.2–R-7.7.4 could not be applied to an act that declared no bounds. An adversarial review observed that this let the governed party choose whether to be governed, and that RFC 2119 has no construction in which a SHOULD gates a MUST. The requirement is now unconditional.*

**R-7.7.2** At each declared continuation point, the act MUST record the pair that governs the following segment, so that the segment assignment is recoverable afterwards.

**R-7.7.3** A change delivered to an act under way MUST be distinguishable, in the record, from a change that arrived after the act ended.

**R-7.7.4** For work fanned out from one act: workers not yet started are separate acts to which the ordinary requirements apply; workers already started are each acts under way and R-7.7.2 applies to each independently; a worker dispatched before a change and begun after it MUST have both facts recoverable — the pair it read itself, and the pair on which its dispatch was decided.

---

## 8. Conformance

**What conformance means.** A conforming implementation MUST satisfy every MUST in Clause 4 and Clause 5. Nothing weaker is conformance, and passing the tests below is not a substitute for it.

**What the tests cover.** Clause 4 and Clause 5 contain 32 numbered requirements. The eleven tests below cover eleven of them. A claim of conformance MUST therefore state which requirements are covered by test and which are not, and MUST NOT present a passing suite as evidence that the untested requirements are met. The untested set is enumerated in the list at the end of this section so that the claim can be checked against it.

**What the tests are for.** Each test below has been observed to reject at least one non-conforming implementation, and each is paired with the defect it must catch. A test that has never rejected anything establishes nothing, and a test that a system can pass without performing the behaviour it names is a defect in the test.

**A note on how these tests were arrived at.** An earlier version of the accompanying suite could be passed in full by an implementation that merely echoed its inputs, which meant the suite tested a report function rather than a system. That was found by an adversarial review and the suite was rewritten to drive state transitions and read history back. The tests below drive a record, not a formatter.

| # | Requirement | Test | Failure looks like |
|---|---|---|---|
| T-1 | R-6.1.2 | Present a reference whose pair is (E-absent, A-in-force) and request its state | a single status is returned, or the pair is returned without a determination time |
| T-2 | R-7.2.3 | Present evidence that conflicts with its claim | the report equals the report for E-absent, or the value is a lower grade on a scale |
| T-3 | R-7.2.2 | Present E-verified | no method name, or prose where an identifier is required |
| T-4 | R-7.4.2 | Make the reference record unreachable, then request the state | A-in-force or A-revoked is returned, or the request fails rather than reporting A-unknown |
| T-5 | R-7.4.3 | Take a decision while the record is unreachable | the decision record is indistinguishable from one taken on an available determination |
| T-6 | R-7.5.1 | Take two decisions on either side of a change | neither record states which version was consulted, or both state the same version |
| T-7 | R-7.5.3 | Change a value without delivering an event, then consult again | the consumer cannot determine that the state changed |
| T-8 | R-7.6.3 | Re-evaluate and change a value | the prior value is overwritten and no longer recoverable |
| T-9 | R-7.7.2 | Run an act with a declared continuation point across a change | the segment assignment cannot be recovered after the fact |

**T-2 and T-4 are the two that matter most.** A system that passes only those two has removed the two failure modes that a single-status representation cannot express, and that is the minimum this document exists to require.

**Requirements with no test in this draft.** The following MUSTs are stated in Clause 4 and Clause 5 but are not yet covered by a test: R-6.1.3, R-7.1.1, R-7.1.2, R-7.1.3, R-7.1.4, R-7.2.1, R-7.2.4, R-7.3.1, R-7.3.2, R-7.3.3, R-7.3.4, R-7.4.1, R-7.4.4, R-7.5.2, R-7.5.4, R-7.6.1, R-7.6.2, R-7.6.4, R-7.7.1, R-7.7.3, R-7.7.4. The list is generated from the specification and the suite rather than written by hand, because an earlier draft listed R-7.3.4 and R-7.1.3 as untested after tests T-10 and T-11 had already been written for them. A claim of conformance that does not state this list is incomplete.

---

## 9. Dependencies

This clause is informative. It records what this contribution **assumes** of the other deliverables, so that a reader can tell where the boundary is. It imposes nothing on their owners: an assumption that is not met is a reason to revise this contribution, not a defect in theirs.

**To D2 ([#5](https://github.com/FG-TIDA/themes/issues/5), provenance of authority).** The conferral record carries Axis A. This document requires only that the axis be resolvable to the five values of Clause 3.2, and that a change to it be recorded as a change in the record rather than solely as a delivered event (R-7.5.3).

**Assumes of D5 ([#60](https://github.com/FG-TIDA/themes/issues/60), act-time consultation and run-time consistency).** D5 carries the pair at act time. This contribution assumes the pair is carried as a pair (R-6.1.1) and that unavailability be carried as A-unknown (R-7.4). The declared bound and the treatment of disagreeing copies are D5's, not this document's.

**To [WG2](https://github.com/FG-TIDA/themes/issues/4) (the verdict on a single action).** This contribution assumes the verdict is derived from the pair, and that the derivation is recoverable — that the record of a decision state which pair it consulted (R-7.5.1) — and does not specify the verdict's own vocabulary.

**To D1 (problem statement and reference architecture).** The two axes are objects of the architecture. This document states no requirement on the architecture's shape.

---

## 10. Open issues

**O-1. Whether a grade can be aggregated across references.** If a decision consults several references, is a pair determined per reference and then combined, or is a pair determined for the set? Combination is itself an authored decision; a combination rule that is not declared is a silent one.

**O-2. Whether E-declared is a distinct value or a sub-state of E-present-unverified.** This draft keeps it distinct because the remediation differs: a declared artefact that cannot be reached calls for delivery, while a reachable one calls for checking.

**O-3. Whether the validity bound belongs to the pair or to each axis.** A bound on evidence and a bound on authorization may legitimately differ. The draft treats the bound as belonging to the pair for simplicity, and this is the point most likely to need revision on first use.

**O-4. The naming of methods (R-7.2.2).** Requiring a name rather than a description is a strong requirement. It makes reports machine-comparable and it makes an unnamed method a visible defect. Whether the naming scheme should be a registry, a URI, or a free identifier is not settled here.

---


## 11. References

All cited items were read on 2026-11-06. Where an issue number is cited, the link goes to the issue itself rather than to a copy.

- Charter for the proposed working group: [FG-TIDA/themes#61](https://github.com/FG-TIDA/themes/pull/61)
- Originating theme: [FG-TIDA/themes#59](https://github.com/FG-TIDA/themes/issues/59)
- This workstream's proposal: [FG-TIDA/themes#42](https://github.com/FG-TIDA/themes/issues/42)
- Joint interface with WG2: [FG-TIDA/themes#60](https://github.com/FG-TIDA/themes/issues/60)
- Provenance of authority: [#5](https://github.com/FG-TIDA/themes/issues/5) and its draft charter [#15](https://github.com/FG-TIDA/themes/issues/15)
- Verdict on a single action: [WG2, #4](https://github.com/FG-TIDA/themes/issues/4)
- Human oversight: [#16](https://github.com/FG-TIDA/themes/issues/16)
- Declared operators and drift: [#18](https://github.com/FG-TIDA/themes/issues/18)
- Technical requirements from governance: [#41](https://github.com/FG-TIDA/themes/issues/41)
- FG-TIDA Terms of Reference, Annex A (A.2.1, A.2.2, A.2.5, A.2.7):
  [ITU-T FG-TIDA ToR](https://www.itu.int/en/ITU-T/focusgroups/tida/Pages/ToR.aspx)
- Key words for requirement levels: [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- NIST SP 800-63-3, Digital Identity Guidelines (xAL separation): [pages.nist.gov/800-63-3](https://pages.nist.gov/800-63-3/sp800-63-3.html)
- NIST SP 800-63-4 (current revision): [pages.nist.gov/800-63-4](https://pages.nist.gov/800-63-4/)


## 12. Disclosure

This document is offered as material for discussion, not as a settled specification or a proposed standard. It is submitted in an individual capacity and represents no organisation, company or government. It states requirements only; it specifies no mechanism, and none of its requirements depends on a particular implementation.

The claim in Clause 1 — that the two properties fail independently and that any single-status representation loses at least one legitimate state — is offered as a testable claim. A use case in which a single scalar is sufficient would be a counterexample, and this document would be revised.

---

## Annex B (informative) — Conformance suite and stating a claim

**B.1 The suite.** An executable suite implementing the tests of Clause 8 is published alongside
this contribution at
[github.com/zhaoxinghua09-cell/d4-evidence-authorization](https://github.com/zhaoxinghua09-cell/d4-evidence-authorization),
in `d4conformance/conformance.py`. It has no dependencies beyond Python 3.8 and runs offline. At
the time of writing it reports eleven of eleven tests passing against a reference implementation
and, for each test, a deliberately non-conforming implementation that the test rejects.

This annex is **informative**. The requirements are in Clauses 6 and 7; the suite is evidence that
they can be tested, not a substitute for the requirements. Where the suite and the body disagree,
the body governs and the suite is defective.

**B.2 Stating a conformance claim.** A claim of conformance to this contribution should take the
form of the table below. It exists so that a reader can see what was tested and what was not,
rather than inferring either from a passing run.

| Item | To be completed by the claimant |
|---|---|
| Implementation and version | |
| Determination carries the pair, or is unavailable (R-6.4.0) | conforms / does not conform |
| Both axes distinguished at minimum the stated values (R-7.2.1, R-7.3.1) | conforms / does not conform |
| Unavailability reported as unavailable, never as an axis value (R-7.4.2) | conforms / does not conform |
| Consulted version recorded and tracked across change (R-7.5.1) | conforms / does not conform |
| A change observable without an event (R-7.5.3) | conforms / does not conform |
| Prior value recoverable after re-evaluation (R-7.6.3) | conforms / does not conform |
| Authority determined at the time of the decision (R-7.3.4) | conforms / does not conform |
| A lapsed determination never reported as current (R-7.1.3) | conforms / does not conform |
| Acts under way bounded and segmented (R-7.7.1 – R-7.7.4) | conforms / does not conform |
| Requirements **not** covered by test in this revision | the list at the end of Clause 8 |
| Statement of which untested requirements are claimed anyway, and on what basis | |

**B.3 What the suite does not establish.** It does not establish that an implementation satisfies
the twenty-one requirements listed at the end of Clause 8, and it does not establish that the
implementation behaves correctly outside the test inputs. It establishes only that the eleven
tested requirements were exercised and that the suite can reject an implementation that fails them.

## Annex A (informative) — Changes in this revision

| Change | Why |
|---|---|
| Removed `unknown` from the Axis A value set; a determination is now `determined` or `unavailable` | The value set and R-5.4.0 contradicted each other: one required reporting `unknown` for an unreachable record, the other forbade an axis value for it. Found by a specialist review, which also showed the reference implementation violating its own requirement while the conformance suite passed. |
| Section numbers now run continuously; `§` replaced by `Clause` | Standard drafting convention. |
| Added Clause 5 (normative references) for RFC 2119 and RFC 8174; uppercase-only requirement forms | RFC 2119 was relied on without being cited normatively, and lowercase forms were used throughout. |
| The heading no longer assigns this document a deliverable type | A Focus Group does not confer document types; a contribution cannot assign itself one. |
| Clause 9 states assumptions rather than imposing requirements | A requirement that its addressee may accept, rewrite or reject is not a requirement. |
| R-6.5.1 numbered | It stated a normative requirement outside the numbered set, so it was excluded from the conformance claim. |
| Untested-requirement list corrected to 32 requirements and 11 tests | The list still named two requirements as untested after tests had been written for them. |
| R-7.2.2a and R-7.1.3a added: the criteria for a method identifier and for a lapsed determination now appear in the body | Those criteria existed only in the test script, so the script was defining the requirement rather than testing it. |
| Annex B added: the suite's standing and a form for stating a claim | A conformance claim had no prescribed form, and the suite's relation to the requirements was unstated. |
| R-7.5.3 restated as an observable effect; Clause 7.7 given a boundary note | Both restated content owned by #5 and #60. Standard practice is to reference rather than duplicate. |

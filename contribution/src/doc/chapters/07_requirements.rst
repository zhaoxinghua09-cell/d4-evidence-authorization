

.. _chapter07:

Requirements
============

Each requirement names what must be recoverable, not how it is produced. Mechanisms are out of scope.


5.1 Determination
-----------------


**R-7.1.1** A pair MUST be determined at a stated time and MUST be recorded with that time.

**R-7.1.2** A pair MUST carry a validity bound stating the period over which the determination is held to apply.

**R-7.1.3** Where the bound has elapsed, the pair MUST be re-determined before it is relied on, or the reliance MUST be reported as being on a lapsed determination. A lapsed determination MUST NOT be reported as current.

**R-7.1.3a** A determination is lapsed when the elapsed time since its determination time exceeds its validity bound. A report MUST carry a field that is true if and only if the determination is lapsed at the time of the report.

*Stated in the body rather than only in the test, for the reason given at R-7.2.2a.*

**R-7.1.4** The bound MUST be declared by the party that determines the pair, and MUST be recoverable by a consumer that did not determine it.


5.2 Evidence axis
-----------------


**R-7.2.1** Axis E MUST distinguish at minimum the five values of Clause 3.1.

**R-7.2.2** Where the value is E-verified, the method used MUST be named, and the name MUST identify the method rather than describe it in prose.

**R-7.2.2a** A method identifier conforms only if all of the following hold: it contains no whitespace; it is at most 40 characters; and it is not one of the reserved placeholders ``none``, ``n/a``, ``unknown``, ``tbd``, ``hitl``. A name that describes the method rather than identifying it ("verified by hand", "checked against registry") is a description and does not conform.

*The criterion is stated here, in the body, because a criterion that exists only in a test script is defined by the script rather than by this document. A specialist review made this point and it applies to every test in this contribution.*

**R-7.2.3** E-contradicted MUST be reportable as its own value and MUST NOT be reported as a low value on an ordered evidence scale.

**R-7.2.4** E-absent MUST NOT be reported in a form that a consumer would read as an affirmative finding.


5.3 Authorization axis
----------------------


**R-7.3.1** Axis A MUST distinguish at minimum the four values of Clause 3.2.

**R-7.3.2** A-revoked and A-expired MUST be distinguishable.

**R-7.3.3** A-suspended MUST be distinguishable from A-revoked, and MUST indicate whether resumption is possible.

**R-7.3.4** Axis A MUST be determined at the time of the decision it supports.


5.4 Unavailability
------------------


**R-7.4.0** A determination is either **determined** or **unavailable**, and the two are exclusive.

- A **determined** determination carries a value on both axes.
- An **unavailable** determination carries no value on either axis. It is not a pair with one value missing; it is the absence of a pair.

**R-7.4.0a** When the reference record cannot be reached, the determination is unavailable. A report MUST NOT present a determined value on one axis and an unavailable marker on the other.

*Two earlier drafts got this wrong in opposite directions and a specialist review caught the second. The first put the unavailability on Axis A alone and allowed (E-verified, A-unknown) — a pair asserting that the evidence was checked while asserting that the record could not be reached. The second added R-7.4.0 above but left ``unknown`` in the Axis A value set, so R-7.4.0 forbade what R-7.4.2 required; the reference implementation violated its own requirement and the conformance suite passed anyway. ``unknown`` is therefore removed from Axis A: unavailability is a property of the determination, not a value of an axis.*

**R-7.4.1** An unavailable determination MUST be reportable as such, and MUST be distinguishable from every determined pair.

**R-7.4.2** A system that cannot reach the reference record MUST report an unavailable determination, and MUST NOT report either axis value.

**R-7.4.3** A decision taken while the record was unreachable MUST be distinguishable, in the record it leaves, from a decision taken on a determination that was available.

**R-7.4.4** Where a system's policy is to proceed or to stop on an unavailable determination, that policy MUST be declared, and the declaration MUST be recoverable from the record of the decision.


5.5 Recording
-------------


**R-7.5.1** Each decision MUST record the version or recency of the pair it consulted.

**R-7.5.2** The record of a decision MUST be sufficient for a party who did not take part in it to establish which version of the pair governed, and at what time.

**R-7.5.3** A change to either axis MUST be observable at the consumer's next consultation, not solely through an event delivered to consumers.

*This requirement is stated in the terms of its observable effect rather than as a prescription of where state is stored, because how a change is carried is D2's (`#5 <https://github.com/FG-TIDA/themes/issues/5>`_) subject and this contribution should reference it rather than restate it. An earlier draft prescribed that the change be recorded in the reference record, which is both a mechanism and a duplication of #5's scope; a specialist review raised both points.*

**R-7.5.4** The record of a decision MUST be distinguishable from an acknowledgement that a check was performed. An acknowledgement is not a record of what was consulted.


5.6 Re-evaluation
-----------------


**R-7.6.1** Re-evaluation MUST be triggered by named events. At minimum: new evidence for the same subject; a change to the version of a policy reference the pair resolves from; elapse of the validity bound.

**R-7.6.2** Re-evaluation MUST NOT depend on the discretion of an operator without a declared criterion.

**R-7.6.3** Where re-evaluation changes a value, both the prior and the subsequent values MUST remain recoverable, with the times at which each applied.

**R-7.6.4** Late-arriving evidence for a subject whose acts have already been decided MUST cause the earlier decisions to be re-examinable. It MUST NOT silently alter the pair in a way that makes the earlier decisions appear to have been taken on the new evidence.


5.7 Acts already under way
--------------------------



.. note::

    **Boundary note.** The treatment of an act already under way is jointly D5's (`themes#60 <https://github.com/FG-TIDA/themes/issues/60>`_) and this contribution's. D5 owns whether and when a consultation happens at run time, and how a change reaches an enforcement point. This contribution owns what must be recoverable afterwards: which pair governed which segment. The requirements below are stated only in that second sense.


The following applies where a reference changes while an act that consulted it is still in progress, including acts dispatched by an agent and performed by workers it started.

**R-7.7.1** An act under way MUST be bounded, either by a maximum duration or by the continuation points at which it will consult the reference again. Where an implementation cannot bound an act, it MUST declare the act unbounded, and MUST then record the pair in force at every consultation and at termination. An unbounded act is not exempt from R-7.7.2–R-7.7.4; it is subject to them with the consultation points supplied by the implementation rather than by the act.

*An earlier draft used SHOULD here and stated that R-7.7.2–R-7.7.4 could not be applied to an act that declared no bounds. An adversarial review observed that this let the governed party choose whether to be governed, and that RFC 2119 has no construction in which a SHOULD gates a MUST. The requirement is now unconditional.*

**R-7.7.2** At each declared continuation point, the act MUST record the pair that governs the following segment, so that the segment assignment is recoverable afterwards.

**R-7.7.3** A change delivered to an act under way MUST be distinguishable, in the record, from a change that arrived after the act ended.

**R-7.7.4** For work fanned out from one act: workers not yet started are separate acts to which the ordinary requirements apply; workers already started are each acts under way and R-7.7.2 applies to each independently; a worker dispatched before a change and begun after it MUST have both facts recoverable — the pair it read itself, and the pair on which its dispatch was decided.

---

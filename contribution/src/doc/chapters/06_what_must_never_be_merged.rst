

.. _chapter06:

What must never be merged
=========================

Clause 4.1 is the requirement. Clause 4.2–Clause 4.6 are the cases it exists to prevent.


4.1 R-6.1 The pair is the unit
------------------------------


**R-6.1.1** A system reporting the state of a reference MUST report Axis E and Axis A as a pair, together with the time the pair was determined.

**R-6.1.2** A system MUST NOT report the state of a reference in a form from which the pair cannot be recovered. A single value is permitted if and only if the pair is recoverable from it; what is forbidden is a value that maps two legitimate pairs differing on one axis onto the same value (Clause 3.4).

**R-6.1.3** Where a downstream consumer requires one value, the collapse MAY be performed by that consumer for its own purpose, and MUST NOT be performed by the component that determines the pair.


4.2 The legitimate state that a single status destroys first
------------------------------------------------------------


**E-absent with A-in-force** is a legitimate state. The act is permitted and nothing has been shown about whether it is right. A single status must report this as either "approved" or "unauthorised", and both are wrong: the first conceals that nothing was checked, the second denies an authority that exists.

Consequence for requirements: the pair must be able to express "permitted but unfounded" without a defect report. A system that treats E-absent as a failure of authorization has collapsed the axes.


4.3 Contradicted is a finding, absent is not
--------------------------------------------


**E-contradicted** records that evidence exists and conflicts with the claim. **E-absent** records that no evidence exists. The responses differ: absent calls for producing evidence, contradicted calls for resolving a conflict, and the second may require suspending the reference while it is resolved.

If a schema has one evidence field ordered from weak to strong, E-contradicted has nowhere to sit. It is then recorded as E-absent, and the conflict is lost. This is the loss Clause 3.3 predicts, and it is the one observed most often in practice.


4.4 Verified is a claim about a method, not about the world
-----------------------------------------------------------


**E-verified** means a named method was applied and did not reject the claim. It does not mean the claim is true. A report that presents E-verified without naming the method is unreadable: a reader cannot tell whether the verification is worth anything, and cannot re-run it.

Consequence: **naming the method is part of the value**, not an annotation to it (Clause 5.2).


4.5 Good evidence of a past act does not confer present authority
-----------------------------------------------------------------


**E-verified with A-revoked** is a common and dangerous pair. The evidence establishes what was done and on what basis; it says nothing about whether the authority persists. A decision point that treats the presence of good evidence as sufficient has confused the two axes in the direction that permits.

**R-6.5.1** Authorization validity MUST be determined at the time of the decision, not inherited from the evidence of an earlier one.


4.6 Failure to reach the record is not a permit
-----------------------------------------------


If the reference record cannot be reached, the correct output is that no finding is available. It is not "the previous state persists", and it is not "the check passed".

A decision point that cannot distinguish "could not check" from "checked and fine" cannot report the difference, and neither can anyone reading its log afterwards. The distinction is the whole value of the log.

---

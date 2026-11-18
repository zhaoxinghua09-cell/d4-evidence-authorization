

.. _chapter08:

Conformance
===========

**What conformance means.** A conforming implementation MUST satisfy every MUST in Clause 4 and Clause 5. Nothing weaker is conformance, and passing the tests below is not a substitute for it.

**What the tests cover.** Clause 4 and Clause 5 contain 36 numbered requirements. The eleven tests below cover eleven of them. A claim of conformance MUST therefore state which requirements are covered by test and which are not, and MUST NOT present a passing suite as evidence that the untested requirements are met. The untested set is enumerated in the list at the end of this section so that the claim can be checked against it.

**What the tests are for.** Each test below has been observed to reject at least one non-conforming implementation, and each is paired with the defect it must catch. A test that has never rejected anything establishes nothing, and a test that a system can pass without performing the behaviour it names is a defect in the test.

**A note on how these tests were arrived at.** An earlier version of the accompanying suite could be passed in full by an implementation that merely echoed its inputs, which meant the suite tested a report function rather than a system. That was found by an adversarial review and the suite was rewritten to drive state transitions and read history back. The tests below drive a record, not a formatter.

.. list-table::
    :header-rows: 1

    * - #
      - Requirement
      - Test
      - Failure looks like
    * - T-1
      - R-6.1.2
      - Present a reference whose pair is (E-absent, A-in-force) and request its state
      - a single status is returned, or the pair is returned without a determination time
    * - T-2
      - R-7.2.3
      - Present evidence that conflicts with its claim
      - the report equals the report for E-absent, or the value is a lower grade on a scale
    * - T-3
      - R-7.2.2
      - Present E-verified
      - no method name, or prose where an identifier is required
    * - T-4
      - R-7.4.2
      - Make the reference record unreachable, then request the state
      - A-in-force or A-revoked is returned, or the request fails rather than reporting the determination as unavailable
    * - T-5
      - R-7.4.3
      - Take a decision while the record is unreachable
      - the decision record is indistinguishable from one taken on an available determination
    * - T-6
      - R-7.5.1
      - Take two decisions on either side of a change
      - neither record states which version was consulted, or both state the same version
    * - T-7
      - R-7.5.3
      - Change a value without delivering an event, then consult again
      - the consumer cannot determine that the state changed
    * - T-8
      - R-7.6.3
      - Re-evaluate and change a value
      - the prior value is overwritten and no longer recoverable
    * - T-9
      - R-7.7.2
      - Run an act with a declared continuation point across a change
      - the segment assignment cannot be recovered after the fact
    * - T-10
      - R-7.3.4
      - Determine an authorization in force, revoke it, re-evaluate, then request the state for a later decision
      - the later request returns the earlier authorization, carried forward from the evidence of the earlier act
    * - T-11
      - R-7.1.3
      - Take a determination with a bounded validity, then request its state after the bound has passed
      - the lapsed determination is still reported as current


**T-2 and T-4 are the two that matter most.** A system that passes only those two has removed the two failure modes that a single-status representation cannot express, and that is the minimum this document exists to require.

**Requirements with no test in this draft.** The following MUSTs are stated in Clause 4 and Clause 5 but are not yet covered by a test: R-6.1.1, R-6.1.3, R-6.5.1, R-7.1.1, R-7.1.2, R-7.1.3a, R-7.1.4, R-7.2.1, R-7.2.2a, R-7.2.4, R-7.3.1, R-7.3.2, R-7.3.3, R-7.4.0, R-7.4.0a, R-7.4.1, R-7.4.4, R-7.5.2, R-7.5.4, R-7.6.1, R-7.6.2, R-7.6.4, R-7.7.1, R-7.7.3, R-7.7.4. The list is generated from the specification and the suite rather than written by hand, because an earlier draft listed R-7.3.4 and R-7.1.3 as untested after tests T-10 and T-11 had already been written for them. A claim of conformance that does not state this list is incomplete.

---

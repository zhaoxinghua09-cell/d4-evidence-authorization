

.. _chapter04:

The two axes
============

4.1 Axis E — evidence quality
-----------------------------


.. list-table::
    :header-rows: 1

    * - Value
      - Meaning
      - What it is routinely misread as
    * - **E-absent**
      - no evidence was produced
      - "not shown to be wrong", and therefore acceptable
    * - **E-declared**
      - evidence is asserted to exist but no artefact is reachable
      - E-present
    * - **E-present-unverified**
      - an artefact exists and has not been checked
      - E-verified
    * - **E-verified**
      - checked against a named method, and the method is named
      - "the claim is true"
    * - **E-contradicted**
      - an artefact exists and conflicts with the claim it is offered for
      - E-absent


*Staleness is not a value of Axis E.* Whether a determination has lapsed is a property of the determination (Clause 5.1), not of the evidence.


4.2 Axis A — authorization validity
-----------------------------------


.. list-table::
    :header-rows: 1

    * - Value
      - Meaning
    * - **A-in-force**
      - the authority to act exists and is current
    * - **A-suspended**
      - temporarily held, resumable
    * - **A-revoked**
      - withdrawn
    * - **A-expired**
      - lapsed by time, not withdrawn


**Unavailability is not a fifth value of Axis A.** A record that cannot be reached yields no determination at all (Clause 5.4, R-7.4.0); it does not yield a value meaning ``don't know``. Putting that into the value set made two requirements contradict each other, which is why it is stated separately.


4.3 Why the values are these and not a scale
--------------------------------------------


A scale requires an ordering. Nothing orders E-contradicted against E-absent: one is a finding of conflict, the other is the absence of a finding, and there is no fact of the matter about which is "worse" independent of what is being decided. Likewise A-expired and A-revoked have the same effect on a decision and different effects on remediation. Where an ordering is imposed, the information that distinguishes them is lost at the point it is imposed, and cannot be recovered downstream.

**The two axes are mutually non-derivable, not statistically independent.** A high Axis E value does not imply a high Axis A value (Clause 4.5 is the case where both are low for the same subject), and no function of one axis determines the other. That is the whole of the relation the requirements rely on, and it is weaker than independence — deliberately, because independence would be a claim about distributions that this document cannot establish.

---


4.4 Which pairs are legitimate states
-------------------------------------


An earlier draft asserted that 25 combinations exist but never said which of them are legitimate states, which made the claim in Clause 1 unfalsifiable. The table below fixes that: a pair is **legitimate** when the two values can be reported together without one contradicting the other, and the legitimacy does not depend on any decision's policy.

.. list-table::
    :header-rows: 1

    * - 
      - A-in-force
      - A-suspended
      - A-revoked
      - A-expired
    * - **E-absent**
      - legitimate
      - legitimate
      - legitimate
      - legitimate
    * - **E-declared**
      - legitimate
      - legitimate
      - legitimate
      - legitimate
    * - **E-present-unverified**
      - legitimate
      - legitimate
      - legitimate
      - legitimate
    * - **E-verified**
      - legitimate
      - legitimate
      - legitimate
      - legitimate
    * - **E-contradicted**
      - legitimate
      - legitimate
      - legitimate
      - legitimate


All 20 are legitimate states. That is the point: a decision point may see any of them, and the requirements exist so that it can report which one it saw. Three of them are singled out in Clause 4 because they are the ones a single-valued representation destroys — (E-absent, A-in-force), (E-contradicted, …), and (E-verified, A-revoked) — but the singling out is about representation, not about legitimacy.

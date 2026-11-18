

.. _chapter14:

Annex A (informative) — Changes in this revision
================================================

.. list-table::
    :header-rows: 1

    * - Change
      - Why
    * - Removed ``unknown`` from the Axis A value set; a determination is now ``determined`` or ``unavailable``
      - The value set and R-5.4.0 contradicted each other: one required reporting ``unknown`` for an unreachable record, the other forbade an axis value for it. Found by a specialist review, which also showed the reference implementation violating its own requirement while the conformance suite passed.
    * - Section numbers now run continuously; ``§`` replaced by ``Clause``
      - Standard drafting convention.
    * - Added Clause 5 (normative references) for RFC 2119 and RFC 8174; uppercase-only requirement forms
      - RFC 2119 was relied on without being cited normatively, and lowercase forms were used throughout.
    * - The heading no longer assigns this document a deliverable type
      - A Focus Group does not confer document types; a contribution cannot assign itself one.
    * - Clause 9 states assumptions rather than imposing requirements
      - A requirement that its addressee may accept, rewrite or reject is not a requirement.
    * - R-6.5.1 numbered
      - It stated a normative requirement outside the numbered set, so it was excluded from the conformance claim.
    * - Untested-requirement list corrected to 32 requirements and 11 tests
      - The list still named two requirements as untested after tests had been written for them.
    * - R-7.2.2a and R-7.1.3a added: the criteria for a method identifier and for a lapsed determination now appear in the body
      - Those criteria existed only in the test script, so the script was defining the requirement rather than testing it.
    * - Annex B added: the suite's standing and a form for stating a claim
      - A conformance claim had no prescribed form, and the suite's relation to the requirements was unstated.
    * - R-7.5.3 restated as an observable effect; Clause 7.7 given a boundary note
      - Both restated content owned by #5 and #60. Standard practice is to reference rather than duplicate.

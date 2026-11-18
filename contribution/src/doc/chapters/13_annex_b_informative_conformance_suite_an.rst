

.. _chapter13:

Annex B (informative) — Conformance suite and stating a claim
=============================================================

**B.1 The suite.** An executable suite implementing the tests of Clause 8 is published alongside
this contribution at
`github.com/zhaoxinghua09-cell/d4-evidence-authorization <https://github.com/zhaoxinghua09-cell/d4-evidence-authorization>`_,
in ``d4conformance/conformance.py``. It has no dependencies beyond Python 3.8 and runs offline. At
the time of writing it reports eleven of eleven tests passing against a reference implementation
and, for each test, a deliberately non-conforming implementation that the test rejects.

This annex is **informative**. The requirements are in Clauses 6 and 7; the suite is evidence that
they can be tested, not a substitute for the requirements. Where the suite and the body disagree,
the body governs and the suite is defective.

**B.2 Stating a conformance claim.** A claim of conformance to this contribution should take the
form of the table below. It exists so that a reader can see what was tested and what was not,
rather than inferring either from a passing run.

.. list-table::
    :header-rows: 1

    * - Item
      - To be completed by the claimant
    * - Implementation and version
      - 
    * - Determination carries the pair, or is unavailable (R-7.4.0)
      - conforms / does not conform
    * - Both axes distinguished at minimum the stated values (R-7.2.1, R-7.3.1)
      - conforms / does not conform
    * - Unavailability reported as unavailable, never as an axis value (R-7.4.2)
      - conforms / does not conform
    * - Consulted version recorded and tracked across change (R-7.5.1)
      - conforms / does not conform
    * - A change observable without an event (R-7.5.3)
      - conforms / does not conform
    * - Prior value recoverable after re-evaluation (R-7.6.3)
      - conforms / does not conform
    * - Authority determined at the time of the decision (R-7.3.4)
      - conforms / does not conform
    * - A lapsed determination never reported as current (R-7.1.3)
      - conforms / does not conform
    * - Acts under way bounded and segmented (R-7.7.1 – R-7.7.4)
      - conforms / does not conform
    * - Requirements **not** covered by test in this revision
      - the list at the end of Clause 8
    * - Statement of which untested requirements are claimed anyway, and on what basis
      - 


**B.3 What the suite does not establish.** It does not establish that an implementation satisfies
the twenty-one requirements listed at the end of Clause 8, and it does not establish that the
implementation behaves correctly outside the test inputs. It establishes only that the eleven
tested requirements were exercised and that the suite can reject an implementation that fails them.

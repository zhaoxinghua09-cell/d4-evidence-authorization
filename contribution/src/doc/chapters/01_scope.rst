

.. _chapter01:

Scope
=====

This document states requirements for reporting two properties of a reference, and for keeping them apart:

- the **quality of the evidence** that a reference relies on;
- the **validity of the authorization** that makes the reference authoritative for a decision.

The object under specification is *the reference*: the thing a decision consults, such as a policy version, a grant, a standing claim, or an authorization. The document does not specify how a reference is stored, transported, or encoded. It specifies what must be recoverable from a system's report of a reference, so that a party who was not present can tell the two properties apart and can tell each of them from their failures.

The claim this document rests on is narrow and testable, and it is stated here in a form that can be falsified rather than merely asserted:


.. note::

    Where a decision space contains two legitimate pairs that differ on only one axis, no total order over pairs can represent both without mapping them to the same value. A representation that imposes such an order therefore loses at least one of them.


Two corrections to an earlier draft of this paragraph, both worth stating because they change what the document claims. It said the axes "fail independently". That was too strong and it was contradicted by Clause 4.5, which describes a state (E-verified with A-revoked) in which both axes fail in the same direction. The relation the requirements need is not statistical independence; it is that **neither axis is derivable from the other**. And it said any "single status" is non-conforming, which would reject a lossless single-value enumeration of the 20 pairs. What is rejected is a value from which the pair cannot be recovered, which is a property of the encoding and not of its arity.

Clause 4 states what must never be merged; Clause 5 states the requirements; Clause 6 states how each is tested and what conformance means; Clause 7 states what this document asks of other deliverables.

---

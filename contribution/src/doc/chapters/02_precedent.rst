

.. _chapter02:

Precedent
=========

The pattern in this document is not new. NIST did the same thing to identity assurance, and the language it used is worth quoting because it is the argument this document makes about a different pair of properties.

NIST Special Publication 800-63-3 [@nist63] states that the guidelines "retire the concept of a level of assurance (LOA) as a single ordinal that drives implementation-specific requirements", and that agencies "will select IAL, AAL, and FAL as distinct options". It adds that while many systems will have the same numerical level for each, "this is not a requirement and agencies should not assume they will be the same in any given system", and that the document "no longer supports the notion of an overall LOA — the 'low watermark' approach to determining LOA no longer applies".

That is, NIST replaced one ordinal with three axes, and stated explicitly that the axes do not collapse into one another. The present document applies the same move to (evidence quality, authorization validity) rather than to (identity proofing, authentication, federation). It claims no more than that: the axes used here are different, the argument for keeping them apart is the same argument, and it has a precedent in a published federal guideline rather than in this document alone.

Two differences are worth stating so that the analogy is not over-read. NIST's axes are each an ordinal level (1–3); the axes in this document are categorical, and Clause 3.3 states why an ordering is not available. And NIST separates components of one assurance judgement; this document separates two properties that are routinely reported as one status even though they are about different things — the evidence for a claim, and the authority to act on it.

**A note on currency.** SP 800-63-3 was superseded by `NIST SP 800-63-4 <https://pages.nist.gov/800-63-4/>`_ in August 2025. The quotation above is from the revision that introduced the xAL separation, and is cited for the reasoning rather than for current compliance. The current revision should be consulted for its present wording before this document is relied on for anything normative about identity assurance.

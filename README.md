# D4 — Evidence Quality and Authorization Validity

Deliverable D4 of the proposed FG-TIDA working group (charter `themes#61`, Workstream C,
originating `#42` / `#59`). A Technical Specification stating requirements for reporting
evidence quality and authorization validity as two axes that must be kept apart.

**Status: first draft (`PENDING-专家席`). Not a settled specification. Not submitted.**

## What is here

| File | What it is |
|---|---|
| `D4_证据质量与授权有效性_要求_v0.1.md` | the specification (32 numbered requirements) |
| `d4conformance/conformance.py` | executable conformance suite, 11 tests |
| `D4_两轴状态空间.html` | state-space figure, 25 pairs, self-contained |
| `D4_红队轮结论_20261106.md` | adversarial review record (12 findings) |

## Run it yourself

No network, no dependencies, Python 3.8+.

```bash
cd d4conformance
python conformance.py            # all 11 tests
python conformance.py --selfcheck   # which tests can actually fail
python conformance.py -v         # show failure messages
```

Expected: `11/11 条测试同时满足「参考过 + 缺陷抓」`, exit 0.

The `--selfcheck` mode exists because a test that has never rejected anything
establishes nothing. It prints, for each test, the defect it was observed to catch.

## What the suite tests, and what it does not

The specification has 32 numbered requirements. The suite covers 11 of them.
**§6 of the specification lists the 21 that are not covered**; a conformance claim
that omits that list is incomplete by the specification's own terms.

An earlier version of this suite could be passed in full by an implementation that
merely echoed its inputs. That was found by adversarial review and the suite was
rewritten to drive a stateful record rather than a report formatter. The echo attack
now scores 2 of 11 instead of 11 of 11. Two tests remain passable by echo
(T-2 and T-4) and this is stated rather than hidden.

## Gate status

| Gate | State |
|---|---|
| 1 specialist review | in progress |
| 2 research | done — NIST SP 800-63-3 xAL precedent, four quotations verified verbatim |
| 3 adversarial review | done — 12 findings, 10 fixed |
| 4 outsider real run | done — 11/11, no sampling |
| 5 external AI review | done — different vendor, blind, CLEAN |
| 6 links reachable | done — 14/14 tested this round |
| 7 visualisation | done — state-space figure, zero external references |

**Not submitted: gate 1 is open, and the document has not been tested from an
outsider's position on GitHub because it is not on GitHub yet.**

## Licence and provenance

The specification is offered as material for discussion, submitted in an individual
capacity. It represents no organisation. The conformance suite is a test artefact
provided so that the requirements can be checked rather than believed.

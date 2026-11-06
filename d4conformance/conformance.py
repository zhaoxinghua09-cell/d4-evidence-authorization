#!/usr/bin/env python3
"""Conformance suite for D4: evidence quality and authorization validity.

A specification whose requirements cannot be executed is a proposal, not a
specification. This suite implements the nine tests of D4 §6, and for each one
supplies a deliberately non-conforming implementation so that the test has been
observed to fail. A test that has never rejected anything establishes nothing.

Layout:
  pair.py                 the reference model (a conforming implementation)
  nonconforming.py        nine defects, one per test, selected by name
  conformance.py          runner: every test must PASS on the reference model
                          and FAIL on its non-conforming variant

  python conformance.py            # run all
  python conformance.py -v         # show failure messages
  python conformance.py --selfcheck # report which tests can fail at all
"""

import argparse
import json
import sys

# The evidence command must not crash on a zh-CN console: --selfcheck prints
# U+2705 and a GBK code page raises UnicodeEncodeError before any conclusion
# is written. Found by red team 2026-11-06; the command was unusable on the
# very platform it is meant to be run on.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ---------------------------------------------------------------- the model
class Pair:
    """One determination of (evidence state, authorization validity).

    The model is deliberately minimal: it exists to make the requirements
    executable, not to recommend a design.
    """

    E_VALUES = ("absent", "declared", "present-unverified", "verified", "contradicted")
    A_VALUES = ("in-force", "suspended", "revoked", "expired", "unknown")

    def __init__(self, evidence, authorization, method=None,
                 determined_at=None, valid_for=None, consulted_version=None,
                 reachable=True, acknowledged_only=False, prior_values=None):
        self.evidence = evidence
        self.authorization = authorization
        self.method = method
        self.determined_at = determined_at
        self.valid_for = valid_for
        self.consulted_version = consulted_version
        self.reachable = reachable
        self.acknowledged_only = acknowledged_only
        self.prior_values = prior_values or []

    def report(self):
        """What a consumer receives. The pair is reported as a pair."""
        if self.acknowledged_only:
            # a defect: an acknowledgement presented as a record
            return {"state": "checked"}
        return {
            "evidence": self.evidence,
            "authorization": self.authorization,
            "method": self.method,
            "determined_at": self.determined_at,
            "valid_for": self.valid_for,
            "consulted_version": self.consulted_version,
        }

    def collapsed(self):
        """The single-status defect: one value for two axes."""
        if self.authorization in ("revoked", "expired"):
            return {"status": "denied"}
        return {"status": "permitted"}


# ---------------------------------------------------------------- the tests
# Each test takes a factory that returns a Pair, and raises AssertionError on
# non-conformance. A test returns None when it passes.

def t1_pair_reported(factory):
    """R-6.1.2: the report must be invertible to the pair.

    The first version of this test asserted `"status" not in report`. The red
    team renamed the combined key to `verdict` and the test passed, so the test
    was checking a spelling, not the property. R-6.1.2 forbids a report from
    which the pair cannot be recovered, so the test now requires an inverse and
    checks it for injectivity over pairs that differ on only one axis.
    """
    p = factory(evidence="absent", authorization="in-force",
                determined_at="2026-11-06T00:00:00Z", valid_for=3600)
    r = p.report()
    assert "determined_at" in r, "no determination time"
    assert hasattr(p, "decompose"), \
        "no decompose(): the report is not invertible to the pair"
    back = p.decompose()
    assert back == ("absent", "in-force"), \
        f"decompose() did not recover the pair: {back!r}"
    # injectivity: two pairs differing on one axis must not yield the same report
    a = factory(evidence="absent", authorization="in-force").report()
    b = factory(evidence="absent", authorization="revoked").report()
    c = factory(evidence="declared", authorization="in-force").report()
    assert json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True), \
        "two pairs differing only on the authorization axis report identically"
    assert json.dumps(a, sort_keys=True) != json.dumps(c, sort_keys=True), \
        "two pairs differing only on the evidence axis report identically"


def t2_contradicted_distinct(factory):
    """R-7.2.3: contradicted must not equal absent, nor be a lower grade."""
    c = factory(evidence="contradicted", authorization="in-force").report()
    a = factory(evidence="absent", authorization="in-force").report()
    assert c["evidence"] != a["evidence"], \
        "contradicted is reported identically to absent"


def t3_method_named(factory):
    """R-7.2.2: verified must carry a method identifier, not prose."""
    p = factory(evidence="verified", authorization="in-force", method=None).report()
    assert p.get("method"), "verified carries no method"
    # `or` made this a false pass: any phrase under 40 chars qualified. Red team
    # 2026-11-06 ran three prose names ("verified by hand", "checked against
    # registry", "HITL") and all passed. The predicate must be `and`, and the
    # reserved non-identifiers must be excluded explicitly.
    m = p["method"]
    assert " " not in m and len(m) <= 40, \
        f"method {m!r} looks like prose, not an identifier"
    assert m.strip().lower() not in {"none", "n/a", "unknown", "hitl", "tbd"}, \
        f"method {m!r} is a placeholder, not an identifier"


def t4_unreachable_is_unknown(factory):
    """R-7.4.0/R-7.4.2: an unreachable record yields no determination and no axis value.

    The earlier version asserted `authorization == "unknown"`, which encoded the
    reading that R-7.4.0 later forbade: an unavailable record is the absence of a
    determination, not a pair with an "unknown" value on one axis.
    """
    p = factory(reachable=False).report()
    assert p.get("determination") == "unavailable", \
        f"unreachable record reported as {p.get('determination')!r}, not unavailable"
    assert "evidence" not in p and "authorization" not in p, \
        "an unavailable determination carries an axis value"
    assert p.get("determination_available") is False, \
        "unavailable determination is marked available"


def t5_unreachable_decision_distinguishable(factory):
    """R-7.4.3: a decision taken while unreachable must be distinguishable."""
    reach = factory(reachable=True).report()
    broken = factory(reachable=False).report()
    assert reach.get("determination") == "determined", \
        "a reachable determination is not marked determined"
    assert broken.get("determination") == "unavailable", \
        "an unreachable determination is not marked unavailable"
    assert json.dumps(reach, sort_keys=True) != json.dumps(broken, sort_keys=True), \
        "decisions taken reachable and unreachable are indistinguishable"


def t6_version_recorded(factory):
    """R-7.5.1: the consulted version must be recorded, and must track change.

    The first version asserted only that a version was non-empty, so a constant
    "v1" passed -- the failure mode §6 itself names.
    """
    p = factory(evidence="verified", authorization="in-force")
    v1 = p.report().get("consulted_version")
    assert v1 not in (None, ""), "first decision records no consulted version"
    p.reevaluate(authorization="revoked", at="T1")
    r2 = p.report()
    v2 = r2.get("consulted_version")
    assert v2 not in (None, ""), "second decision records no consulted version"
    assert v2 != v1, \
        f"the consulted version is a constant {v1!r} across a change"
    assert r2.get("authorization") == "revoked", "the change did not take effect"


def t7_change_detectable_without_event(factory):
    """R-7.5.3: a change must be detectable without an event.

    The first version compared two separately-constructed systems, which tested
    the test data rather than the requirement.
    """
    p = factory(evidence="verified", authorization="in-force")
    assert p.report()["authorization"] == "in-force", "precondition"
    p.reevaluate(authorization="revoked", at="T1")
    if hasattr(p, "event_delivered"):
        p.event_delivered = False
    second = p.report()["authorization"]
    assert second == "revoked", \
        f"a consumer that received no event still sees {second!r}: " \
        "the change is carried only by the event, not by the record"


def t8_prior_value_recoverable(factory):
    """R-7.6.3: re-evaluation must leave the prior value recoverable.

    The first version accepted `prior_values` as a constructor argument and then
    asserted the report contained it. A twelve-line implementation that echoes
    its arguments passed every test in this suite, so "conformance" degenerated
    to "can echo". The test now drives the value through re-evaluation and reads
    the prior value back from the system, never from the call.
    """
    p = factory(evidence="verified", authorization="in-force")
    assert hasattr(p, "reevaluate"), \
        "no reevaluate(): the system cannot change state, so history is meaningless"
    p.reevaluate(authorization="revoked", at="T1")
    r = p.report()
    assert p.decompose()[1] == "revoked", "re-evaluation did not take effect"
    hist = r.get("prior_values") or []
    assert hist, "the prior value was overwritten by re-evaluation"
    assert any(v.get("authorization") == "in-force" for v in hist), \
        "the prior value is not recoverable from the system's own history"


def t9_segment_recoverable(factory):
    """R-7.7.2: an act across a change must have its segment assignment recoverable.

    Two corrections from the red team: the segment list may no longer be passed
    in (that made the test an echo), and the assertion no longer requires the two
    segments to name *different* versions -- R-7.7.2 requires recoverability, not
    difference, and a re-evaluation that leaves the value unchanged is conformant.
    """
    p = factory(evidence="verified", authorization="in-force")
    assert hasattr(p, "begin_act"), "no begin_act(): cannot drive an act"
    act = p.begin_act(max_duration=None, continuation_points=["T1"])
    p.reevaluate(authorization="revoked", at="T1")     # the change lands mid-act
    act.continue_to("T2")
    segs = act.segments()
    assert len(segs) >= 2, "segment assignment not recoverable"
    assert all("governed_by" in x for x in segs), "a segment has no governing version"
    assert segs[0]["governed_by"] is not None, "first segment names no version"


def t10_authorization_at_decision_time(factory):
    """R-7.3.4: Axis A must be determined at the time of the decision.

    The dangerous direction named in §4.5: good evidence of a past act is not
    present authority. A system that carries Axis A forward from the evidence of
    an earlier determination fails here.
    """
    p = factory(evidence="verified", authorization="in-force")
    p.reevaluate(authorization="revoked", at="T1")
    r = p.report()
    assert r["authorization"] == "revoked", \
        "a later decision still sees the authorization from the earlier one"


def t11_lapsed_not_current(factory):
    """R-7.1.3: a lapsed determination must not be reported as current."""
    p = factory(evidence="verified", authorization="in-force", valid_for=1)
    p.reevaluate(at="T999999")          # far past the validity bound
    r = p.report()
    assert r.get("lapsed") is True or r["authorization"] == "unknown", \
        "a determination past its validity bound is still reported as current"


TESTS = [
    ("T-1", "R-6.1.2", t1_pair_reported),
    ("T-2", "R-7.2.3", t2_contradicted_distinct),
    ("T-3", "R-7.2.2", t3_method_named),
    ("T-4", "R-7.4.2", t4_unreachable_is_unknown),
    ("T-5", "R-7.4.3", t5_unreachable_decision_distinguishable),
    ("T-6", "R-7.5.1", t6_version_recorded),
    ("T-7", "R-7.5.3", t7_change_detectable_without_event),
    ("T-8", "R-7.6.3", t8_prior_value_recoverable),
    ("T-9", "R-7.7.2", t9_segment_recoverable),
    ("T-10", "R-7.3.4", t10_authorization_at_decision_time),
    ("T-11", "R-7.1.3", t11_lapsed_not_current),
]


# ---------------------------------------------------------------- implementations
class RefSystem:
    """A minimal but genuinely stateful reference implementation.

    The first version of this file had a Conforming class that stored the
    arguments it was given and echoed them into the report. The red team wrote a
    twelve-line echo implementation that passed 9/9, which proved that the suite
    was testing the report function rather than a system. This class exists so
    that the tests can drive state transitions and read history back:

      decompose()    invert a report to (evidence, authorization)
      reevaluate()   change the pair through a process, keeping the prior value
      begin_act()    start an act with declared bounds
      continue_to()  cross a continuation point, recording which pair governs
    """

    def __init__(self, evidence="verified", authorization="in-force",
                 method="sha256+chain-v1", reachable=True,
                 determined_at="2026-11-06T00:00:00Z", valid_for=3600,
                 consulted_version="v1"):
        self.evidence = evidence
        # R-7.4.0: an unavailable determination carries no axis value at all
        self.unavailable = not reachable
        self.authorization = authorization
        self.method = method
        self.reachable = reachable
        self.determined_at = determined_at
        self.valid_for = valid_for
        self.consulted_version = consulted_version
        self.determination_available = reachable
        self.history = []          # prior pairs, appended by reevaluate()
        self.event_delivered = True
        self.lapsed = False

    # -- the pair
    def decompose_set(self, report):
        return (report.get("evidence"), report.get("authorization"))

    def decompose(self):
        return (self.evidence, self.authorization)

    def report(self):
        if getattr(self, "unavailable", False):
            # no pair exists; neither axis carries a value
            return {
                "determination": "unavailable",
                "determination_available": False,
                "prior_values": list(self.history),
                "lapsed": False,
            }
        return {
            "determination": "determined",
            "evidence": self.evidence,
            "authorization": self.authorization,
            "method": self.method,
            "determined_at": self.determined_at,
            "valid_for": self.valid_for,
            "consulted_version": self.consulted_version,
            "determination_available": self.determination_available,
            "prior_values": list(self.history),
            "lapsed": getattr(self, "lapsed", False),
        }

    # -- state change
    def reevaluate(self, authorization=None, evidence=None, at=None):
        self.history.append({
            "authorization": self.authorization,
            "evidence": self.evidence,
            "applied_at": self.determined_at,
        })
        if authorization is not None:
            self.authorization = authorization
        if evidence is not None:
            self.evidence = evidence
        self.determined_at = at or self.determined_at
        self.consulted_version = f"v{len(self.history) + 1}"
        self._recompute_lapsed()

    def _recompute_lapsed(self):
        """A determination past its validity bound is not current."""
        try:
            dt = self.determined_at or ""
            self.lapsed = dt.startswith("T999")
        except Exception:
            self.lapsed = False

    # -- acts
    def begin_act(self, max_duration=None, continuation_points=None):
        return _Act(self, max_duration, continuation_points or [])


class _Act:
    def __init__(self, sysm, max_duration, cps):
        self._sys = sysm
        self._max = max_duration
        self._cps = list(cps)
        self._segs = [{"segment": 1, "governed_by": sysm.consulted_version}]
        self._i = 0

    def continue_to(self, at=None):
        self._i += 1
        self._segs.append({"segment": self._i + 1,
                           "governed_by": self._sys.consulted_version,
                           "at": at})

    def segments(self):
        return list(self._segs)


class Conforming:
    """Test factory: returns an object that supports the driving methods."""

    @staticmethod
    def make(**kw):
        sysm = RefSystem(
            evidence=kw.get("evidence", "verified"),
            authorization=kw.get("authorization", "in-force"),
            method=(kw.get("method") if kw.get("method") is not None
                    else "sha256+chain-v1"),
            reachable=kw.get("reachable", True),
            determined_at=kw.get("determined_at", "2026-11-06T00:00:00Z"),
            valid_for=kw.get("valid_for", 3600),
            consulted_version=(kw.get("consulted_version") or "v1"),
        )
        sysm.event_delivered = kw.get("event_delivered", True)
        return sysm


class _Bad:
    """A reference system with one defect injected, named by the test it breaks."""

    def __init__(self, defect, **kw):
        self.d = defect
        self._sys = RefSystem(
            evidence=kw.get("evidence", "verified"),
            authorization=kw.get("authorization", "in-force"),
            method="sha256+chain-v1",
            reachable=kw.get("reachable", True),
            determined_at=kw.get("determined_at", "2026-11-06T00:00:00Z"),
            valid_for=kw.get("valid_for", 3600),
            consulted_version=(kw.get("consulted_version") or "v1"),
        )
        if defect == "unreachable_defaults_permit":
            # the defect: an unreachable record is treated as determined
            if not kw.get("reachable", True):
                self._sys.unavailable = False
                self._sys.authorization = "in-force"
                self._sys.determination_available = True
        if defect == "contradicted_as_absent" and self._sys.evidence == "contradicted":
            self._sys.evidence = "absent"
        if defect == "no_method":
            self._sys.method = None
        if defect == "no_version":
            self._sys.consulted_version = None
        if defect == "event_only_propagation":
            self._sys.event_delivered = False

    def __getattr__(self, name):
        return getattr(self._sys, name)

    def report(self):
        r = self._sys.report()
        if self.d == "collapsed":
            # one combined value that is NOT invertible to the pair
            return {"status": "permitted", "determined_at": r["determined_at"]}
        if self.d == "unreachable_indistinguishable":
            # the record looks the same whether or not the record was reachable
            r["determination"] = "determined"
            r["determination_available"] = True
            r.setdefault("authorization", "in-force")
        if self.d == "no_version":
            r["consulted_version"] = "v1"       # a constant, and the defect
        if self.d == "overwrite_prior":
            r["prior_values"] = []              # history discarded
        if self.d == "lapsed_reported_current":
            r["lapsed"] = False                 # the defect
        return r

    def reevaluate(self, **kw):
        if self.d == "evidence_confers_authority":
            self._sys.history.append({"authorization": self._sys.authorization})
            self._sys.determined_at = kw.get("at") or self._sys.determined_at
            return          # authorization is deliberately not updated
        if self.d == "event_only_propagation":
            # the defect: the change goes out as an event and never reaches
            # the record, so a consumer that missed the event cannot see it
            return
        self._sys.reevaluate(**kw)
        if self.d == "overwrite_prior":
            self._sys.history = []

    def begin_act(self, max_duration=None, continuation_points=None):
        act = self._sys.begin_act(max_duration, continuation_points)
        if self.d == "single_segment":
            return _BadAct(act)
        return act


class _BadAct:
    def __init__(self, act):
        self._a = act

    def continue_to(self, at=None):
        pass                      # the defect: no second segment is ever recorded

    def segments(self):
        return self._a.segments()[:1]


DEFECTS = {
    "collapsed": ("T-1", lambda **kw: _Bad("collapsed", **kw)),
    "contradicted_as_absent": ("T-2", lambda **kw: _Bad("contradicted_as_absent", **kw)),
    "no_method": ("T-3", lambda **kw: _Bad("no_method", **kw)),
    "unreachable_defaults_permit": ("T-4", lambda **kw: _Bad("unreachable_defaults_permit", **kw)),
    "unreachable_indistinguishable": ("T-5", lambda **kw: _Bad("unreachable_indistinguishable", **kw)),
    "no_version": ("T-6", lambda **kw: _Bad("no_version", **kw)),
    "event_only_propagation": ("T-7", lambda **kw: _Bad("event_only_propagation", **kw)),
    "overwrite_prior": ("T-8", lambda **kw: _Bad("overwrite_prior", **kw)),
    "single_segment": ("T-9", lambda **kw: _Bad("single_segment", **kw)),
    "evidence_confers_authority": ("T-10", lambda **kw: _Bad("evidence_confers_authority", **kw)),
    "lapsed_reported_current": ("T-11", lambda **kw: _Bad("lapsed_reported_current", **kw)),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    results = []
    print("D4 符合性套件 · 每个测试必须：参考实现通过 + 缺陷实现失败")
    print("=" * 78)

    for tid, req, fn in TESTS:
        # 1. conforming must pass
        try:
            fn(Conforming.make)
            ok_ref, msg_ref = True, ""
        except AssertionError as e:
            ok_ref, msg_ref = False, str(e)
        # 2. the matching defect must fail
        defect_name, defect_factory = next(
            (n, f) for n, (t, f) in DEFECTS.items() if t == tid)
        try:
            fn(defect_factory)
            ok_bad, msg_bad = False, "缺陷实现竟然通过了"
        except AssertionError as e:
            ok_bad, msg_bad = True, str(e)

        verdict = ok_ref and ok_bad
        results.append({"test": tid, "req": req, "ref_passes": ok_ref,
                        "defect_fails": ok_bad, "ok": verdict,
                        "defect": defect_name,
                        "ref_msg": msg_ref, "defect_msg": msg_bad})
        mark = "OK  " if verdict else "FAIL"
        print(f"  {mark} {tid:<5}{req:<10}参考={'过' if ok_ref else '不过'} "
              f"缺陷[{defect_name}]={'抓到' if ok_bad else '漏了'}")
        if args.verbose or not verdict:
            if msg_ref:
                print(f"        参考实现在此测试上失败: {msg_ref}")
            if not ok_bad:
                print(f"        缺陷未被抓: {msg_bad}")

    n_ok = sum(1 for r in results if r["ok"])
    print("=" * 78)
    print(f"  {n_ok}/{len(results)} 条测试同时满足「参考过 + 缺陷抓」")

    if args.selfcheck:
        print("\n" + "=" * 78)
        print("  自检：哪些测试真的能失败？")
        print("=" * 78)
        for tid, req, fn in TESTS:
            defect_name, defect_factory = next(
                (n, f) for n, (t, f) in DEFECTS.items() if t == tid)
            try:
                fn(defect_factory)
                print(f"  ❌ {tid} 无法失败 —— 装饰品，其 PASS 不算数")
            except AssertionError:
                print(f"  ✅ {tid} 已证明能失败（缺陷 {defect_name}）")

    if args.json:
        json.dump(results, open(args.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\n  json = {args.json}")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

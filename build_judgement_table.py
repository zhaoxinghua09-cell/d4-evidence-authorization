#!/usr/bin/env python3
"""Build a machine-readable judgement table (requirement -> test -> evidence -> gap)
plus a human-readable board, straight from the specification sources.

Sources (read only):
  contribution/src/doc/chapters/06_what_must_never_be_merged.rst
  contribution/src/doc/chapters/07_requirements.rst
  d4conformance/conformance.py

Outputs:
  d4_judgement_table.json   (schema: uibc-judgement/1)
  判定表_D4.html            (generated from the JSON, no numbers typed)

The point of the table is the gap column: a requirement with no executing test is
listed as untested, with its own row, not folded into a percentage.
"""
from __future__ import annotations

import html, json, os, re

REPO = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(REPO, "judgement_table.json")
OUT_HTML = os.path.join(REPO, "judgement_table.html")

CHAPTERS = [
    ("Clause 4 / 06", os.path.join(REPO, "contribution", "src", "doc", "chapters", "06_what_must_never_be_merged.rst")),
    ("Clause 5 / 07", os.path.join(REPO, "contribution", "src", "doc", "chapters", "07_requirements.rst")),
]
CONF = os.path.join(REPO, "d4conformance", "conformance.py")

REQ_LINE = re.compile(r"^\*\*(R-\d+\.\d+\.\d+[a-z]?)\*\*\s*(.*)$")
HEADING = re.compile(r"^\d+\.\d+\s+(.+)$")


def parse_requirements() -> list[dict]:
    reqs: list[dict] = []
    for chapter, path in CHAPTERS:
        heading = ""
        lines = open(path, encoding="utf-8").read().splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            m = HEADING.match(line.strip())
            if m:
                heading = m.group(1).strip()
            m = REQ_LINE.match(line)
            if m:
                rid, text = m.group(1), m.group(2).strip()
                # gather continuation lines until a blank line
                j = i + 1
                while j < len(lines) and lines[j].strip():
                    if REQ_LINE.match(lines[j].rstrip()) or HEADING.match(lines[j].strip()):
                        break
                    text += " " + lines[j].strip()
                    j += 1
                reqs.append({"id": rid, "chapter": chapter, "section": heading, "text": text})
                i = j
                continue
            i += 1
    # de-duplicate by id, first occurrence wins
    seen, out = set(), []
    for r in reqs:
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out


def parse_tests() -> list[dict]:
    src = open(CONF, encoding="utf-8").read()
    pairs = re.findall(r'\(\s*"(T-\d+)"\s*,\s*"(R-\d+\.\d+\.\d+[a-z]?)"\s*,\s*([A-Za-z0-9_]+)\s*\)', src)
    if not pairs:
        pairs = [(m[0], m[1], "") for m in re.findall(r'"(T-\d+)"\s*,\s*"(R-\d+\.\d+\.\d+[a-z]?)"', src)]
    tests, seen = [], set()
    for tid, rid, fn in pairs:
        if (tid, rid) in seen:
            continue
        seen.add((tid, rid))
        tests.append({"id": tid, "requirement": rid, "function": fn})
    return tests


def main() -> int:
    reqs = parse_requirements()
    tests = parse_tests()
    by_req: dict[str, list[dict]] = {}
    for t in tests:
        by_req.setdefault(t["requirement"], []).append(t)

    max_clause = "5.1"
    for r in reqs:
        m = re.search(r"$", "")
        r["tested_by"] = [t["id"] for t in by_req.get(r["id"], [])]
        r["test_functions"] = [t["function"] for t in by_req.get(r["id"], []) if t["function"]]
        r["status"] = "tested" if r["tested_by"] else "untested"
        r["gap"] = "" if r["tested_by"] else "no executing test in d4conformance/conformance.py"

    tested = [r for r in reqs if r["status"] == "tested"]
    untested = [r for r in reqs if r["status"] == "untested"]

    table = {
        "schema": "uibc-judgement/1",
        "generated_from": {
            "chapters": [c for c, _ in CHAPTERS],
            "tests": "d4conformance/conformance.py",
            "repo": "d4-evidence-authorization",
        },
        "summary": {
            "requirements_defined": len(reqs),
            "requirements_tested": len(tested),
            "requirements_untested": len(untested),
            "tests": len({t["id"] for t in tests}),
            "mappings": len(tests),
        },
        "requirements": reqs,
        "tests": tests,
        "gaps": [
            {"requirement": r["id"], "section": r["section"], "reason": r["gap"], "text": r["text"]}
            for r in untested
        ],
        "claim": {
            "boundary_sentence": (
                "A uibc PASS means: within the observed evidence boundary, no violation was detected. "
                "It does not claim the agent was correct, safe, or wise; that the recorded inputs were true "
                "or complete; or that any real-world outcome followed."
            ),
            "not_claimed": [
                "that an untested requirement is unimplementable, or that a tested one is fully covered",
                "that this table is a conformance result for any implementation other than the suite itself",
                "that the count of tests implies the count of requirements covered",
            ],
        },
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(table, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("json:", OUT_JSON)
    print("requirements", len(reqs), "tested", len(tested), "untested", len(untested), "tests", len({t['id'] for t in tests}))

    s = table["summary"]
    rows = []
    for r in reqs:
        cls = "untested" if r["status"] == "untested" else "tested"
        tested_by = ", ".join(r["tested_by"]) if r["tested_by"] else "—"
        fns = "<br>".join(html.escape(f) for f in r["test_functions"]) if r["test_functions"] else ""
        rows.append(
            f'<tr class="{cls}"><td class="rid">{html.escape(r["id"])}</td>'
            f'<td class="sec">{html.escape(r["section"])}</td>'
            f'<td class="txt">{html.escape(r["text"])}</td>'
            f'<td class="tid">{html.escape(tested_by)}</td>'
            f'<td class="fn">{fns}</td>'
            f'<td class="gap">{html.escape(r["gap"]) if r["gap"] else ""}</td></tr>'
        )

    doc = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>D4 判定表 · 需求→测试→证据→缺口</title>
<style>
:root{{--ink:#0f172a;--muted:#5b6b82;--line:#e2e8f0;--ok:#0b7a4b;--okbg:#effaf3;--bad:#a4231e;--badbg:#fdf0ef;--accent:#1d4ed8}}
*{{box-sizing:border-box}}body{{margin:0;padding:32px 28px;font:15px/1.55 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif;color:var(--ink);background:#fbfcfe}}
h1{{font-size:26px;margin:0 0 6px}}sub{{color:var(--muted);display:block;margin-bottom:20px}}
.stats{{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0 6px}}
.stat{{border:1px solid var(--line);border-radius:12px;padding:14px 18px;background:#fff;min-width:150px}}
.stat b{{display:block;font-size:26px;line-height:1.2}}
.stat span{{color:var(--muted);font-size:13px}}
.bar{{height:8px;border-radius:6px;background:var(--line);margin:16px 0 24px;overflow:hidden;display:flex}}
.bar i{{display:block;height:100%}}
.bar .a{{background:var(--ok)}}.bar .b{{background:var(--bad)}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13.5px}}
th{{background:#f1f5fb;text-align:left;padding:10px 12px;font-weight:600;border-bottom:1px solid var(--line);font-size:13px}}
td{{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
tr.tested td.rid{{color:var(--ok);font-weight:600}}tr.untested{{background:var(--badbg)}}
tr.untested td.rid{{color:var(--bad);font-weight:600}}
td.rid{{white-space:nowrap;font-family:ui-monospace,Consolas,monospace}}
td.sec{{color:var(--muted);font-size:12.5px;white-space:nowrap}}
td.tid{{font-family:ui-monospace,Consolas,monospace;white-space:nowrap}}
td.fn{{color:var(--muted);font-family:ui-monospace,Consolas,monospace;font-size:12px}}
td.gap{{color:var(--bad);font-size:12.5px}}
.foot{{margin-top:22px;padding:14px 16px;border-left:3px solid var(--accent);background:#f4f7ff;font-size:13px;color:#243b6b}}
.legend{{margin:10px 0 0;color:var(--muted);font-size:12.5px}}
</style></head><body>
<h1>D4 判定表 · 需求 → 测试 → 证据 → 缺口</h1>
<sub>由 <code>build_judgement_table.py</code> 从规范源文件现读生成，本页无手打数字 · schema <code>uibc-judgement/1</code></sub>
<div class="stats">
  <div class="stat"><b>{s['requirements_defined']}</b><span>已定义需求</span></div>
  <div class="stat"><b>{s['requirements_tested']}</b><span>有执行测试</span></div>
  <div class="stat"><b>{s['requirements_untested']}</b><span>无执行测试（缺口）</span></div>
  <div class="stat"><b>{s['tests']}</b><span>测试用例</span></div>
  <div class="stat"><b>{s['mappings']}</b><span>需求-测试映射</span></div>
</div>
<div class="bar"><i class="a" style="width:{s['requirements_tested']/max(1,s['requirements_defined'])*100:.1f}%"></i><i class="b" style="width:{s['requirements_untested']/max(1,s['requirements_defined'])*100:.1f}%"></i></div>
<table><thead><tr><th style="width:104px">需求</th><th style="width:130px">章节</th><th>需求原文</th><th style="width:80px">测试</th><th style="width:210px">执行函数</th><th style="width:190px">缺口</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table>
<p class="legend">绿=有执行测试；红=无执行测试。缺口列写明原因，不并入任何百分比。</p>
<div class="foot">{html.escape(table['claim']['boundary_sentence'])}<br><br>
不含主张：{'；'.join(html.escape(x) for x in table['claim']['not_claimed'])}</div>
</body></html>
"""
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)
    print("html:", OUT_HTML)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

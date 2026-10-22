#!/usr/bin/env python3
"""sqltk-know 回归测试：阈值 / 指标字典 / 故障指纹

不依赖 pytest / 真实数据库。直接运行：

    python tests/test_dbknow.py
"""

from __future__ import annotations

import os
import pathlib
import sys
import tempfile

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "src"))
# 开发期：兄弟仓库用源码目录；正式使用请 pip install（见 README）
for _sib in ():
    _p = _HERE.parent.parent / _sib / "src"
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

os.environ.setdefault("DBT_LOG_LEVEL", "ERROR")
_TMPDIR = tempfile.mkdtemp(prefix="dbt-dbknow-")
os.environ.setdefault("DBT_STORE", os.path.join(_TMPDIR, "store.db"))


PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSED.append(name)
    else:
        FAILED.append(f"{name}  << {detail[:300] if detail else ''}")


def section(title: str) -> None:
    print(f"\n── {title}")



from dbknow.metrics import diff_counter, diff_raw_counters, is_counter, COUNTER_ALIASES
# 13.1 counter/gauge 差分
check("qps 标记为 counter、connections_used 为 gauge",
      is_counter("qps") and not is_counter("connections_used"))
_r, _w = diff_counter(1000.0, 2000.0, 60.0)
check("counter 差分：正常速率", _r == 16.6667 and _w is None, f"{_r}")
_r, _w = diff_counter(2000.0, 1000.0, 60.0)
check("counter 差分：值回落判定重启并作废", _r is None and _w == "restart")
_rates, _warns = diff_raw_counters({"qps": 600}, {"qps": 1200}, 60.0)
check("批量差分产出速率", _rates.get("qps") == 10.0 and not _warns)


# ==================================================================
print("\n" + "=" * 60)
print("通过 %d 项，失败 %d 项" % (len(PASSED), len(FAILED)))
if FAILED:
    print("\n失败明细：")
    for _f in FAILED:
        print("  ✗", _f)
    raise SystemExit(1)
print("全部通过")

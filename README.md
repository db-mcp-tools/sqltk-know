# sqltk-know

**数据库引擎知识层** · Library（不是 MCP）

> 零历史、零数据库、零第三方依赖 —— 客户还没给任何数据时，判断能力的来源。

> 发行名 `sqltk-know`，import 包名 `dbknow`（`pip install sqltk-know` → `import dbknow`）—— 两者不同是刻意的，原因见顶层 README「命名」。

## 安装

```bash
pip install sqltk-know                        # 从 PyPI
pip install ./sqltk-know                      # 从源码（在工具链根目录执行）
```

## 三块知识

| 模块 | 内容 |
|---|---|
| `dbknow.baselines` | 各引擎阈值（连接数、延迟、缓冲池…）+ 版本能力位。每条都带 `why` 与 `ref`，可引用不可瞎编 |
| `dbknow.metrics` | 逻辑指标字典：指标名归一、单位、默认告警线、**counter/gauge 二分**与差分管道 |
| `dbknow.signature` | 18 种故障指纹：症状 → 检查项 → 成因 → 处置 → 升级标准 |

## 为什么 counter/gauge 要在这里

`Queries`（MySQL）这类自启动以来只增不减的值，直接当 QPS 用是**错的**。
`diff_raw_counters()` 负责差分；值回落判定实例重启、该窗口速率作废并告警。
这条规则属于「引擎知识」而不是某个 MCP 的私有实现，所以放在这里。

## 知识的来源与更新

阈值来自官方文档与公开最佳实践，`ref` 字段写明依据。客户现场标定出的更精确阈值，
应该回写到 `sqltk-store` 的实例基线里（每个客户自己的 p95），而不是改这里 ——
**通用知识与个案数据必须分开**，否则一次客户调优会污染所有客户。

## 开发

```bash
python tests/test_dbknow.py
```

## 许可

MIT © 2026 罗文星 —— 见 [LICENSE](LICENSE)。

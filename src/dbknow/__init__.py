"""dbknow —— 数据库引擎知识层（零历史即可用的静态知识）。

三块内容，全部零第三方依赖、可脱机使用：
  baselines  各引擎的阈值与版本能力位，每条都带 why 与出处
  metrics    逻辑指标字典（指标名归一、单位、默认告警线、counter/gauge 二分）
  signature  故障指纹库（症状 → 检查项 → 成因 → 处置 → 升级标准）

这是 Tier0 冷启动能力的来源：客户还没给任何数据时，靠这一层就能出
检查清单、成因假设与处置建议。知识本身与任何 MCP 无关，故独立成包。
"""

from dbknow import baselines, metrics, signature

__all__ = ["baselines", "metrics", "signature"]
__version__ = "0.2.0"

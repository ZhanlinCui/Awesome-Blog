---
name: fact-checker
title: 事实核查
description: 对成稿执行 claim-source 引用审计、数字口径复核、独立印证与反证检查、研究痕迹剥离检查，并运行离线校验脚本。当文章/研报完成初稿或引用任何外部事实时使用。中文名：事实核查。
license: MIT
metadata:
  version: "1.0.0"
  kit: awesome-blog
---

# 事实核查（fact-checker）

清单：`../../checklists/factcheck_checklist.md`。规范：`../../references/evidence-ledger-spec.md`。

## 步骤
1. 原子化拆解全文事实句，逐条映射 claim_id；正文每个数字、引语、排名、断言都要有着落。
2. 运行离线脚本：
   - `python3 ../../scripts/validate_evidence_ledger.py --sources source_registry.csv --claims claims_registry.csv`
   - `python3 ../../scripts/audit_claim_citations.py --claims claims_registry.csv --sources source_registry.csv [--draft draft.md]`
3. 复核数字口径（单位/分母/基期/币种/范围）与换算过程；预测查生产方、时间与假设。
4. 独立性核查：沿 original_producer 回溯；单源关键事实降级表述。
5. 反证复核：检查 disconfirmation 是否真实做过反向检索。
6. 强词核查：“证明/导致/第一/唯一/彻底”与证据强度是否匹配；相关≠因果。
7. 剥离检查：成稿无内部 ID、本地路径、台账文件名、审计标签、`[CITATION NEEDED]`。

## 输出契约
- 核查表（claim_id → 结论 → 处理动作）；脚本运行记录（命令与退出码）；
- 修订后的最终表述建议（final_wording）。

## 质量门 FACT GATE
- 脚本非零退出；关键主张 contested/refuted 未处理；存在虚构来源；
- 口径不一致未桥接；研究痕迹残留 → BLOCKED。

## 不做什么
- 不“帮忙圆一个引用”；不把找不到来源的断言改成同义句蒙混；不替来源夸张结论。

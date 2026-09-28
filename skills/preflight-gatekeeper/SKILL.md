---
name: preflight-gatekeeper
title: 发布前门
description: 交付前的最终质量门：运行离线 preflight 脚本，按清单核查事实/代码/研究痕迹/合规/交付物，汇总 rubric 扣分并做放行裁决。当稿件准备交付给作者前使用。中文名：发布前门。
license: MIT
metadata:
  version: "1.0.0"
  kit: awesome-blog
---

# 发布前门（preflight-gatekeeper）

“发布前”指**把本地成稿交给作者本人手动上传之前**。本技能与任何平台之间没有连接动作。

## 步骤
1. 运行：`python3 ../../scripts/preflight.py --draft deliverables/final.md --workdir .`
   （研报追加 `--ledger` 等参数，脚本帮助为准）。
2. 按 `../../checklists/preflight_checklist.md` 五大块逐项确认。
3. 汇总各维度结果，用 `../../templates/rubric.md` 打分，**必须附扣分项清单**；
   分数仅用于内部放行与同稿前后对比，不构成任何外部效果承诺。
4. 裁决：
   - 无阻断 → PASS / PASS-WITH-NITS，允许交付；
   - 有阻断 → BLOCKED，退回责任阶段，重过对应门；
   - 机器判不了 → NEEDS-HUMAN，作者在工作台账记录决策后放行（记录不入成稿）。
5. 最后一次扫描研究痕迹与禁止内容：内部 ID、本地路径、`[CITATION NEEDED]`、
   任何平台登录/凭据/自动发布相关字样（套件中本不应存在，出现即视为污染）。

## 输出契约
- preflight 报告（脚本输出 + 清单勾选 + 扣分项 + 裁决 + 时间）。
- 交付物路径：本地 Markdown/HTML；并提示作者：上传发布由其本人手动完成。

## 不做什么
- 不因为“赶时间”放行阻断项；不删占位符假装通过；不对外解释成“已达到可发布/可获流量标准”。

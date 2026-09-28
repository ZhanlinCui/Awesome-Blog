---
name: research-evidence
title: 研究取证与证据台账
description: 建立研究契约与来源/主张双台账，执行多源交叉验证、独立印证判定（聚合回溯原始生产者）、反证尝试、口径登记。当任务需要查资料、找证据、管理引用与来源时使用。中文名：研究取证。
license: MIT
metadata:
  version: "1.0.0"
  kit: awesome-blog
---

# 研究取证与证据台账（research-evidence）

规范全文：`../../references/evidence-ledger-spec.md`。

## 触发
任何需要外部事实支撑的写作/研究任务；或作者丢来一堆链接要求梳理证据。

## 输入
冻结的 brief/task_spec；检索关键词；作者提供的初始材料。

## 步骤
1. 建立工作目录三件套：`task_spec.md`、`source_registry.csv`、`claims_registry.csv`
   （模板在 `../../templates/`）；研报加 `market_assumptions.csv`。
2. 按来源优先级检索：官方/监管/财报/学术优先；每条来源登记 title/publisher/url/
   source_type/retrieval_date/original_producer/method/limitations。
3. **独立性判定**：沿 original_producer 回溯；聚合转载不算第二来源。
4. 主张原子化登记：fact/statistic/estimate/calculation/forecast/opinion 分类，
   映射 source_ids；关键事实要求 2 个独立来源，否则降级表述或补证。
5. **反证尝试**：对关键主张主动构造反向检索词，记录在 disconfirmation。
6. 口径登记：数字必须带单位、范围、时间、币种、基期；口径不一先做桥接表。
7. 运行 `../../scripts/validate_evidence_ledger.py` 做完整性校验。

## 输出契约
- 完整三件套 CSV/MD；证据缺口清单（转为正文 `[需补：…]` 或补证任务）。

## 质量门 RESEARCH GATE（阻断项）
- 来源必填字段缺失；关键主张零独立印证且未降级；来源无法定位（疑似模型编造）；
- 聚合被当作独立印证；脚本校验失败。

## 不做什么
- 不凭模型记忆生成文献；不把通稿与原文算互证；不抹平来源冲突；
- 不获取付费墙后/非公开/需越权访问的材料；不处理任何平台账号凭据。

# 证据台账规范（Evidence Ledger Spec）

版本：1.0 ｜ 适用：research-evidence、fact-checker、deep-research-report 及全部需要取证的技能。

本套件把“研究”和“成稿”严格分离。研究期所有材料落在**工作目录**的台账文件里；
成稿交付前必须剥离一切内部 ID 与路径。

## 1. 三件套

研究一个选题时，工作目录至少包含三个文件（模板见 `templates/`）：

1. `task_spec.md`：研究契约——要回答的问题、读者、决策用途、范围边界、检索截止日期。
2. `source_registry.csv`：来源登记册，每条来源一行，字段见下。
3. `claims_registry.csv`：主张登记册，每条事实性主张一行，映射到来源 ID。

研报类选题额外使用 `evidence_ledger.csv`（在 source/claims 之上记录方法、局限与反证尝试）
与 `market_assumptions.csv`（市场测算的全部假设与取值）。

## 2. 来源登记册字段（source_registry.csv）

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| source_id | 是 | 本地编号，如 `S007`；只在研究期使用，成稿中必须移除 |
| title | 是 | 来源标题（原题语言） |
| publisher | 是 | 发布机构/站点/出版方 |
| url | 否* | 可在线获取时填写；付费库、纸质来源写检索位置描述 |
| source_type | 是 | official_stat / regulator / filing / company_official / academic / media / aggregator / community / other |
| retrieval_date | 是 | YYYY-MM-DD |
| original_producer | 条件 | 若本来源是转载/聚合，填写原始生产方；并在 original_source_id 关联其原始出处条目 |
| method | 条件 | 数据型来源必须写：口径、样本、采集方式 |
| limitations | 是 | 已知局限（样本偏差、时间陈旧、利益相关、样本量等）；没有也要写“未发现” |
| accessed_lawfully | 是 | yes/no：是否通过公开合法渠道获取 |

\\* 无 URL 的来源必须给出可复核的检索路径（数据库名、报告全名、页码）。

### 独立性规则

- 聚合商（转载、二手综述、内容农场）与其引用的原始出处**不是相互独立的印证**。
- 判断“多源印证”时，沿 original_producer 链回溯到真正的原始生产者；
  同一原始生产者的不同分发渠道仍算一个来源。
- 单一来源支撑的关键主张必须：降级表述（“据 X 单方面披露……”）或补证，二者必居其一。

## 3. 主张登记册字段（claims_registry.csv）

| 字段 | 说明 |
| --- | --- |
| claim_id | 本地编号，如 `C012` |
| statement | 主张的一句话表述（含数字时把数字写全） |
| claim_type | fact / statistic / estimate / calculation / forecast / opinion / recommendation |
| source_ids | 支撑来源 ID，分号分隔；计算型填 `CALC:` 加测算记录 ID |
| independent_sources | 独立来源数量（按上条回溯后的数量） |
| status | verified / contested / single_source / refuted / placeholder |
| disconfirmation | 为证伪它而主动寻找的反证，及结果（未找到/找到后如何修正） |
| final_wording | 核查后允许进入成稿的最终表述（含必要的限定语） |

### 主张类型与举证要求

- fact：至少 1 个高质量来源；关键事实要求 2 个独立来源或显式降级。
- statistic：来源 + 口径（单位、范围、时间、币种、基期）+ 复算或转述页码。
- estimate / forecast：必须带生产方、时间、方法或假设区间；禁止写成既成事实。
- calculation：输入项各自可溯，计算由 `market_sizing.py` 等确定性脚本复算。
- opinion / recommendation：明确归属到具体主体，不得伪装成事实。

## 4. 成稿前剥离规则

交付稿（`deliverables/` 中的 Markdown/HTML）中不得出现：

- `S007`、`C012` 这类内部 ID；
- 本地绝对路径、台账文件名、“见 claims_registry 第 X 行”等审计标签；
- `[CITATION NEEDED]` 等内部批注（未补的内容应回到作者确认环节，不得带病交付）。

允许保留的只有**面向读者的正常引用**：机构名、报告名、链接、年份、页码。

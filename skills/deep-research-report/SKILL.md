---
name: deep-research-report
title: 行业深研报告
description: 科技行业与金融/产业深度研究报告的全流程技能：研究契约、来源与主张双台账、claim-source 追溯、反证尝试、口径锁定、TAM/SAM/SOM 双路径测算与情景敏感性、研究痕迹与成稿分离、编辑门。当用户要写行业研究、产业分析、市场测算、Deep Research 报告时使用。中文名：行业深研报告。
license: MIT
metadata:
  version: "1.0.0"
  language: "zh-CN/en"
  kit: awesome-blog
---

# 行业深研报告（deep-research-report）

> **名称对照**：中文名「行业深研报告」⇄ 机器名 `deep-research-report`。

自包含的深度研究栈。输出的是**证据可审计**的本地报告（Markdown/HTML）：
每条主张可追溯到来源、每个数字有口径与复算、每个结论有反证尝试记录。
不提供投资/法律/税务/监管建议，不做确定性买卖结论。

## 何时使用 / 不使用

- 适用：行业扫描、产业链分析、竞争格局、公司/产品深研、市场规模测算（TAM/SAM/SOM）、
  预测与情景敏感性、技术趋势 Deep Research。
- 不适用：纯技术教程（`tech-blog-en` / `dev-post-zh`）；只需几篇资料摘要的轻量任务
  （直接用 `research-evidence` + `content-research-writer` 即可）。

## 关于外部研究后端（说明，不内置、不绑定）

- 本技能是**宿主无关的工作流契约**：检索动作可由宿主自身联网能力、用户自行部署的
  研究工具或手工检索完成；套件脚本全部离线、仅用 Python 标准库。
- 用户可自选部署开源 Deep Research 后端（如 GPT Researcher 等）作为检索来源之一。
  **许可提示**：GPT Researcher 仓库 README 标注 MIT，但 GitHub API 识别为 Apache-2.0，
  两者存在矛盾，且其工具输出质量需自行评估；本套件**不包含其任何代码或文案**，
  其产出也必须像其他来源一样进入来源登记册、标注方法与局限，不享受“免检”。
- 对争议性选题，可采用多视角提问/模拟对辩的综述式提问方法（思路受 STORM 等
  MIT 项目启发，方法为本套件原创表述）。

## 工作流

### 阶段 1 · 研究契约（research-evidence）
填 `templates/task_spec.md`：决策问题、读者、重要性阈值、范围、**口径约定**
（指标定义、单位、币种、基期、名义/实际、存量/流量、总额/净额）、检索截止日期。
**CONTRACT GATE**：口径未锁定 → 后续一切测算 BLOCKED。

### 阶段 2 · 系统取证（research-evidence）
- 优先级：官方统计/监管文件 > 公司公告财报招股书 > 透明方法的学术与行业研究 > 媒体 > 社区。
- 每条来源按 `evidence-ledger-spec` 登记方法与局限；沿 original_producer 回溯原始生产者；
  聚合与被聚合来源不构成独立印证。
- 利益相关来源（厂商自述、卖方研报）显式标注，结论与之对冲。
- 数据型来源必须记录：口径、样本、采集/发布时间、与 task_spec 口径是否一致；
  不一致先做口径桥接表，不得直接相加。

### 阶段 3 · 主张—证据—反证台账
`claims_registry.csv` 逐条登记，区分 fact/statistic/estimate/calculation/forecast/opinion。
对支撑核心结论的关键主张，**主动用反向关键词与对立来源做反证尝试**并记录结果；
争议数字在成稿中以区间或“不同机构分歧”呈现，不得二选一伪装成确定值。

### 阶段 4 · 市场测算（market sizing）
- 填 `templates/market_assumptions.csv`：每个假设一个 ID、取值、单位、来源或“假设”标记、情景。
- **TAM/SAM/SOM** 同时给：
  - 自上而下（top-down）：宏观基数 × 渗透率等，每个乘数可溯；
  - 自下而上（bottom-up）：客户数 × ARPU / 产能 × 单价等，每个加总可溯；
  - **两条路径必须对账**：差异超出阈值（默认 ±20%，可在 task_spec 改）必须解释，
    或回到假设修正，不许选好看的一条。
- **情景与敏感性**：至少 bear/base/bull 三情景；对关键假设（增速、渗透率、价格）
  做单变量敏感性，指出结论对哪个假设最脆弱。
- 全部算术由离线脚本确定性复算：
  `python3 scripts/market_sizing.py --assumptions market_assumptions.csv ...`
- **MATH GATE**：脚本不通过、假设无来源且无作者签字、双路径差异未解释 → BLOCKED。
- 输出明确标注：这是对“你提供的假设”的算术核算，**不构成投资建议**。

### 阶段 5 · 结构化成稿（本地写作）
建议结构（可裁剪）：摘要（结论先行+关键数字区间）→ 问题定义与口径 → 方法与来源说明 →
市场/行业事实层 → 产业链与竞争格局 → 测算与情景（含假设表与敏感性）→
反方观点与不确定性 → 结论与边界 → 附录（来源清单、术语、口径桥接表）。
写作协作可调用 `content-research-writer`；编辑门采用原创的编辑规则：
骨架/数字锁定、诊断+处方、字数纪律。

### 阶段 6 · 审计与事实核查（fact-checker）
- `validate_evidence_ledger.py`（台账完整性）+ `audit_claim_citations.py`（引用审计）。
- 复核：所有正文数字都能在台账找到；图表数字与正文一致；脚注/链接真实可达或可定位。

### 阶段 7 · 编辑门（editor-polish-zh/en + seo-geo-optimizer）
- 结论与证据强度匹配：估算不写成事实、相关不写成因果、单源不写成共识；
- 删除“内部黑话”和无信息量形容词；中英文稿分别过对应编辑技能；
- 可发现性检查仅为内部启发式，不做任何效果承诺。

### 阶段 8 · Preflight + 研究痕迹剥离
- `scripts/preflight.py` 0 阻断；**成稿中不得出现** S0xx/C0xx 内部 ID、
  本地路径、台账文件名、“见附录第 X 行”类审计标签；面向读者的只保留
  机构名、报告名、链接、年份、页码等正常引注。
- 交付物：`deliverables/report-final.md`（本地文件，作者自行决定后续分享方式）。

### 阶段 9 · 更新
数据有时效：按 refresh-and-decay 规范定期重跑关键假设与情景，更新说明中披露变化。

## 不做什么

- 不给买入/卖出/目标价式结论，不替代持牌专业意见。
- 不把厂商白皮书数字当市场共识；不隐藏来源冲突。
- 不做没有假设表的“黑箱测算”；不输出单点确定值掩盖区间。
- 不把检索工具的模型输出直接当事实；它只是待核查来源。
- 不提供任何平台自动发布能力。

## 资产
- 规范：`../../references/evidence-ledger-spec.md`、`../../references/quality-gates.md`
- 脚本：`../../scripts/market_sizing.py`、`validate_evidence_ledger.py`、`audit_claim_citations.py`
- 模板：`../../templates/task_spec.md`、`source_registry.csv`、`claims_registry.csv`、`market_assumptions.csv`、`rubric.md`

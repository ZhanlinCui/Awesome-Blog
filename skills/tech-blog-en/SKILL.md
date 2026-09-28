---
name: tech-blog-en
title: 英文技术博客
description: End-to-end production of in-depth English-language technical blog posts and developer-community articles (tutorials, deep dives, benchmarks, postmortems, engineering writeups). Use when the user wants to write an English technical article with reader interviews, evidence-backed research, runnable code verification, multi-gate quality contract, editing and SEO/GEO hygiene. 当用户要求写英文技术深度博客、开发者技术文章（教程/原理解析/benchmark/postmortem）时使用。中文名：英文技术博客。
license: MIT
metadata:
  version: "1.0.0"
  language: en
  kit: awesome-blog
---

# 英文技术博客（tech-blog-en）

> **Name mapping 名称对照**：中文名「英文技术博客」⇄ 机器名 `tech-blog-en`。
> 用中文说“写英文技术博客”也应路由到本技能。

一个**自包含、可独立安装**的栈技能：从选题访谈到交付本地英文成稿，内置多阶段质量门
交付契约。它把套件中的共享子技能编排为一条流水线，并可以在协作环节调用横向技能
`content-research-writer`（中文名：协作研究写作）。

## 何时使用

- 写英文教程（how-to）、原理解析（deep dive）、benchmark/性能评测、事故复盘（postmortem）、工程实践总结、SDK/产品技术发布文。
- 读者是工程师/技术决策者，需要代码可信、论证有据。
- 作者愿意按阶段交付、逐阶段过门，而不是一次生成全文。

## 何时**不**使用

- 中文社区/公众号稿 → 用 `dev-post-zh`。
- 行业研究、市场测算型研报 → 用 `deep-research-report`。
- 只想润色一段现成英文 → 直接用共享子技能 `editor-polish-en`。
- 需要“登录某平台自动发布” → **套件不提供此能力**，本技能只交付本地 Markdown/HTML。

## 流水线、输入输出契约与质量门

全程在作者指定的**工作目录**中进行（默认 `./workspace/<slug>/`）。
质量门总则见套件根目录 `references/quality-gates.md`；下文只写本栈特有要求。

### 阶段 0 · Intake 访谈（调用 topic-brief，可联合 content-research-writer）

先问再写，至少问清：目标读者角色与水平、阅读场景、读完能做到什么、文章类型、
目标篇幅与渠道格式、已有素材/代码、读者已有的误解是什么。输出
`templates/article_brief.md` 的填好版本 `01_brief.md`。

- **BRIEF GATE**：读者画像四问任一空白 → BLOCKED；核心论点一句话写不出 → BLOCKED。
- 同时产出 **10 个候选标题**（不同角度：问题式、结论式、数字式、故事式等），作者选定前不定稿题目。

### 阶段 1 · Research 取证（调用 research-evidence）

- 建立 `task_spec.md`、`source_registry.csv`、`claims_registry.csv`（模板在套件 `templates/`）。
- 技术事实优先一手来源：官方文档/changelog/RFC、源码 issue/commit、论文、官方 benchmark。
- 版本号、API 签名、弃用声明、配置项必须记录来源与检索日期。
- **RESEARCH GATE**：关键事实零独立印证（或未降级表述）→ BLOCKED；来源字段缺失 → BLOCKED。

### 阶段 2 · Outline 骨架（调用 collaborative-outline）

- 用 `templates/outline.md`：钩子/张力/核心论点/结尾路径“骨架四件套”由作者锁定；
  每节标注证据状态（有据/待证/纯论述）。
- **OUTLINE GATE**：存在“待证”但无对应 claim 计划的节 → BLOCKED；作者未确认骨架不得开写。

### 阶段 3 · Draft 分段写作（调用 technical-blog-writing）

- 一次只写一节；每节完成即给“诊断+处方”式反馈（可调用 content-research-writer 的逐节反馈）。
- **数字锁定**：没有来源的具体数字一律写 `[需补：数字及来源]`，禁止编造。
- **受保护文本**：代码、CLI 命令、API 名、参数、版本号、文件名不被“润色”改动。
- 所有代码块必须可独立运行或显式标注未运行原因（见阶段 4）。

### 阶段 4 · 技术校验（调用 code-verifier）

- 提取代码块，按语言在隔离环境实际运行；记录命令、环境、结果到 `verification_log.md`。
- benchmark 类：给出硬件/软件环境、配置、日期、重复次数与原始结果，可复现。
- postmortem 类：时间线、影响面、根因分类都要有证据或明确标注“推断”。
- **CODE GATE**：代码未运行且未标注 / 运行失败未修复 → BLOCKED。

### 阶段 5 · Fact-check 事实核查（调用 fact-checker）

- 跑 `audit_claim_citations.py` + `validate_evidence_ledger.py`；按
  `checklists/factcheck_checklist.md` 逐条过；记录反证尝试。
- **FACT GATE**：脚本非零退出 / 关键主张 contested 未处理 → BLOCKED。

### 阶段 6 · Edit 英文润色（调用 editor-polish-en）

- 按其 AI-tone 清单、句子节奏、术语一致性清单修订；编辑只给选项，作者拍板。
- 非英语母语作者的稿件保留其真实声音，不“标准化”成无特征的模板腔。

### 阶段 7 · SEO/GEO 卫生（调用 seo-geo-optimizer）

- 标题、meta description、H 层级、内链外链、alt 文本完整性检查；关键词自然出现。
- 所有结论标注为**内部启发式检查，不构成排名或 AI 引用效果承诺**。

### 阶段 8 · Preflight 发布前门（调用 preflight-gatekeeper）

- 运行 `scripts/preflight.py`；按 `checklists/preflight_checklist.md` 逐项确认；
  用 `templates/rubric.md` 打分并附扣分项（分数仅供改稿前后对比与放行）。
- **DELIVERY GATE**：存在阻断项 → 不交付。剥离全部研究痕迹（内部 ID、本地路径、审计标签）。

### 阶段 9 · 交付（止于本地文件）

- 产物：`deliverables/final.md`（可选 HTML）。**没有任何自动上传/发布后续步骤**；
  是否、何时、上传到哪个平台，全部由作者本人手动完成。

### 阶段 10（可选）· 更新（调用 article-refresh-decay）

- 旧文按 `references/refresh-and-decay.md` 做衰减盘点后重过相关质量门。

## 反例（明确不做什么）

- 不先写文章再“补引用”；不生成看似合理的参考文献列表。
- 不把没跑过的代码写成“运行结果如下”。
- 不为了通顺改写 API 名、参数、版本号。
- 不用营销空话替代技术细节（“革命性的”“极致性能”无证据即删）。
- 不把模型记忆里的接口签名当成事实；必须查当前版本文档。
- 不提供平台登录/自动发布能力，不处理任何凭据。

## 最小调用示例

```text
用户：帮我写一篇英文技术博客，讲我们如何把构建时间从 12 分钟降到 90 秒。
技能：进入阶段 0 访谈 → 产出 01_brief.md 与 10 个标题候选 →
      作者确认后建研究台账 → 列纲锁定骨架 → 逐节写作 →
      实跑构建脚本留证 → 事实核查 → 英文润色 → SEO/GEO 卫生 →
      preflight 0 阻断 → 交付 deliverables/final.md（作者自行上传）。
```

## 资产

- 共享规范：`../../references/quality-gates.md`、`../../references/evidence-ledger-spec.md`
- 模板：`../../templates/`（brief、task_spec、两个登记册、outline、rubric）
- 清单：`../../checklists/`
- 离线脚本：`../../scripts/`（证据台账校验、引用审计、市场测算、preflight）

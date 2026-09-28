# 与 Awesome-Blog 套件的集成约定

本文件说明 `content-research-writer`（Apache-2.0，© ComposioHQ，经适配）如何与
Awesome-Blog 套件（MIT）的三个主栈与共享子技能协作。许可边界见该目录下 `LICENSE`
与套件根目录 `ATTRIBUTION.md`。

## 1. 调用时机

```mermaid
flowchart LR
    A[选题/intake] --> B[协作列纲]
    B --> C[研究取证<br/>research-evidence]
    C --> D[逐节写作+逐节反馈]
    D --> E[事实核查 fact-checker]
    E --> F[编辑润色]
    F --> G[preflight 发布前门]
    G --> H[本地 Markdown/HTML 交付]
```

- A/B/D 的协作体验由 content-research-writer 提供；
- C 必须落到套件证据台账（source/claims 两件套），不能只停留在对话里；
- E/G 由套件确定性质量门执行，分数为内部启发式，不承诺任何平台效果；
- H 永远是本地文件，不存在“自动上传”后续环节。

## 2. 字段对齐

content-research-writer 原生只有自由格式的 research.md。纳入套件后，
研究输出同时满足：

| 协作写作中的概念 | 套件台账字段 |
| --- | --- |
| Research 段的一条 finding | `claims_registry.csv` 一行（claim_id / statement / claim_type / source_ids / status） |
| Citations [1][2] | `source_registry.csv` 一行（source_id / title / publisher / url / source_type / retrieval_date / limitations） |
| “needs source” 批注 | `status=placeholder`，正文写 `[需补：…]` |
| Final review 的 citations 检查 | 由 `scripts/audit_claim_citations.py` 离线执行 |

## 3. 声音保持的执行口径

上游原文中的“suggest / enhance”原则，在本套件中按如下原创口径执行：

- 批注格式为“诊断 + 处方”：先指出问题类型（如证据不足、术语跳跃、逻辑断层），
  再给 2 个以上改写候选并说明各自代价；
- 不直接覆盖作者原句；候选被作者拒绝即关闭该意见；
- 技术稿中代码、命令、API 名、参数、版本号属于“受保护文本”，润色阶段不得改动，
  只能对其周边叙述文字提建议。

## 4. 禁止事项

- 禁止把该技能 Examples 里的虚构机构名/百分比/引语写进真实文章；
- 禁止生成“看起来合理”的参考文献列表充数；
- 禁止在交付稿保留内部 ID、本地路径、审计标签；
- 禁止增加任何平台登录、凭据、自动发布相关内容——本套件到此为止只交付本地成稿。

# 署名与许可声明（ATTRIBUTION）

本仓库（Awesome-Blog「写 Blog 全能 Agent Skills Kit」，下称“本套件”）的**全部原创内容**——
包括但不限于所有 `SKILL.md`、`references/`、`templates/`、`checklists/` 文档以及
`scripts/` 下的校验脚本——均以 **MIT License** 发布（见 [LICENSE](./LICENSE)）。

本套件在设计过程中参考了下列开源项目的**流程思路与结构约定**。除明确标注外，
本套件**未复制任何第三方代码、原文或示例文本**，所有工作流描述均为原创重写。

## 一、MIT / Apache 宽松许可的设计参考（在此署名致谢）

| 项目 | 许可 | 借鉴的设计点（仅思路，文案均原创重写） |
| --- | --- | --- |
| [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) | MIT | “主编排器 + 专项技能”的分层架构、贯穿全生命周期的命令式工作流、发布前多级质量门与交付契约 |
| [samber/cc-skills](https://github.com/samber/cc-skills) | MIT | 访谈式写作 intake（先问清读者与场景再动笔）、多标题候选、分阶段交付；并行检索与多源交叉验证 |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | MIT | 任务规格先行、记忆/子任务编排、中间产物落盘的组织方式 |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | MIT | 面向发布的页面级 SEO 检查清单组织方式 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | MIT（market-research-reports frontmatter 自标） | 证据台账字段模型、claim–source 精确映射、TAM/SAM/SOM 双路径对账、离线确定性脚本的做法（脚本与文案均为原创实现） |
| [rrrrrredy/research-toolkit](https://github.com/rrrrrredy/research-toolkit) | MIT | task_spec / source_registry / claims_registry 三件套、反证尝试、成稿前清除研究痕迹 |
| [geekjourneyx/industry-research](https://github.com/geekjourneyx/industry-research) | MIT | 行业研究的问题拆解与证据分层 |
| [Jiaranbb/report-helper](https://github.com/Jiaranbb/report-helper) | MIT | 研报结构脚手架与结论先行的组织方式 |
| [Guan-Yep/industry-research](https://github.com/Guan-Yep/industry-research) | MIT | 产业链 / 竞争格局的分析维度划分 |
| [Qiyao313/editorial-ai](https://github.com/Qiyao313/editorial-ai) | MIT | 骨架优先（作者锁定核心论点与叙事路径）、数字锁定（禁止编造具体数字）、诊断+处方式批注、字数纪律 |
| [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | MIT | 证据驱动的深度长文评审视角；作者/编辑/读者三视角与术语口语化的思路 |
| [SkillMedev/skills](https://github.com/SkillMedev/skills) | MIT | 技能目录与宿主适配说明的组织方式 |
| [tomzx/agents](https://github.com/tomzx/agents) | MIT | 技能元数据与触发条件的写法 |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | MIT | 研究→写作多阶段流水线的阶段划分 |
| [Infrasity-Labs/dev-gtm-claude-skills](https://github.com/Infrasity-Labs/dev-gtm-claude-skills) | MIT | 开发者向内容的读者—场景匹配 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | 发布前检查项与渠道适配 |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | 技能边界与“何时不要使用”的写法 |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | MIT | 多视角提问、模拟对辩用于争议性选题（未搬用任何代码） |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Apache-2.0（母仓；子技能许可各异） | 仅参考技能集合的编排与索引思路 |
| [anthropics/skills](https://github.com/anthropics/skills) | 混合许可（多数示例 Apache-2.0；docx/pdf/pptx/xlsx 等为 source-available） | 仅参考 Agent Skills 的 `SKILL.md` 规范格式；未使用任何 source-available 文档类技能内容 |
| [lu90/industry-research-skill](https://github.com/lu90/industry-research-skill) | 技能 Apache-2.0；reports/ 示例为 CC BY-NC 4.0 | 仅参考技能结构；从未复制其 CC BY-NC 示例报告中的任何文字 |

## 二、仅作“设计灵感”、文字全部原创重写的限制性许可项目

下列项目采用 CC BY-NC-SA 4.0 / CC BY-NC 4.0 / CC BY 4.0 等限制性许可。
本套件**仅阅读其公开结构以理解产品形态**，没有复制其任何句子、段落、模板或示例；
相关技能的全部文字均为原创撰写，并在此致谢：

| 项目 | 许可 | 仅被参考的结构层面 |
| --- | --- | --- |
| [datawhalechina/vibe-blog](https://github.com/datawhalechina/vibe-blog) | CC BY-NC-SA 4.0 | 研究后追问澄清、分段成文、多角色审核循环的流水线形态（`dev-post-zh` 全部为原创重写） |
| [gwagjiug/technical-writing](https://github.com/gwagjiug/technical-writing) | 技能内容 CC BY-NC-SA 4.0；脚本 MIT | 技术审校分级（阻断 / 重要 / 次要 / 措辞）的思路 |
| [yzhao062/agent-style](https://github.com/yzhao062/agent-style) | CC BY 4.0（且声明不覆盖非英文散文） | 风格规则与正文规则分离的思路；本套件的中文规范全部原创 |
| [onovich/Research](https://github.com/onovich/Research) | CC BY 4.0 | 研究产物组织方式；示例内容未被复制 |

## 三、明确排除的项目

- **[assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)**：其 README 标注 MIT，
  但 GitHub API 识别为 Apache-2.0，存在许可矛盾。本套件**未使用其任何代码或文案**；
  仅在文档中将其列为“用户可自行部署的可选外部研究后端”之一，并提示该许可矛盾。

## 四、商标与第三方内容

- Claude Code、Cursor、Codex、GitHub、知乎、微信公众号、CSDN、掘金等名称均为各自权利人的商标/产品名，
  本套件与上述主体无隶属、授权或背书关系。
- 使用者检索得到的外部网页、报告、数据，其著作权与许可归原权利人所有；本套件要求在证据台账中
  记录来源与使用边界，由使用者合法合规地引用。

## 五、免责声明

本套件中的评分（百分制 rubric）与 SEO/GEO 检查结论均为**本地、内部的启发式质量检查**，
用于帮助发现写作与工程质量问题，**不构成对搜索引擎排名、引用流量或任何商业结果的承诺或保证**；
市场测算脚本仅对使用者自行提供的假设做确定性算术核算，**不构成投资、法律、税务或监管建议**。

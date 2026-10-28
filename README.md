# Dynamic Chat Title Skill (`dynamic-chat-title`)

一个轻量级、零外部依赖、跨平台兼容的 AI Agent Skill，专门解决长对话中**「初始自动生成的标题随主题演进而严重失真」**的痛点。

---

## 1. 功能与设计原则

### 核心功能
- **全景主题识别**：结合完整可见对话历史，识别主线目标、近期连续焦点与上位概念（Umbrella Topic），拒绝仅凭最新一条消息断章取义。
- **防抖与抗干扰（Anti-Thrashing）**：严格区分「连续多轮实质性主题转移」与「单轮跑题/日常闲聊」，避免频繁无意义的标题变动。
- **高信噪比命名规范**：默认与用户语言一致，中文控制在 **6～16 个汉字**，直击核心任务，剔除「关于……的讨论」等废话与敏感信息（PII / 密钥）。
- **诚实宿主适配**：自动区分宿主是否提供原生重命名工具；有工具则静默调用，无工具则提供轻量建议，绝不伪造 API 调用或谎称已修改。

### 设计原则（MVP 极简主义）
- **纯行为规约**：以标准 `SKILL.md` 为唯一入口，不启动后台常驻进程。
- **零外部侵入**：不依赖浏览器插件、数据库、RAG 或额外 MCP 服务。
- **可测试与可解释**：每条触发与抑制规则均有明确边界，配套 10 大标准测试用例与自动化校验脚本。

---

## 2. 目录结构

```text
dynamic-chat-title/
├── SKILL.md                          # Skill 核心入口（通用 YAML + 四级宿主自适应状态机）
├── README.md                         # 项目说明、四大平台+第三方平台安装指南与验证文档
├── agents/
│   └── openai.yaml                   # OpenAI Codex 原生 UI 元数据与 $dynamic-chat-title 调用策略
├── adapters/                         # 第三方平台万能自适应套件（Web客户端 / API网关 / 无Skill宿主）
│   ├── universal_system_prompt.md    # 极简提示词/规则块（适配 Cherry Studio / LobeChat / .windsurfrules / .clinerules）
│   ├── openai_function_tool.json     # 标准 OpenAI Function Calling & MCP Tool Schema（适配 Dify / Coze / FastGPT）
│   └── middleware_regex_parser.py    # 第三方中间件正则提取器 & OpenWebUI Outlet Filter 插件
├── scripts/
│   └── install_and_verify_all.py     # 13+ 平台环境自动嗅探安装器与五层自动化合规验证器
├── examples/
│   └── conversations.md              # 多轮主题演进、单轮跑题防抖与宿主差异示例
└── tests/
    ├── test-cases.md                 # 10 大标准边界测试用例集（TC-01 ~ TC-10）
    └── validate_skill.py             # 零依赖 Python 自动化自检与规则验证脚本
```

---

## 3. 四大原生平台 + 第三方全生态自适应安装矩阵

运行内置的自适应环境嗅探与验证脚本，即可自动探测本机已安装的 Agent 平台（支持 Antigravity、Codex、Claude Code、Cursor 以及 Windsurf、Cline、Roo Code、Trae、OpenCode、Continue.dev、Goose 等 13 种生态），一键完成同步与五层验证：

```powershell
python scripts/install_and_verify_all.py
# 若需强制生成所有未安装第三方平台的目录，可加参数：python scripts/install_and_verify_all.py --all
```

### 3.1 原生 `SKILL.md` 平台（自动探测直装）

| 宿主平台 | 全局安装路径 | 自动触发机制 | 显式手动调用口令 |
| :--- | :--- | :--- | :--- |
| **Google Antigravity** | `~/.gemini/config/skills/dynamic-chat-title/` | 识别 YAML `description` 按需自动挂载 | 自然语言说「评估/更新当前对话标题」 |
| **OpenAI Codex** | `~/.codex/skills/dynamic-chat-title/` | `agents/openai.yaml` (`allow_implicit_invocation: true`) | 输入 `$dynamic-chat-title` |
| **Claude Code** | `~/.claude/skills/dynamic-chat-title/` + `~/.claude/commands/dynamic-chat-title.md` | 识别 Skill 描述自动挂载 | 输入 `/dynamic-chat-title` |
| **Cursor** | `~/.cursor/skills/dynamic-chat-title/` + `~/.agents/skills/dynamic-chat-title/` | 支持环境上下文自动触发 | 输入 `/dynamic-chat-title` 或 `@dynamic-chat-title` |
| **Windsurf / Cline / Roo / Trae / OpenCode / Goose** | 自动嗅探 `~/.codeium/windsurf`、`~/.cline`、`~/.roo`、`~/.trae`、`~/.config/opencode` 等 | 自动同步至对应 `skills/` 或 `rules/` 目录 | 按各端 Skill/Rule 机制自动生效 |

### 3.2 第三方 Web 客户端 / 无 Skill 平台（`adapters/` 万能适配包）

针对不支持本地 `SKILL.md` 文件夹的第三方平台，直接使用 [`adapters/`](./adapters/) 目录下的三件套：
1. **桌面/Web 聊天客户端（Cherry Studio / Chatbox / LobeChat / NextChat / OpenWebUI）与传统 IDE 规则（`.windsurfrules` / `.clinerules` / `.github/copilot-instructions.md`）**：
   直接复制 [`adapters/universal_system_prompt.md`](./adapters/universal_system_prompt.md) 中的 150 Token 极简协议块粘贴至系统提示词或项目规则文件。
2. **第三方智能体编排平台（Dify / Coze / FastGPT / LangChain / 自建网关）**：
   直接导入 [`adapters/openai_function_tool.json`](./adapters/openai_function_tool.json) 中的标准 `update_chat_title` Function Calling / MCP Schema，模型会自动进入 **Tier 1 工具执行模式**。
3. **自建前端 / 网关的解析参考实现**：
   [`adapters/middleware_regex_parser.py`](./adapters/middleware_regex_parser.py) 能从模型回复中提取 `<!-- dynamic-chat-title: 新标题 -->` 或 `💡 建议更新会话标题：「新标题」`，并把结果写入 `body["dynamic_chat_title"]`。**它本身不会修改任何界面标题**——真正改名需要你在自己的前端/网关里读取这个字段，再调用该平台的改名接口（OpenWebUI 不会自动识别这个字段）。

---

## 4. 兼容性与宿主平台限制（重要说明）

为了保证工程诚实性与跨平台稳定运行，使用者需知悉以下两项客观边界：

1. **按需加载机制限制（Progressive Disclosure）**：
   在 Antigravity 等现代 Agent 框架中，`SKILL.md` 默认采用渐进式按需加载（平时仅向模型暴露 `name` 与 `description`）。**仅靠 `SKILL.md` 文件本身无法强行劫持宿主底层每轮自动执行**，除非用户在对话中触发相关意图，或通过宿主的常驻 Rule（`always_on`）显式挂载。
2. **宿主标题修改权限限制**：
   - **模型生成标题 ≠ 宿主实际改名**。
   - 若宿主平台向模型开放了原生重命名工具（Tool/API），模型可直接完成改名；
   - 若宿主平台（如多数标准 Web 聊天界面或未开放 UI 改名接口的 IDE 会话）未提供改名工具，模型**无法直接改动界面标题**，此时会降级为在回复末尾输出 `💡 建议更新会话标题：「xxx」` 供用户复制。

---

## 5. 示例输入与预期结果

| 场景 | 原标题 | 近期对话演变 | 评估动作 | 预期输出标题 |
| :--- | :--- | :--- | :--- | :--- |
| **主题未变** | `Python 入门` | 继续询问 `if/elif/else` 分支写法 | `KEEP` | `Python 入门`（不改名） |
| **单轮跑题** | `Python 函数封装` | 在图书馆突然问了一句高分子化学结构 | `KEEP` | `Python 函数封装`（防抖抑制） |
| **长期转向** | `Python 入门` | 已连续 8 轮设计并编写动态标题 Skill | `RENAME` | `开发动态对话标题 Skill` |
| **多子主题** | `配置 Nginx` | 先后配置 Nginx、SSL 证书与防火墙加固 | `RENAME` | `Linux 服务器部署与安全加固` |

更多完整对话推演请查阅 [`examples/conversations.md`](./examples/conversations.md)。

---

## 6. 测试方法

### 1. 运行自动化结构与规则自检脚本
项目内置了纯 Python 标准库编写的验证脚本，一键检查文件完整性、YAML 头部、10 大用例覆盖度及标题命名合规性：

```powershell
python tests/validate_skill.py
```

预期输出：
```text
=== [dynamic-chat-title] MVP Self-Check & Validation ===
[PASS] All 4 required files exist and are non-empty.
[PASS] SKILL.md YAML frontmatter valid.
[PASS] All 10 standard test cases (TC-01 ~ TC-10) documented in tests/test-cases.md.
[PASS] All 10 simulated decision & title lint checks passed.
=== ALL CHECKS PASSED (100%) ===
```

### 2. 模型行为基准测试
将 [`tests/test-cases.md`](./tests/test-cases.md) 中的 `TC-01` 至 `TC-10` 上下文逐一输入加载了本 Skill 的模型中，核对模型输出的 `KEEP` / `RENAME` 决策是否与预期完全一致。

# 🏷️ Dynamic Chat Title (`dynamic-chat-title`)

> **基于 `SKILL.md` 的对话标题偏移评估规约与多平台适配模板**  
> 评估当前对话标题是否仍能代表主要议题，仅在主线发生持续性偏移或用户显式要求时提出或应用新标题。

---

## ⚠️ 真实能力边界说明（请在使用前阅读）

为了避免产生“装上就能在所有客户端全自动改窗口标题”的误解，本项目明确声明以下真实技术边界：

1. **本项目本质是提示词规约（`SKILL.md`）+ 辅助脚本与模板包，不是后台守护进程或系统定时器。**
   - `SKILL.md` 本身不具备绕过宿主客户端沙箱直接修改 GUI 界面标题的权限。
2. **是否能直接修改宿主左上角/侧边栏的真实 UI 标题，完全取决于宿主是否开放了改名接口：**
   - **OpenAI Codex Desktop**：宿主内置了 `mcp__codex_app__set_thread_title` 工具，模型触发本 Skill 后**可以直接修改客户端真实标题**。
   - **Claude Code / Cursor**：本地脚本 `scripts/rename_host_session.py` 仅作为同步辅助工具尝试更新本地会话元数据（需会话落盘后刷新列表生效），并非官方原生实时 UI 改名 API。
   - **Antigravity / 普通网页端聊天窗口**：宿主未向模型开放会话标题写入接口，本 Skill **只能输出结构化改名建议（供手动复制）**，无法直接改动界面上的标题文字。
3. **关于“每 5 轮周期性巡检”的局限性：**
   - 安装脚本写入 `AGENTS.md` / `CLAUDE.md` 的周期检查规则依赖模型在对话回合中的注意力自觉执行，**不是操作系统的硬件定时任务**。当模型处于高负载编码或长链路工具调用中时，可能会忽略该软性指令，最稳妥的触发方式是显式指令（如“帮我更新一下标题”或调用 `$dynamic-chat-title`）。

---

## 🎯 解决什么问题？

大多数 AI 聊天工具只在**第 1 轮对话**时生成一个静态标题。当对话延续数十轮、话题早已从最初的闲聊转向具体的工程开发或排障时，侧边栏里的旧标题会变得毫无检索价值。

`dynamic-chat-title` 提供了一套克制的评估规则：
- **抗噪防抖**：单轮插科打诨、顺手问个小问题、纯情绪闲聊一律保持 `KEEP`，不乱改标题；
- **持续偏移判定**：只有当新主题成为最近多轮的核心主线（参考阈值：连续约 3 轮或占近 5 轮的 60% 以上）时，才判定 `RENAME`；
- **多子话题伞状概括**：同一大项目下的多个分支自动提炼伞状总标题，避免频繁来回改名。

---

## 🖥️ 各平台实际表现对照表

| 宿主环境 | 触发方式 | 能否直接修改客户端 UI 标题 | 实际行为说明 |
| :--- | :--- | :--- | :--- |
| **OpenAI Codex** | `$dynamic-chat-title` / 自然语言 / `AGENTS.md` 软性提示 | ✅ **支持（原生接口）** | 调用 Codex 内置 `mcp__codex_app__set_thread_title` 实时更新侧边栏与顶部标题 |
| **Claude Code** | `/dynamic-chat-title` / 自然语言 / `CLAUDE.md` 软性提示 | ⚠️ **仅本地文件级辅助** | 可调用 `scripts/rename_host_session.py` 写入本地 JSONL/索引，需刷新列表生效 |
| **Cursor** | `@dynamic-chat-title` / `.mdc` 规则提示 | ⚠️ **仅本地数据库辅助** | 可调用 `scripts/rename_host_session.py` 尝试更新本地 `state.vscdb` 标题字段 |
| **Antigravity** | 自然语言显式触发 / 全局 Rule 提示 | ❌ **不支持直接改 UI** | 宿主未开放改名工具，模型仅在回复末尾输出可复制的新标题建议 |
| **自建 WebUI / API** | 挂载 `adapters/` 模板与中间件 | 🔧 **需开发者自行对接** | 需由外层前端或后端中间件拦截 `<chat_title_patch>` 标签或工具调用后写入数据库 |

---

## 📦 目录结构

```text
dynamic-chat-title/
├── SKILL.md                             # 核心评估规则与四级宿主自适应协议
├── README.md                            # 项目说明与真实能力边界声明
├── agents/
│   └── openai.yaml                      # OpenAI Codex 技能元数据清单
├── adapters/                            # 第三方自建平台接入模板（需开发者配合实现）
│   ├── system-prompt-lite.md            # 极简 System Prompt 补丁
│   ├── tool-schema.json                 # OpenAI / MCP Function Calling 定义模板
│   └── webui-middleware.py              # 正则拦截 <chat_title_patch> 的中间件示例
├── examples/
│   └── conversations.md                 # 6 组多轮对话正反例推演
├── scripts/
│   ├── install_and_verify_all.py        # 本地多端同步安装与验证脚本
│   └── rename_host_session.py           # Claude Code / Cursor 本地会话文件辅助改名脚本
└── tests/
    ├── test-cases.md                    # 10 个标准测试场景 (TC-01 ~ TC-10)
    └── validate_skill.py                # 零依赖自检校验脚本
```

---

## 🛠️ 安装与验证

### 1. 运行自检校验
```bash
python tests/validate_skill.py
```

### 2. 同步安装至本机已装客户端
```bash
python scripts/install_and_verify_all.py
```
该脚本会将技能包同步至本机存在的 `~/.codex/skills/`、`~/.claude/skills/`、`~/.cursor/skills/`、`~/.gemini/config/skills/` 目录，并执行校验。

---

## 📄 开源协议

MIT License

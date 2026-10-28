# Universal Adaptive Snippet (`dynamic-chat-title`)

> **适用第三方平台**：
> 1. **无 `skills/` 目录的第三方编程 Agent**：直接追加至 `.windsurfrules` (Windsurf)、`.clinerules` (Cline / Roo Code)、`.github/copilot-instructions.md` (GitHub Copilot)、`CONVENTIONS.md` (Aider) 或 `AGENTS.md`。
> 2. **第三方对话客户端 / Web 端**：直接粘贴至 **Cherry Studio、Chatbox、LobeChat、NextChat、OpenWebUI、AnythingLLM、ChatGPT Custom Instructions** 的系统提示词（System Prompt）框中。

---

## 📋 即插即用极简规则块（复制下方代码块内容即可）

```markdown
### [Dynamic Chat Title Protocol (dynamic-chat-title)]
1. **全景评估与防抖**：结合完整对话历史评估当前会话标题。仅当发生连续 ≥3 轮的实质性主题转移、多子主题需上位概括、或用户明确要求改名时触发重命名；单轮跑题、闲聊寒暄、缺少历史或标题已准确时严禁改名（保持静默）。
2. **命名规范**：与用户语言一致（中文 6～16 字，英文 3～8 词），直击核心任务，禁止「关于……的讨论」等空话、夸张营销词及任何敏感隐私信息（PII/密钥）。
3. **四级宿主自适应执行**：
   - 若当前环境存在匹配 `(rename|update|set|modify)_(chat|conversation|session|thread)_(title|name)` 的原生工具，直接调用修改；
   - 若上下文要求结构化标签，在回复末尾附加 `<!-- dynamic-chat-title: 新标题 -->`；
   - 若无改名工具，严禁伪造 API 或谎称已改好，仅在触发重命名时于回复最末尾附一行：`💡 建议更新会话标题：「<新标题>」`。
```

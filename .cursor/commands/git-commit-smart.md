# git-commit-smart

## 概述
分析当前所有改动，生成规范的 commit message 并提交。

## 执行步骤

### 第一步：查看当前改动
```powershell
git status
git diff --stat
```
确认有哪些文件被修改、新增或删除。如果没有任何改动，告知用户无需提交。

### 第二步：分析改动内容
- 对每个变更文件执行 `git diff <file>` 查看具体改动
- 理解每处改动的业务意图（新功能、修复、重构、配置变更等）
- 如果改动涉及多个不相关的功能，建议用户拆分为多次提交

### 第三步：安全检查
检查变更文件中是否包含以下内容，如有则**警告用户并排除**：
- `target/` 目录下的编译产物
- `.env` / `application-prod.yml` 等含敏感配置的文件
- 硬编码的密钥、Token、密码
- `.idea/` / `.vscode/` 等 IDE 配置文件（除非有意提交）

### 第四步：生成 commit message
格式：`<type>(<scope>): <简要描述>`

**type 取值：**
- `feat`：新功能
- `fix`：修复 Bug
- `refactor`：重构（不改变功能）
- `perf`：性能优化
- `style`：代码格式调整（不影响逻辑）
- `docs`：文档变更
- `chore`：构建/工具/依赖变更
- `test`：测试相关

**scope 取值：**
使用改动涉及的模块名，如 `ai`、`common`、`model`、`mq-consumer`、`ai-api`

**描述规范：**
- 使用中文
- 简洁明了，一句话说清改动内容
- 示例：`feat(ai): 新增小程序知点流水排行榜接口`

如果改动较大，生成多行 message：
```
feat(ai): 新增用户反馈功能

- 新增 UserFeedback 实体类和 DAO
- 新增提交反馈和查询反馈接口
- 反馈记录支持分页查询
```

### 第五步：确认并提交
将生成的 message 展示给用户，等待用户确认后再执行。

**重要：本项目在 Windows PowerShell 环境下运行，禁止使用 bash heredoc 语法。**

- **单行 message**：直接使用 `-m` 参数
  ```powershell
  git add <相关文件>
  git commit -m "feat(ai): 简要描述"
  ```
- **多行 message**：使用多个 `-m` 参数（每个 `-m` 会自动生成一个段落）
  ```powershell
  git add <相关文件>
  git commit -m "feat(ai): 新增用户反馈功能" -m "- 新增 UserFeedback 实体类和 DAO" -m "- 新增提交反馈和查询反馈接口" -m "- 反馈记录支持分页查询"
  ```

### 第六步：确认结果
```powershell
git push
git log --oneline -3
```
输出最近 3 条 commit 确认提交成功。

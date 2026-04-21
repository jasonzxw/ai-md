# dev-workflow

## 概述
开发工作流导航。自动检测当前分支和代码状态，判断所处开发阶段，推荐下一步该执行的操作。

## 执行步骤

### 第一步：采集当前状态
并行执行以下命令，采集环境信息：
```bash
git branch --show-current
git status --short
git log --oneline -1
git log master..HEAD --oneline
```

从以上输出中提取：
- **当前分支名**（是否为 master？是否为功能分支？）
- **工作区状态**（是否有未提交的改动？）
- **领先 master 的提交数**（开发进度如何？）

### 第二步：判断阶段并推荐操作

根据采集到的状态，按以下规则判断当前所处阶段，并给出推荐：

---

#### 情况 A：当前在 master 分支
**判定：⓪ 待启动阶段**

推荐操作：
| 序号 | 操作 | 命令 | 说明 |
|------|------|------|------|
| 1 | 转换需求文档 | `/pdf-to-markdown` | 将 PDF 需求文档转为 Markdown，方便阅读和引用 |
| 2 | 生成技术方案 | `/generate-tech-design` | 根据需求描述生成完整技术方案设计文档 |
| 3 | 创建功能分支 | `/create-feature-branch` | 技术方案确认后，基于最新 master 创建功能分支 |

---

#### 情况 B：当前在功能分支，领先 master 0 个提交，无改动
**判定：① 编码阶段（刚开始）**

推荐操作：
| 序号 | 操作 | 命令 | 说明 |
|------|------|------|------|
| 1 | 转换需求文档 | `/pdf-to-markdown` | 如果有 PDF 需求文档，先转为 Markdown |
| 2 | 生成技术方案 | `/generate-tech-design` | 如果还没有技术方案，先设计再编码 |
| 3 | 生成 CRUD 骨架 | `/generate-crud` | 如果需要新建表的增删改查 |
| 4 | 生成 SQL | `/generate-mybatis-sql` | 如果需要新增数据库操作 |
| 5 | 同步 master | `/sync-master` | 如果 master 有新提交需要合入 |

---

#### 情况 C：当前在功能分支，有未提交的改动
**判定：② 编码进行中**

推荐操作：
| 序号 | 操作 | 命令 | 说明 |
|------|------|------|------|
| 1 | 提交代码 | `/git-commit-smart` | 分析改动、编译校验、生成规范 commit |
| 2 | 同步 master | `/sync-master` | 先提交再同步，避免冲突混乱 |

> 注意：`/git-commit-smart` 已内置编译校验，Java 文件变更时会自动执行 `mvn compile` 检查，编译失败将阻止提交。

---

#### 情况 D：当前在功能分支，领先 master ≥1 个提交，工作区干净
**判定：③ 验证 & 收尾阶段**

推荐操作：
| 序号 | 操作 | 命令 | 说明 |
|------|------|------|------|
| 1 | 代码审查 | `/review-code` | 自动审查代码质量和安全性 |
| 2 | Redis 检查 | `/check-redis-usage` | 如果改动涉及 Redis 操作 |
| 3 | 生成测试集 | `/generate-api-test` | 为新接口生成 Postman 测试 |
| 4 | 生成文档 | `/generate-api-doc` | 为新接口生成业务流程文档 |
| 5 | **上线前检查** | `/pre-launch-check` | **合并上线前必须执行**，7 维度综合检查 |
| 6 | 同步 master | `/sync-master` | 合并前确保与 master 同步 |
| 7 | 提交代码 | `/git-commit-smart` | 如果审查/文档产生了新改动 |

---

### 第三步：输出导航面板

按以下格式输出：

```
## 🧭 开发工作流导航

**当前分支**：xxx
**工作区状态**：干净 / 有 x 个文件未提交
**开发进度**：领先 master x 个提交
**当前阶段**：[阶段名称]

---

### 推荐下一步
> [根据当前阶段给出最推荐的 1-2 个操作及理由]

### 当前阶段可用命令
[对应阶段的操作表格]
```

底部始终附上全量命令速查表：

```
### 全部命令速查

| 阶段 | 命令 | 一句话说明 |
|------|------|-----------|
| ⓪ 需求 | `/pdf-to-markdown` | 将 PDF 需求文档转为 Markdown |
| ⓪ 设计 | `/generate-tech-design` | 从需求描述生成技术方案设计文档 |
| ⓪ 启动 | `/create-feature-branch` | 基于 master 创建功能分支 |
| ① 编码 | `/generate-crud` | 根据表结构生成全套 CRUD |
| ① 编码 | `/generate-mybatis-sql` | 生成 MyBatis SQL + DAO 方法 |
| ① 编码 | `/sync-master` | 同步 master 最新代码到当前分支 |
| ② 编码 | `/git-commit-smart` | 智能提交（含编译校验） |
| ③ 验证 | `/review-code` | 代码审查（P0~P3） |
| ③ 验证 | `/check-redis-usage` | Redis 使用规范检查 |
| ③ 验证 | `/generate-api-test` | 生成 Postman 测试集合 |
| ③ 验证 | `/generate-api-doc` | 生成接口业务流程文档 |
| ③ 上线 | `/pre-launch-check` | 上线前 7 维度综合检查 |
| ④ 排错 | `/explain-error-log` | 分析异常日志定位根因 |
| ⑤ 收尾 | `/delete-branch` | 删除本地和远程分支 |
| 🔍 随时 | `/git-help` | 自然语言查询 Git 指令用法 |
```

## 注意事项
- 只输出导航信息和推荐，**不要自动执行任何命令**，等待用户选择
- `/explain-error-log` 不属于固定阶段，任何时候遇到报错都可使用
- `/git-help`、`/generate-tech-design` 和 `/pdf-to-markdown` 不受阶段限制，任何时候都可使用
- `/pre-launch-check` 建议在合并到 master 前必须执行一次，作为上线门禁
- 如果用户输入了具体需求（如"我要新增一个接口"），可以直接推荐最相关的命令而非输出完整面板

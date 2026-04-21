# delete-branch

## 概述
删除指定的本地分支和对应的远程分支。分支名由用户输入。

## 输入
- `$BRANCH_NAME`：要删除的分支名称（由用户提供）

## 执行步骤

### 第一步：安全检查
确认当前所在分支：
```bash
git branch --show-current
```
- 如果当前正处于要删除的分支上，**必须先切换到其他分支**（优先 `master` 或 `main`）再执行删除
- 禁止删除 `master`、`main`、`develop` 等受保护分支，若用户输入了这些分支名，直接拒绝并告知原因

### 第二步：确认分支存在性
```bash
git branch -a
```
- 检查本地是否存在该分支
- 检查远程（`origin`）是否存在该分支
- 将检查结果告知用户（例如"本地存在 / 远程存在"）
- 如果本地和远程都不存在，告知用户并终止

### 第三步：确认合并状态
```bash
git log master..$BRANCH_NAME --oneline
```
- 如果该分支有未合并到 `master` 的提交，**警告用户**并列出这些提交
- 等待用户确认是否继续删除

### 第四步：执行删除
经用户确认后，按需执行：

**删除本地分支：**
```bash
git branch -D $BRANCH_NAME
```

**删除远程分支：**
```bash
git push origin --delete $BRANCH_NAME
```

### 第五步：确认结果
```bash
git branch -a
```
输出当前分支列表，确认目标分支已从本地和远程移除，并告知用户删除完成。

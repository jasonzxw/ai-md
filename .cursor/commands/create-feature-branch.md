# create-feature-branch

## 概述
基于最新的远程 master 分支创建规范命名的功能分支，确保起点干净。

## 执行步骤

### 第一步：确认工作区状态
```bash
git status
```
- 如果有未提交的改动，提醒用户先提交或暂存（`git stash`），不要自行处理。
- 如果工作区干净，继续下一步。

### 第二步：同步远程 master
```bash
git fetch origin master
```

### 第三步：生成分支名
根据用户描述的功能需求，生成规范的分支名：
- 格式：`feature/简要描述`（用英文短横线连接，全小写）
- 示例：`feature/add-user-feedback`、`feature/optimize-coin-flow`
- 如果是修复类需求，使用 `fix/` 前缀
- 将生成的分支名展示给用户确认

### 第四步：创建并切换分支
```bash
git checkout -b <分支名> origin/master
```

### 第五步：确认结果
```bash
git log --oneline -3
```
输出当前分支名和最新 commit 信息，确认分支创建成功且基于最新的 master。

# explain-error-log

## 概述
分析用户提供的 Java 异常堆栈或错误日志，快速定位问题根因并给出修复建议。

## 执行步骤

### 第一步：解析异常信息
从用户粘贴的日志中提取：
- **异常类型**：如 `NullPointerException`、`SQLException`、`RedisConnectionFailureException` 等
- **异常消息**：`message` 内容
- **关键堆栈帧**：仅关注 `com.dingzi.zhimo.*` 包下的调用链（忽略框架层堆栈）
- **触发位置**：精确到类名和行号

### 第二步：读取源码上下文
- 根据堆栈中的类名和行号，读取对应源文件的相关代码段（前后各扩展 10 行）
- 如果涉及多个文件（调用链），按调用顺序逐一读取

### 第三步：根因分析
根据异常类型进行针对性分析：

**NullPointerException：**
- 定位哪个变量为 null
- 检查 DAO 查询结果是否未判空
- 检查链式调用中间环节是否可能为 null

**SQLException / MyBatisSystemException：**
- 检查对应的 Mapper XML 语法
- 检查参数绑定是否正确（`#{}` 参数名与方法参数是否匹配）
- 检查 SQL 逻辑是否有误（类型不匹配、字段不存在等）

**RedisConnectionFailureException / RedisCommandTimeoutException：**
- 确认 Redis 配置
- 检查是否有大 Key 操作导致超时
- 检查是否缺少降级逻辑

**HttpClientErrorException / RestClientException：**
- 检查外部服务调用的 URL、参数
- 检查超时配置
- 检查是否有重试和降级机制

**ClassCastException / NumberFormatException：**
- 定位类型转换的具体位置
- 检查数据来源（用户输入、DB 数据）是否有脏数据可能

**其他异常：**
- 结合异常消息和代码上下文，分析可能原因

### 第四步：输出诊断报告

```
## 异常诊断报告

### 异常概要
- **类型**：XxxException
- **消息**：具体 message
- **触发位置**：`类名.java:行号` → `方法名()`

### 根因分析
[详细解释为什么会发生这个异常]

### 问题代码
[展示有问题的代码段，标注问题行]

### 修复方案
[给出具体的代码修改建议]

### 预防措施
[如何避免类似问题再次发生，如增加判空、加 try-catch、加监控等]
```

### 第五步：辅助修复（可选）
如果用户确认，直接在源码中应用修复方案。

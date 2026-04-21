# build-java

## 概述
清理并重新编译 Java 项目（znzmo 多模块），用于解决"找不到主类"、编译产物缺失、依赖冲突等问题。

## 执行步骤

请在**项目根目录**下执行以下 Maven 命令，并在每一步后检查结果：

### 第一步：清理 + 编译
```bash
mvn clean compile
```
- `clean`：删除所有模块的 `target` 目录，清除旧的编译产物
- `compile`：重新编译源代码，生成 `target/classes`
- 如果此步骤成功，输出中会包含 `BUILD SUCCESS`
- 如果失败，立即停止并报告完整错误信息，**不要继续执行后续步骤**

### 第二步（可选）：打包
如果用户需要打包（生成 JAR），继续执行：
```bash
mvn clean package -DskipTests
```
- `-DskipTests`：跳过单元测试加速打包
- 打包成功后，列出各模块 `target/` 下生成的 JAR 文件及大小

### 常见编译错误处理

| 错误类型 | 可能原因 | 建议操作 |
|---------|---------|---------|
| `cannot find symbol` | 依赖模块未编译 | 确保从根 POM 执行而非子模块 |
| `package xxx does not exist` | 依赖缺失 | 先执行 `mvn clean install -DskipTests` |
| `java.lang.UnsupportedClassVersionError` | JDK 版本不匹配 | 项目使用 Java 8，检查 `java -version` |
| 编码错误 `unmappable character` | 文件编码问题 | 检查文件是否为 UTF-8 编码 |

# generate-api-test

## 概述
读取当前打开的 Controller 文件，解析所有接口，生成可直接导入 Postman 的 Collection JSON。

## API 规范
- baseUrl: `localhost:85/ai/api`
- header 认证字段: `Cookie`
- Content-Type: `application/json`

## 执行步骤

### 第一步：解析 Controller
- 读取当前 Controller 文件中所有带 `@RequestMapping` / `@GetMapping` / `@PostMapping` / `@PutMapping` / `@DeleteMapping` 的方法
- 提取以下信息：
  - 类级别的 `@RequestMapping` 路径前缀
  - 每个方法的请求路径、HTTP 方法
  - `@ApiOperation` 中的接口描述
  - `@RequestBody` 对应的实体类结构（需要读取该实体类文件获取字段）
  - `@RequestParam` / `@PathVariable` 参数
  - `@ApiImplicitParams` 中定义的参数说明

### 第二步：读取关联实体类
- 对于 `@RequestBody` 引用的实体类（如 VO、DTO、Entity），读取其源文件
- 提取所有字段名、类型、`@ApiModelProperty` 描述
- 根据字段类型生成合理的测试默认值：
  - String → 填写字段语义相关的示例值
  - Integer/Long → 填 1 或合理数值
  - Boolean → 填 true
  - Date → 填 `2025-01-01 00:00:00`
  - List → 填 `[]`

### 第三步：生成 Postman Collection JSON
按 **Postman Collection v2.1** 格式输出，要求：
- `info.name` 使用 Controller 的 `@Api` 注解值或类名
- 每个接口作为一个 `item`，`name` 使用 `@ApiOperation` 的 value
- URL 拼接规则：`{{baseUrl}}` + 类级路径 + 方法级路径
- GET 接口：参数放在 `url.query` 中
- POST 接口：参数放在 `body.raw` 中（JSON 格式），`mode` 设为 `raw`
- 所有请求的 `header` 统一添加：
  - `Cookie: {{cookie}}`
  - `Content-Type: application/json`
- Collection 级别定义 `variable`：
  - `baseUrl` = `localhost:85/ai/api`
  - `cookie` = `（留空，用户自行填写）`

### 第四步：输出
将完整的 JSON 用代码块输出，用户可直接复制后在 Postman 中 Import → Raw text 导入。

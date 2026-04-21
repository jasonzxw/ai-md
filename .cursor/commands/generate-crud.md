# generate-crud

## 概述
根据用户提供的数据库表结构（建表 SQL）或已有实体类，一次性生成 Entity → DAO → Mapper XML → Service → ServiceImpl → Controller 全套 CRUD 代码。

## 前置准备
在生成代码之前，先阅读以下参考文件以对齐项目风格：
- **Entity 参考**：`znzmo-model/src/main/java/com/dingzi/zhimo/model/entity/` 目录下的已有实体类
- **Controller 参考**：`znzmo-ai/src/main/java/com/dingzi/zhimo/controller/` 目录下的已有 Controller
- **Service 参考**：`znzmo-ai/src/main/java/com/dingzi/zhimo/service/` 及 `service/impl/` 目录
- **DAO + XML 参考**：`znzmo-common/src/main/resources/mybatis/dao/` 目录下的已有 Mapper XML

读取至少 1 个同类文件作为风格模板，确保生成的代码风格一致。

## 生成规范

### Entity（放在 znzmo-model 模块）
- 包路径：`com.dingzi.zhimo.model.entity`
- 使用 `@Data`（Lombok）
- 每个字段加 `@ApiModelProperty(value = "字段说明")`
- 时间字段使用 `java.util.Date` 类型
- 字段加 JavaDoc 注释说明含义

### DAO 接口（放在 znzmo-common 模块）
- 包路径：`com.dingzi.zhimo.dao`
- 使用 `@Mapper` 注解
- 方法命名规范：
  - 查询：`selectXxxByXxx`
  - 新增：`insertXxx`
  - 更新：`updateXxxByXxx`
  - 删除：`deleteXxxByXxx`
- 默认生成方法：`insert`、`selectById`、`selectByAccountId`、`updateById`

### Mapper XML（放在 znzmo-common 模块）
- 路径：`znzmo-common/src/main/resources/mybatis/dao/`
- 包含完整的 `<resultMap>`
- 使用 `<sql>` 片段定义通用列
- 参数一律使用 `#{}` 占位符，禁止 `${}`
- `<where>` + `<if>` 组合处理动态条件

### Service 接口（放在 znzmo-ai 模块）
- 包路径：`com.dingzi.zhimo.service`
- 方法命名与业务语义对齐（如 `add`、`getById`、`update`）

### ServiceImpl（放在 znzmo-ai 模块）
- 包路径：`com.dingzi.zhimo.service.impl`
- 使用 `@Service` + `@Slf4j`
- DAO 注入使用 `@Resource`
- 包含基本的参数校验和日志记录

### Controller（放在 znzmo-ai 模块）
- 包路径：`com.dingzi.zhimo.controller`
- 使用 `@RestController` + `@RequestMapping` + `@Api`
- 每个接口方法加 `@ApiOperation`
- 鉴权逻辑复用项目已有模式：
  ```java
  String accountId = CommonUtils.isEmpty(request.getUserPrincipal()) 
      ? AccountId.ACCOUNT_ID : request.getUserPrincipal().getName();
  if (StringUtils.isEmpty(accountId)) {
      return new CommonResp<>(ErrorCode.SYS_NO_LOGIN);
  }
  ```
- 返回值统一使用 `CommonResp<>` 封装
- POST 接收对象加 `@Valid @RequestBody`

## 执行步骤
1. 用户提供建表 SQL 或表名 + 字段信息
2. 读取项目中 1-2 个同类文件作为风格参考
3. 按照 Entity → DAO → XML → Service → ServiceImpl → Controller 顺序逐一生成
4. 每个文件生成后列出文件路径，方便用户确认
5. 最后输出文件清单汇总

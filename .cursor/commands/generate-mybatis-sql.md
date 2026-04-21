# generate-mybatis-sql

## 概述
根据用户的需求描述，在对应的 Mapper XML 中生成 MyBatis SQL 语句，并在 DAO 接口中添加对应的方法签名。

## 执行步骤

### 第一步：明确需求
确认以下信息（如用户未提供，主动询问）：
- 操作类型：查询 / 新增 / 更新 / 删除
- 涉及的表名和字段
- 查询条件、排序、分页需求
- 返回值结构（单条 / 列表 / 分页 / 计数）

### 第二步：查找已有文件
- 找到对应的 DAO 接口文件和 Mapper XML 文件
- 如果不确定，在 `znzmo-common/src/main/resources/mybatis/dao/` 下搜索
- 阅读已有 SQL 了解表结构和现有写法风格

### 第三步：生成 SQL
在 Mapper XML 中添加 SQL，遵循以下规范：

**安全规范（强制）：**
- 参数一律使用 `#{}` 占位符，**严禁使用 `${}`**
- 动态条件使用 `<where>` + `<if>` 组合，避免全空条件导致全表扫描
- IN 子句必须判断集合非空：
  ```xml
  <if test="ids != null and ids.size() > 0">
      AND id IN
      <foreach collection="ids" item="id" open="(" separator="," close=")">
          #{id}
      </foreach>
  </if>
  ```

**编写规范：**
- `<select>` 的 `resultMap` 或 `resultType` 必须正确
- 复用已有的 `<sql>` 列片段，避免手写 `SELECT *`
- UPDATE 语句使用 `<set>` + `<if>` 实现动态更新
- 批量插入使用 `<foreach>` 并注意数据量限制
- 复杂查询添加 XML 注释说明查询意图

### 第四步：添加 DAO 方法
在对应 DAO 接口中添加方法签名：
- 命名规范：`selectXxxByXxx` / `insertXxx` / `updateXxxByXxx` / `deleteXxxByXxx` / `countXxxByXxx`
- 多参数使用 `@Param` 注解
- 返回类型与 XML 中的 `resultMap` / `resultType` 匹配

### 第五步：索引提醒
生成完成后，列出 SQL 涉及的：
- WHERE 条件字段
- ORDER BY 字段
- JOIN 关联字段

提醒用户确认这些字段是否有索引覆盖，如果没有建议添加索引。

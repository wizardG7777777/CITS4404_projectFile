# Agent Guidance: CITS4404 Trading Bot Project

## 0. 项目背景与定位

- **项目性质**：这是一个轻量级的**交易算法研究项目**（CITS4404 Team Project — Building AI Trading Bots）。
- **核心目标**：利用自然启发式优化算法（nature-inspired algorithms）设计、实现并评估比特币交易机器人。
- **技术栈**：主要程序使用 **Python** 构建；已配置 `uv` 虚拟环境，Python 版本统一为 **3.12+**。
- **辅助工具**：项目配备了 `toolkit` CLI 工具，用于辅助研究阶段快速读取和分析 CSV/PDF 数据。
- **合规要求**：**必须严格遵循 `project_guidelines.txt` 中的要求编写代码与报告**。任何偏离规范的行为（如直接复制外部交易机器人代码、使用通用优化库、未按要求提交 .ipynb 等）都可能导致**扣分**。

---

## 1. 工具定位

- 工具类型：只读型数据检索工具
- 作用对象：CSV 文件、PDF 文件
- 风险级别：低（默认不修改任何文件）
- 禁止行为：覆盖原始数据、删除文件、执行与读取无关的系统命令
- 运行前提：项目已配置 `uv` 虚拟环境，Agent 默认通过 `uv run` 执行命令

## 2. 能力边界

### CSV 工具能力

- 按行范围读取内容
- 按列范围读取内容
- 按关键词匹配列名
- 按条件筛选实例（行）
- 将筛选结果打印到终端
- 输出必须始终包含第一行表头

### PDF 工具能力

- 按页范围提取文本
- 按关键词定位并读取命中页文本

### 非目标能力（当前不支持）

- OCR（扫描版 PDF 图像识别）
- 数据写回或文件修改
- 跨文件 JOIN 或数据库式查询

## 3. 命令清单（规范）

```bash
uv run python -m toolkit csv read-rows --file <csv_path> --start <int> --end <int> [--output json|table] [--table-charset utf8|ascii]
uv run python -m toolkit csv read-cols --file <csv_path> --start-col <int> --end-col <int> [--output json|table] [--table-charset utf8|ascii]
uv run python -m toolkit csv find-columns --file <csv_path> --keyword <text> [--ignore-case] [--output json|table] [--table-charset utf8|ascii]
uv run python -m toolkit csv filter-rows --file <csv_path> --where "<expr>" [--where "<expr>"] [--output json|table] [--table-charset utf8|ascii]

uv run python -m toolkit pdf read-pages --file <pdf_path> --start-page <int> --end-page <int> [--output json|table] [--table-charset utf8|ascii]
uv run python -m toolkit pdf find-keyword --file <pdf_path> --keyword <text> [--output json|table] [--table-charset utf8|ascii]
```

## 4. 参数契约

- 索引规则：行号、列号、页号均为 `1-based`
- 范围规则：`start <= end`，且为闭区间
- 文件路径：必须是可访问路径
- 关键词：非空字符串
- `--where`：支持多次传入，按 AND 组合
- 输出规则：CSV 任何结果都必须包含表头行
- `--table-charset`：取值为 `utf8|ascii`，适用于 CSV 和 PDF；当 `--output json` 时自动忽略
- 表格输出中单元格换行符会被替换为空格，超长文本（>120 字符）自动截断并加 `...`

## 5. 表达式规则（`--where`）

语法：

`<column> <operator> <value>`

- `<column>`：列名（建议区分大小写）
- `<operator>`：`=`、`!=`、`>`、`>=`、`<`、`<=`、`contains`、`~=`
- `<value>`：比较值；包含空格时建议使用双引号包裹

组合规则：

- 支持重复传入多个 `--where`
- 多个条件默认按 `AND` 组合

类型规则：

- `>`、`>=`、`<`、`<=` 仅用于数值比较
- `=`、`!=` 可用于字符串和数值
- `contains` 用于子串匹配
- `~=` 用于正则匹配（若未启用正则引擎，返回明确错误）

错误码约定：

- `INVALID_WHERE_EXPRESSION`：表达式语法不合法
- `COLUMN_NOT_FOUND`：列名不存在
- `TYPE_MISMATCH`：数值比较用于非数值列

示例：

- `Country=Australia`
- `Score>=80`
- `City contains Perth`

## 6. 输出契约

默认优先返回表格；当指定 `--output json` 时返回结构化数据。
CSV 与 PDF 在表格输出时均支持 `--table-charset utf8|ascii`：`utf8` 可读性更高，`ascii` 兼容性更好。
当 `--output json` 时忽略 `--table-charset`。

推荐 JSON 响应结构：

```json
{
  "ok": true,
  "command": "csv filter-rows",
  "meta": {
    "file": "data.csv",
    "row_count": 12,
    "columns": ["Name", "Country", "Score"]
  },
  "data": [
    { "Name": "A", "Country": "Australia", "Score": 85 }
  ]
}
```

错误输出格式：

```json
{
  "ok": false,
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "CSV file does not exist"
  }
}
```

## 7. Agent 调用策略

满足以下意图时优先调用本 CLI：

- “读取 CSV 某些行/列”
- “查找包含某关键词的列”
- “筛选某些属性的记录”
- “读取 PDF 某几页”
- “在 PDF 里找某个关键词”

执行约定：

- 在项目根目录执行 `uv run python -m toolkit ...`
- 默认不使用 `pip install`、`python -m venv`、`uv init` 进行重复环境初始化
- 仅在用户明确要求时再执行依赖变更（如 `uv add`）

以下情况不调用或需先提示用户：

- 路径不明确或文件不存在
- 用户要求 OCR（扫描 PDF）
- 用户要求改写原文件

## 8. 错误恢复策略

按顺序执行恢复：

1. 校验参数合法性（范围、空值、类型）
2. 校验路径与文件类型
3. 对可恢复错误给出修复建议并重试一次
4. 若仍失败，返回结构化错误并停止

典型恢复示例：

- `INVALID_RANGE`：提示交换或修正 `start/end`
- `PAGE_OUT_OF_RANGE`：提示最大页码并建议缩小范围
- `COLUMN_NOT_FOUND`：返回相近列名候选

## 9. 安全与合规

- 仅读取，不写入
- 不执行危险 shell 命令
- 不上传本地敏感数据到外部网络
- 输出中避免泄露绝对路径以外的敏感信息

## 10. 示例（Agent 参考）

### 成功案例：按条件筛选 CSV

请求意图：筛选 `Score>=80` 且 `Country=Australia`

调用：

```bash
uv run python -m toolkit csv filter-rows --file ./data.csv --where "Score>=80" --where "Country=Australia" --output table --table-charset utf8
```

预期：终端返回 UTF-8 表格，且结果包含表头；如需结构化结果，改用 `--output json`。

### 成功案例：按关键词定位 PDF 页面

调用：

```bash
uv run python -m toolkit pdf find-keyword --file ./docs/report.pdf --keyword "swarm intelligence" --output json
```

预期：返回命中页号列表与页面文本。

### 失败恢复案例：页码越界

错误：

```json
{
  "ok": false,
  "error": {
    "code": "PAGE_OUT_OF_RANGE",
    "message": "end-page exceeds total pages (max=73)"
  }
}
```

恢复动作：将 `--end-page` 调整到 `73` 后重试。

## 11. 版本建议

- 建议在工具实现后引入 `--version`
- 每次参数或输出结构变更都更新本文件
- 重大变更时保持向后兼容或提供迁移说明

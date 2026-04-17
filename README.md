# Python Data Reader Toolkit

本项目计划提供一组基于 Python 的命令行工具，用于高效读取和筛选 CSV 与 PDF 内容。

## 功能概览

### CSV 阅读工具

支持以下能力：

1. 读取指定行范围内的内容
2. 读取指定列范围内的内容
3. 根据关键词查找匹配的列名
4. 根据关键词或条件筛选符合属性的实例（行）
5. 将符合条件的内容打印到终端
6. 无论行号范围如何设置，输出始终包含第一行表头

### PDF 阅读工具

支持以下能力：

1. 根据页号读取指定范围内的文本
2. 根据关键词定位并读取包含关键词的页面内容

## 安装与环境

### 要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 虚拟环境管理器

### 首次初始化（从零开始）

如果你刚克隆本项目，或 `.venv` 目录不存在，请按以下步骤初始化环境：

```bash
# 1. 确保 uv 已安装（若未安装，可参考 https://docs.astral.sh/uv/getting-started/installation/）
uv --version

# 2. 在项目根目录创建虚拟环境（Python 版本由 .python-version 指定为 3.12）
uv venv

# 3. 安装项目依赖
uv sync
```

### 已有环境（同步依赖）

如果 `.venv` 已存在但依赖可能有变更，执行以下命令同步：

```bash
uv sync
```

### 验证环境

初始化完成后，可通过以下命令验证工具是否可用：

```bash
uv run python -m toolkit --help
```

已安装的主要依赖：

- `pandas`（CSV 处理）
- `pypdf`（PDF 文本提取）
- `pytest`（测试框架）
- `cython`（由环境解析引入）

## CLI 设计（建议）

以下为推荐命令结构，便于后续扩展：

```bash
uv run python -m toolkit csv read-rows --file <csv_path> --start 1 --end 20 [--output table|json] [--table-charset utf8|ascii]
uv run python -m toolkit csv read-cols --file <csv_path> --start-col 1 --end-col 4 [--output table|json] [--table-charset utf8|ascii]
uv run python -m toolkit csv find-columns --file <csv_path> --keyword <text> [--ignore-case] [--output table|json] [--table-charset utf8|ascii]
uv run python -m toolkit csv filter-rows --file <csv_path> --where "<expr>" [--where "<expr>"] [--output table|json] [--table-charset utf8|ascii]

uv run python -m toolkit pdf read-pages --file <pdf_path> --start-page 1 --end-page 5 [--output table|json]
uv run python -m toolkit pdf find-keyword --file <pdf_path> --keyword <text> [--output table|json]
```

## 参数与行为约定

为保证一致性，建议采用以下约定：

- 行号、列号、页号均使用 `1-based`（从 1 开始）
- 范围参数为闭区间：`start` 和 `end` 都包含
- 当 `start > end` 时返回参数错误
- CSV 输出始终包含表头（第一行）
- 默认关键词匹配区分大小写，可通过 `--ignore-case` 关闭区分
- 条件筛选 `--where` 支持多次传入，默认按 AND 逻辑组合
- `--table-charset utf8|ascii` 仅在 `--output table` 时生效，适用于 CSV 和 PDF
- 表格输出中单元格换行符会被替换为空格，超长文本（>120 字符）自动截断并加 `...`

## `--where` 表达式规范

`--where` 使用以下语法：

`<column> <operator> <value>`

- `<column>`：列名（建议区分大小写）
- `<operator>`：`=`、`!=`、`>`、`>=`、`<`、`<=`、`contains`、`~=`
- `<value>`：比较值；当值包含空格时建议使用双引号包裹

多条件规则：

- 可重复传入多个 `--where`
- 多个条件默认按逻辑 `AND` 组合

类型与比较规则：

- `>`、`>=`、`<`、`<=` 仅用于数值比较
- `=`、`!=` 可用于字符串和数值
- `contains` 用于子串匹配
- `~=` 用于正则匹配（如未启用正则引擎，应明确报错）

错误处理建议：

- 表达式语法错误：`INVALID_WHERE_EXPRESSION`
- 列名不存在：`COLUMN_NOT_FOUND`
- 数值比较用于非数值列：`TYPE_MISMATCH`

示例：

```bash
uv run python -m toolkit csv filter-rows --file data.csv --where "Country=Australia"
uv run python -m toolkit csv filter-rows --file data.csv --where "Score>=80" --where "City contains Perth"
```

## 输出格式

支持两种输出格式：

- 终端表格（默认，便于阅读）
- JSON（`--output json`，便于 Agent 处理）

表格字符集：

- `--table-charset utf8`：使用 UTF-8 线框字符（可读性更好）
- `--table-charset ascii`：使用 ASCII 字符（兼容性更稳）
- 当终端字体或宽度导致对齐问题时，建议切换到 `ascii` 或 `json`

统一错误输出格式：

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_RANGE",
    "message": "start must be less than or equal to end"
  }
}
```

## 使用示例

### 读取 CSV 的第 10 到 20 行（含表头）

```bash
uv run python -m toolkit csv read-rows --file ./docs/Nature-Inspired\ Algorithms/nature_inspired_algorithms.csv --start 10 --end 20 --output table --table-charset utf8
```

### 查找包含关键词 `algorithm` 的列名

```bash
uv run python -m toolkit csv find-columns --file ./data.csv --keyword algorithm --ignore-case
```

### 读取 PDF 的第 2 到 4 页

```bash
uv run python -m toolkit pdf read-pages --file ./docs/comprehensive_database_of_NatureInspired_Algorithms.pdf --start-page 2 --end-page 4
```

### 在 PDF 中按关键词定位页面

```bash
uv run python -m toolkit pdf find-keyword --file ./docs/comprehensive_database_of_NatureInspired_Algorithms.pdf --keyword swarm
```

## 错误处理

已覆盖以下错误场景：

- 文件不存在
- 文件格式不正确（非 CSV/PDF）
- 编码错误（CSV）
- 页码越界（PDF）
- 列名不存在或表达式语法错误

## 项目状态

工具已实现并保持命令与输出契约稳定。可直接使用 `uv run python -m toolkit` 运行。

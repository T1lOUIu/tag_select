以下是修改后的 Markdown 文档，添加了关于翻译 API 的配置说明，并调整了安装方法：

---

# Flask 标签选择器项目

## 简介

标签选择器是一个基于 Flask 框架的 Web 应用程序，程序集成了蓝图（Blueprint），用于模块化和可重用性。该项目允许用户选择不同的标签类别，并提供Google翻译API集成。项目改编自 [NovelAI-tag-generator](https://github.com/WolfChen1996/NovelAI-tag-generator)。

[![2024-01-30-103950.png](https://i.postimg.cc/cLp422HR/2024-01-30-103950.png)](https://postimg.cc/v4vs6P5T) *Tag选择*

[![2024-01-30-103532.png](https://i.postimg.cc/qMZ7XzHZ/2024-01-30-103532.png)](https://postimg.cc/D8LF7fZq) *画师选择（带预览图）*

[![2024-01-30-103856.png](https://i.postimg.cc/52Y2Pbx9/2024-01-30-103856.png)](https://postimg.cc/LJSS5dYG) *自定义Tag*

## 体验网站

- **网站地址**：https://idlecloud.cc/

## 功能特点

- **蓝图集成**：使用 Flask 蓝图进行模块化设计。
- **YAML 文件管理**：根据类别动态加载 YAML 文件中的数据。
- **错误处理**：为文件未找到的情况提供适当的错误响应。
- **翻译 API 集成**：集成 Google 翻译 API 对标签进行自动翻译。
- **用户友好界面**：直观的 Web 界面，用于选择和管理标签。

## 项目结构

- `app.py`：主 Flask 应用程序。
- `tag_extractor.py`：提取和翻译标签的模块。
- `search.py`：标签搜索功能模块。
- `config.yaml`：项目配置文件，包含 Google 翻译设置。
- `templates` 目录：包含 HTML 模板。
- `static` 目录：包含 JavaScript、CSS 文件等。
- `public` 目录：存放公共资源文件。

## 环境要求

- Python 3.x
- Flask
- PyYAML
- requests
- BeautifulSoup4
- jieba
- python-Levenshtein
- googletrans==4.0.0-rc1

## 安装与部署

### 1. **克隆仓库**：

将此仓库克隆到本地机器或下载源代码：

```bash
git clone https://github.com/YILING0013/tag_select.git
```

### 2. **创建虚拟环境**（可选但推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Unix 或 MacOS
venv\Scripts\activate  # Windows
```

### 3. **安装依赖**：

安装 `requirements.txt` 文件中的依赖项：

```bash
pip install -r requirements.txt
```

### 4. **配置 Google 翻译**：

在根目录下创建或修改 `config.yaml` 文件，添加 Google 翻译的配置：

```yaml
# Google翻译配置
google_translate_settings:
  default_source_language: 'auto'
  default_target_language: 'zh-cn'
  retry_count: 3
```

### 5. **运行应用程序**：

执行以下命令启动 Flask 应用程序：

```bash
python app.py
```

这将启动 Flask 开发服务器，您可以访问 `http://127.0.0.1:5000/` 以使用标签选择界面。

## API 使用

### 提取标签

从指定的URL提取标签并翻译：

```
GET /extract_tags?url={url}
```

### 翻译接口

翻译提供的文本：

```
POST /Tagtranslate
Content-Type: application/json

{
  "texts": ["text1", "text2", ...]
}
```

## 注意事项

- Google 翻译 API 有请求频率限制，请合理使用。
- 首次运行时可能需要等待几秒钟以初始化翻译服务。

---

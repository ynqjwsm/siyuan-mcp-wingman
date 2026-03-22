# 思源MCP僚机

思源笔记 MCP (Model Context Protocol) 服务，提供与思源笔记 API 的交互接口。

## 功能特性

- **笔记本管理**：获取笔记本列表、配置、根据名称获取笔记本
- **文档操作**：使用 Markdown 创建文档
- **搜索功能**：全文搜索、块搜索、标签搜索、引用块搜索、模板搜索、嵌入块搜索
- **导出功能**：导出 Markdown、HTML、预览 HTML、思源 Markdown
- **系统管理**：获取版本号、当前时间、工作空间目录、配置、设置外观模式、获取系统字体、工作空间账号、更新日志
- **大纲管理**：获取文档大纲
- **同步管理**：获取同步信息、执行同步、获取云端空间

## 安装方法

### 方法一：直接运行

1. 克隆项目
   ```bash
   git clone https://github.com/your-username/siyuan-mcp-wingman.git
   cd siyuan-mcp-wingman
   ```

2. 安装依赖
   ```bash
   # 使用 uv 包管理器
   pip install uv
   uv pip install -e .
   ```

3. 运行服务
   ```bash
   # 设置环境变量
   export SIYUAN_URL=http://localhost:6806
   export SIYUAN_TOKEN=your-token-here
   
   # 启动服务
   python server.py
   ```

### 方法二：Docker 部署

1. 运行容器
   ```bash
   docker run -d --name siyuan-mcp -p 8000:8000 \
     -e SIYUAN_URL=http://your-siyuan-server:6806 \
     -e SIYUAN_TOKEN=your-actual-token \
     brantwang/siyuan-mcp-wingman:v0.0.7
   ```

## 环境变量配置

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| SIYUAN_URL | 思源服务器地址 | http://127.0.0.1:6806 |
| SIYUAN_TOKEN | 认证令牌 | isbpqifdo2jv0cbc |

## 使用方法

### MCP 服务端点

服务启动后，MCP 端点地址为：`http://localhost:8000/mcp`

### 可用工具

- `list_notebooks()` - 获取笔记本列表
- `get_notebook_conf(notebook_id: str)` - 获取笔记本配置
- `get_notebook_by_name(name: str)` - 根据名称获取笔记本
- `create_doc_with_md(notebook_id: str, path: str, markdown: str)` - 使用 Markdown 创建文档
- `full_text_search_block(query: str, notebook_id: Optional[str] = None, method: int = 0, types: Optional[dict] = None, path: Optional[str] = None)` - 全文搜索块
- `search_block(query: str, notebook_id: Optional[str] = None)` - 搜索块
- `search_tag(query: str = "")` - 搜索标签
- `search_ref_block(query: str, notebook_id: Optional[str] = None, excluded_ids: Optional[List[str]] = None)` - 搜索引用块
- `search_template(query: str = "")` - 搜索模板
- `search_embedding_block(query: str, notebook_id: Optional[str] = None)` - 搜索嵌入块
- `get_recent_updated_blocks()` - 获取最近更新的块
- `get_recent_docs_by_usage()` - 根据使用频率获取最近文档
- `get_docs_by_words(words: List[str])` - 根据关键词获取文档
- `export_md_content(doc_id: str)` - 导出 Markdown 内容
- `export_md(doc_id: str)` - 导出 Markdown
- `export_html(doc_id: str, save_assets: bool = False)` - 导出 HTML
- `export_preview_html(doc_id: str, keep_lazy_load: bool = False)` - 导出预览 HTML
- `export_siyuan_md(doc_id: str)` - 导出思源 Markdown
- `version()` - 获取版本号
- `get_current_time()` - 获取当前时间
- `get_workspace_dir()` - 获取工作空间目录
- `get_conf()` - 获取配置
- `set_appearance_mode(mode: int)` - 设置外观模式
- `get_sys_fonts()` - 获取系统字体
- `get_workspace_acc()` - 获取工作空间账号
- `get_changelog()` - 获取更新日志
- `get_doc_outline(doc_id: str)` - 获取文档大纲
- `get_sync_info()` - 获取同步信息
- `perform_sync(mode: int = 0)` - 执行同步
- `get_cloud_space()` - 获取云端空间

## 技术栈

- Python 3.14+
- FastMCP
- FastAPI
- Requests
- Uvicorn
- Pydantic

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

## 许可证

MIT License

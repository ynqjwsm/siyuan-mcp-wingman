import os
from typing import Any, Dict, Optional, List
from fastmcp import FastMCP
from api import SiyuanAPI, SiyuanAPIError

mcp = FastMCP("siyuan-wingman")

siyuan_url = os.getenv("SIYUAN_URL", "http://127.0.0.1:6806")
siyuan_token = os.getenv("SIYUAN_TOKEN", "isbpqifdo2jv0cbc")

siyuan_api = SiyuanAPI(siyuan_url, siyuan_token)

@mcp.tool(
    annotations={
        "description": "获取笔记本列表",
        "readonlyHint": True
    }
)
def list_notebooks() -> dict:
    """
    获取笔记本列表

    Returns:
        笔记本列表，包含笔记本的 ID、名称等信息
    """
    try:
        return siyuan_api.list_notebooks()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_notebook_conf(notebook_id: str) -> dict:
    """
    获取笔记本配置

    Args:
        notebook_id: 笔记本 ID

    Returns:
        笔记本配置信息
    """
    try:
        return siyuan_api.get_notebook_conf(notebook_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_notebook_by_name(name: str) -> dict:
    """
    根据名称获取笔记本

    Args:
        name: 笔记本名称

    Returns:
        笔记本信息
    """
    try:
        return siyuan_api.get_notebook_by_name(name)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def create_doc_with_md(notebook_id: str, path: str, markdown: str) -> dict:
    """
    使用 Markdown 创建文档

    Args:
        notebook_id: 笔记本 ID
        path: 文档路径
        markdown: Markdown 内容

    Returns:
        创建的文档信息
    """
    try:
        return siyuan_api.create_doc_with_md(notebook_id, path, markdown)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def full_text_search_block(
    query: str,
    notebook_id: Optional[str] = None,
    method: int = 0,
    types: Optional[dict] = None,
    path: Optional[str] = None
) -> dict:
    """
    全文搜索块

    Args:
        query: 搜索关键词
        notebook_id: 笔记本 ID
        method: 搜索方法，0：关键字，1：查询语法，2：SQL，3：正则表达式
        orderBy: 排序字段，0：按相关度降序，1：按相关度升序，2：按更新时间升序，3：按更新时间降序
        types: 块类型过滤
        path: 路径

    Returns:
        搜索结果列表
    """
    try:
        return siyuan_api.full_text_search_block(query, notebook_id, method, orderBy, types, path)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_block(query: str, notebook_id: Optional[str] = None) -> dict:
    """
    搜索块

    Args:
        query: 搜索关键词
        notebook_id: 笔记本 ID

    Returns:
        搜索结果列表
    """
    try:
        return siyuan_api.search_block(query, notebook_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_tag(query: str = "") -> dict:
    """
    搜索标签

    Args:
        query: 搜索关键词

    Returns:
        标签列表
    """
    try:
        return siyuan_api.search_tag(query)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_ref_block(
    query: str,
    notebook_id: Optional[str] = None,
    excluded_ids: Optional[List[str]] = None
) -> dict:
    """
    搜索引用块

    Args:
        query: 搜索关键词
        notebook_id: 笔记本 ID
        excluded_ids: 排除的块 ID 列表

    Returns:
        搜索结果列表
    """
    try:
        return siyuan_api.search_ref_block(query, notebook_id, excluded_ids)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_template(query: str = "") -> list:
    """
    搜索模板

    Args:
        query: 搜索关键词

    Returns:
        模板列表
    """
    try:
        return siyuan_api.search_template(query)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_embedding_block(query: str, notebook_id: Optional[str] = None) -> list:
    """
    搜索嵌入块

    Args:
        query: 搜索关键词
        notebook_id: 笔记本 ID

    Returns:
        搜索结果列表
    """
    try:
        return siyuan_api.search_embedding_block(query, notebook_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_recent_updated_blocks() -> list:
    """
    获取最近更新的块

    Returns:
        最近更新的块列表
    """
    try:
        return siyuan_api.get_recent_updated_blocks()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_recent_docs_by_usage() -> list:
    """
    根据使用频率获取最近文档

    Returns:
        最近文档列表
    """
    try:
        return siyuan_api.get_recent_docs_by_usage()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_docs_by_words(words: List[str]) -> list:
    """
    根据关键词获取文档

    Args:
        words: 关键词列表

    Returns:
        文档列表
    """
    try:
        return siyuan_api.get_docs_by_words(words)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def export_md_content(doc_id: str) -> dict:
    """
    导出 Markdown 内容

    Args:
        doc_id: 文档 ID

    Returns:
        Markdown 内容
    """
    try:
        return siyuan_api.export_md_content(doc_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def export_md(doc_id: str) -> str:
    """
    导出 Markdown

    Args:
        doc_id: 文档 ID

    Returns:
        Markdown 文本
    """
    try:
        return siyuan_api.export_md(doc_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def export_html(doc_id: str, save_assets: bool = False) -> str:
    """
    导出 HTML

    Args:
        doc_id: 文档 ID
        save_assets: 是否保存资源

    Returns:
        HTML 内容
    """
    try:
        return siyuan_api.export_html(doc_id, save_assets)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def export_preview_html(doc_id: str, keep_lazy_load: bool = False) -> str:
    """
    导出预览 HTML

    Args:
        doc_id: 文档 ID
        keep_lazy_load: 是否保留懒加载

    Returns:
        HTML 内容
    """
    try:
        return siyuan_api.export_preview_html(doc_id, keep_lazy_load)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def export_siyuan_md(doc_id: str) -> str:
    """
    导出思源 Markdown

    Args:
        doc_id: 文档 ID

    Returns:
        Markdown 内容
    """
    try:
        return siyuan_api.export_siyuan_md(doc_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def version() -> str:
    """
    获取版本号

    Returns:
        版本号
    """
    try:
        return siyuan_api.version()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_current_time() -> int:
    """
    获取当前时间

    Returns:
        当前时间戳
    """
    try:
        return siyuan_api.get_current_time()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_workspace_dir() -> str:
    """
    获取工作空间目录

    Returns:
        工作空间目录
    """
    try:
        return siyuan_api.get_workspace_dir()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_conf() -> dict:
    """
    获取配置

    Returns:
        配置字典
    """
    try:
        return siyuan_api.get_conf()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def set_appearance_mode(mode: int) -> dict:
    """
    设置外观模式

    Args:
        mode: 模式，0：自动，1：亮色，2：暗色

    Returns:
        设置结果
    """
    try:
        return siyuan_api.set_appearance_mode(mode)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_sys_fonts() -> list:
    """
    获取系统字体

    Returns:
        字体列表
    """
    try:
        return siyuan_api.get_sys_fonts()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_workspace_acc() -> dict:
    """
    获取工作空间账号

    Returns:
        账号信息
    """
    try:
        return siyuan_api.get_workspace_acc()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_changelog() -> str:
    """
    获取更新日志

    Returns:
        更新日志
    """
    try:
        return siyuan_api.get_changelog()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_doc_outline(doc_id: str) -> list:
    """
    获取文档大纲

    Args:
        doc_id: 文档 ID

    Returns:
        大纲列表
    """
    try:
        return siyuan_api.get_doc_outline(doc_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_sync_info() -> dict:
    """
    获取同步信息

    Returns:
        同步信息
    """
    try:
        return siyuan_api.get_sync_info()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def perform_sync(mode: str = "0") -> dict:
    """
    执行同步

    Args:
        mode: 同步模式，"0"：手动，"1"：自动

    Returns:
        同步结果
    """
    try:
        return siyuan_api.perform_sync(mode)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_cloud_space() -> dict:
    """
    获取云端空间

    Returns:
        云端空间信息
    """
    try:
        return siyuan_api.get_cloud_space()
    except SiyuanAPIError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http", port=8000, host="0.0.0.0", path="/mcp")

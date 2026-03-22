import os
from typing import Any, Dict, Optional, List
from fastmcp import FastMCP
from api import SiyuanAPI, SiyuanAPIError

mcp = FastMCP("siyuan-wingman")

siyuan_url = os.getenv("SIYUAN_URL", "http://127.0.0.1:6806")
siyuan_token = os.getenv("SIYUAN_TOKEN", "this-is-a-token-here")

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

# 搜索相关 API

@mcp.tool
def full_text_search_block(
    query: str,
    page_size: int = 50,
    notebook_id: Optional[str] = None,
    method: int = 0,
    orderBy: int = 0,
    types: Optional[dict] = None,
    path: Optional[str] = None
) -> dict:
    """
    全文搜索块

    Args:
        query: 搜索关键词
        page_size: 每页数量
        notebook_id: 笔记本 ID
        method: 搜索方法，0：关键字，1：查询语法，2：SQL，3：正则表达式
        orderBy: 排序字段，0：按相关度降序，1：按相关度升序，2：按更新时间升序，3：按更新时间降序
        types: 块类型过滤
        path: 路径

    Returns:
        搜索结果列表
    """
    try:
        return siyuan_api.full_text_search_block(query, page_size, notebook_id, method, orderBy, types, path)
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
def search_tag(keyword: str = "") -> dict:
    """
    搜索标签

    Args:
        keyword: 搜索关键词

    Returns:
        标签列表
    """
    try:
        return siyuan_api.search_tag(keyword)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_ref_block(
    id: str,
    root_id: str,
    keyword: str,
    before_len: int,
    req_id: Optional[str] = None,
    is_square_brackets: bool = False,
    is_database: bool = False
) -> dict:
    """
    搜索引用块

    Args:
        id: 块 ID
        root_id: 根 ID
        keyword: 搜索关键词
        before_len: 前置长度
        req_id: 请求 ID
        is_square_brackets: 是否方括号
        is_database: 是否数据库

    Returns:
        包含 blocks、newDoc、k、reqId 的字典
    """
    try:
        return siyuan_api.search_ref_block(id, root_id, keyword, before_len, req_id, is_square_brackets, is_database)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_template(keyword: str = "") -> dict:
    """
    搜索模板

    Args:
        keyword: 搜索关键词

    Returns:
        模板列表
    """
    try:
        return siyuan_api.search_template(keyword)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_widget(keyword: str = "") -> dict:
    """
    搜索小部件

    Args:
        keyword: 搜索关键词

    Returns:
        小部件列表
    """
    try:
        return siyuan_api.search_widget(keyword)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def search_embed_block(
    embed_block_id: str,
    stmt: str,
    exclude_ids: Optional[List[str]] = None,
    heading_mode: int = 0,
    breadcrumb: bool = False
) -> dict:
    """
    搜索嵌入块

    Args:
        embed_block_id: 嵌入块 ID
        stmt: SQL 查询语句
        exclude_ids: 排除的块 ID 列表
        heading_mode: 标题模式，0：显示标题与下方的块，1：仅显示标题，2：仅显示标题下方的块
        breadcrumb: 是否显示面包屑

    Returns:
        包含 blocks 的字典
    """
    try:
        return siyuan_api.search_embed_block(embed_block_id, stmt, exclude_ids, heading_mode, breadcrumb)
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_embed_block(
    embed_block_id: str,
    include_ids: List[str],
    heading_mode: int = 0,
    breadcrumb: bool = False
) -> dict:
    """
    获取嵌入块

    Args:
        embed_block_id: 嵌入块 ID
        include_ids: 包含的块 ID 列表
        heading_mode: 标题模式，0：显示标题与下方的块，1：仅显示标题，2：仅显示标题下方的块
        breadcrumb: 是否显示面包屑

    Returns:
        包含 blocks 的字典
    """
    try:
        return siyuan_api.get_embed_block(embed_block_id, include_ids, heading_mode, breadcrumb)
    except SiyuanAPIError as e:
        return {"error": str(e)}

## 导出相关 API

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

## 系统相关 API

@mcp.tool
def version() -> dict:
    """
    获取思源版本号

    Returns:
        思源版本字典对象
    """
    try:
        return siyuan_api.version()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_current_time() -> dict:
    """
    获取思源服务器当前时间

    Returns:
        思源服务器当前时间戳字典对象
    """
    try:
        return siyuan_api.get_current_time()
    except SiyuanAPIError as e:
        return {"error": str(e)}

@mcp.tool
def get_workspace_dir() -> dict:
    """
    获取工作空间目录

    Returns:
        工作空间目录字典对象
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
        配置字典对象
    """
    try:
        return siyuan_api.get_conf()
    except SiyuanAPIError as e:
        return {"error": str(e)}

## 大纲相关 API

@mcp.tool
def get_doc_outline(doc_id: str) -> dict:
    """
    获取文档大纲

    Args:
        doc_id: 文档 ID

    Returns:
        大纲字典对象
    """
    try:
        return siyuan_api.get_doc_outline(doc_id)
    except SiyuanAPIError as e:
        return {"error": str(e)}

## 同步相关 API

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

if __name__ == "__main__":
    mcp.run(transport="http", port=8000, host="0.0.0.0", path="/mcp")

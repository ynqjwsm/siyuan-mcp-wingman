"""
siyuan-note API 客户端
"""
import json
from typing import Any, Optional
from urllib.parse import urljoin
import requests


class SiyuanAPIError(Exception):
    """siyuan-note API 错误异常"""
    def __init__(self, code: int, msg: str, data: Any = None):
        self.code = code
        self.msg = msg
        self.data = data
        super().__init__(f"[{code}] {msg}")


class SiyuanAPI:
    """siyuan-note API 客户端"""
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {self.token}"
    
    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """
        发送 API 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据

        Returns:
            API 响应数据

        Raises:
            SiyuanAPIError: API 错误
        """
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method, url, json=data)
        response.raise_for_status()

        # 检查响应内容是否为空
        content = response.text.strip()
        if not content:
            raise SiyuanAPIError(-1, "Empty response from server")

        # 尝试解析 JSON
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            raise SiyuanAPIError(-1, f"Invalid JSON response: {str(e)}", content[:200])

        if result.get("code") != 0:
                raise SiyuanAPIError(
                    code=result.get("code", -1),
                    msg=result.get("msg", "Unknown error"),
                    data=result.get("data")
                )

        return result
       
    def list_notebooks(self) -> dict:
        """
        获取笔记本列表

        Returns:
            笔记本列表
        """
        return self._request("POST", "/api/notebook/lsNotebooks")

    def get_notebook_conf(self, notebook_id: str) -> dict:
        """
        获取笔记本配置

        Args:
            notebook_id: 笔记本 ID

        Returns:
            笔记本配置
        """
        return self._request("POST", "/api/notebook/getNotebookConf", {"notebook": notebook_id})

    def get_notebook_by_name(self, name: str) -> dict:
        """
        根据名称获取笔记本

        Args:
            name: 笔记本名称

        Returns:
            笔记本信息
        """
        return self._request("POST", "/api/notebook/getNotebookByName", {"name": name})

    def create_doc_with_md(self, notebook_id: str, path: str, markdown: str) -> dict:
        """
        使用 Markdown 创建文档

        Args:
            notebook_id: 笔记本 ID
            path: 文档路径
            markdown: Markdown 内容

        Returns:
            创建的文档信息
        """
        return self._request("POST", "/api/filetree/createDocWithMd", {
            "notebook": notebook_id,
            "path": path,
            "markdown": markdown
        })  

    # ==================== 搜索相关 API ====================

    def full_text_search_block(
        self,
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
        payload = {"query": query, "pageSize": page_size, "method": method}
        if orderBy:
            payload["orderBy"] = orderBy
        if notebook_id:
            payload["notebook"] = notebook_id
        if types:
            payload["types"] = types
        if path:
            payload["path"] = path
        return self._request("POST", "/api/search/fullTextSearchBlock", payload)

    def search_block(self, query: str, notebook_id: Optional[str] = None) -> dict:
        """
        搜索块

        Args:
            query: 搜索关键词
            notebook_id: 笔记本 ID

        Returns:
            搜索结果列表
        """
        payload = {"query": query}
        if notebook_id:
            payload["notebook"] = notebook_id
        return self._request("POST", "/api/search/searchBlock", payload)

    def search_tag(self, keyword: str = "") -> dict:
        """
        搜索标签

        Args:
            keyword: 搜索关键词

        Returns:
            标签列表
        """
        return self._request("POST", "/api/search/searchTag", {"k": keyword})

    def search_ref_block(
        self,
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
        payload = {
            "id": id,
            "rootID": root_id,
            "k": keyword,
            "beforeLen": before_len,
            "isSquareBrackets": is_square_brackets,
            "isDatabase": is_database
        }
        if req_id:
            payload["reqId"] = req_id
        return self._request("POST", "/api/search/searchRefBlock", payload)

    def search_template(self, keyword: str = "") -> dict:
        """
        搜索模板

        Args:
            keyword: 搜索关键词

        Returns:
            模板列表
        """
        return self._request("POST", "/api/search/searchTemplate", {"k": keyword})

    def search_widget(self, keyword: str = "") -> dict:
        """
        搜索小部件

        Args:
            keyword: 搜索关键词

        Returns:
            小部件列表
        """
        return self._request("POST", "/api/search/searchWidget", {"k": keyword})

    def search_embed_block(
        self,
        embed_block_id: str,
        stmt: str,
        exclude_ids: Optional[list] = None,
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
        payload = {
            "embedBlockID": embed_block_id,
            "stmt": stmt,
            "headingMode": heading_mode,
            "breadcrumb": breadcrumb
        }
        if exclude_ids:
            payload["excludeIDs"] = exclude_ids
        return self._request("POST", "/api/search/searchEmbedBlock", payload)

    def get_embed_block(
        self,
        embed_block_id: str,
        include_ids: list,
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
        payload = {
            "embedBlockID": embed_block_id,
            "includeIDs": include_ids,
            "headingMode": heading_mode,
            "breadcrumb": breadcrumb
        }
        return self._request("POST", "/api/search/getEmbedBlock", payload)

    # ==================== 导出相关 API ====================

    def export_md_content(self,
        method: int = 0,
        orderBy: int = 0,
        types: Optional[dict] = None,
        path: Optional[str] = None
    ) -> dict:
        """
        导出 Markdown 内容

        Args:
            doc_id: 文档 ID

        Returns:
            Markdown 内容
        """
        return self._request("POST", "/api/export/exportMdContent", {"id": doc_id})

    def export_preview_html(self, doc_id: str, keep_lazy_load: bool = False) -> str:
        """
        导出预览 HTML

        Args:
            doc_id: 文档 ID
            keep_lazy_load: 是否保留懒加载

        Returns:
            HTML 内容
        """
        return self._request("POST", "/api/export/preview", {
            "id": doc_id,
            "keepLazyLoad": keep_lazy_load
        })

    # ==================== 系统相关 API ====================

    def version(self) -> dict:
        """
        获取思源版本号

        Returns:
            思源版本字典
        """
        return self._request("POST", "/api/system/version")

    def get_current_time(self) -> dict:
        """
        获取思源服务器当前时间

        Returns:
            思源服务器当前时间戳字典对象
        """
        return self._request("POST", "/api/system/currentTime")

    def get_workspace_dir(self) -> dict:
        """
        获取工作空间目录

        Returns:
            工作空间目录字典对象
        """
        return self._request("POST", "/api/system/getWorkspaces")

    def get_conf(self) -> dict:
        """
        获取思源配置

        Returns:
            思源配置字典对象
        """
        return self._request("POST", "/api/system/getConf")

    # ==================== 大纲相关 API ====================

    def get_doc_outline(self, doc_id: str) -> dict:
        """
        获取文档大纲

        Args:
            doc_id: 文档 ID

        Returns:
            大纲字典对象
        """
        return self._request("POST", "/api/outline/getDocOutline", {"id": doc_id})

    # ==================== 同步相关 API ====================

    def get_sync_info(self) -> dict:
        """
        获取同步信息

        Returns:
            同步信息
        """
        return self._request("POST", "/api/sync/getSyncInfo")

    def perform_sync(self, mode: str = "0") -> dict:
        """
        执行同步

        Args:
            mode: 同步模式，0：手动，1：自动

        Returns:
            同步结果
        """
        return self._request("POST", "/api/sync/performSync", {"mode": mode})
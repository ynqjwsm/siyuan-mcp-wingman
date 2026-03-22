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

    def full_text_search_block(
        self,
        query: str,
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
            notebook_id: 笔记本 ID
            method: 搜索方法，0：关键字，1：查询语法，2：SQL，3：正则表达式
            orderBy: 排序字段，0：按相关度降序，1：按相关度升序，2：按更新时间升序，3：按更新时间降序
            types: 块类型过滤
            path: 路径

        Returns:
            搜索结果列表
        """
        payload = {"query": query, "method": method}
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

    def search_tag(self, query: str = "") -> dict:
        """
        搜索标签

        Args:
            query: 搜索关键词

        Returns:
            标签列表
        """
        return self._request("POST", "/api/search/searchTag", {"query": query})

    def search_ref_block(self, query: str, notebook_id: Optional[str] = None, excluded_ids: Optional[list] = None) -> dict:
        """
        搜索引用块

        Args:
            query: 搜索关键词
            notebook_id: 笔记本 ID
            excluded_ids: 排除的块 ID 列表

        Returns:
            搜索结果列表
        """
        payload = {"query": query}
        if notebook_id:
            payload["notebook"] = notebook_id
        if excluded_ids:
            payload["excludeIDs"] = excluded_ids
        return self._request("POST", "/api/search/searchRefBlock", payload)

    def search_template(self, query: str = "") -> list:
        """
        搜索模板

        Args:
            query: 搜索关键词

        Returns:
            模板列表
        """
        return self._request("POST", "/api/search/searchTemplate", {"query": query})

    def search_embedding_block(self, query: str, notebook_id: Optional[str] = None) -> list:
        """
        搜索嵌入块

        Args:
            query: 搜索关键词
            notebook_id: 笔记本 ID

        Returns:
            搜索结果列表
        """
        payload = {"query": query}
        if notebook_id:
            payload["notebook"] = notebook_id
        return self._request("POST", "/api/search/searchEmbeddingBlock", payload)

    def get_recent_updated_blocks(self) -> list:
        """
        获取最近更新的块

        Returns:
            最近更新的块列表
        """
        return self._request("POST", "/api/search/getRecentUpdatedBlocks")

    def get_recent_docs_by_usage(self) -> list:
        """
        根据使用频率获取最近文档

        Returns:
            最近文档列表
        """
        return self._request("POST", "/api/search/getRecentDocsByUsage")

    def get_docs_by_words(self, words: list[str]) -> list:
        """
        根据关键词获取文档

        Args:
            words: 关键词列表

        Returns:
            文档列表
        """
        return self._request("POST", "/api/search/getDocsByWords", {"words": words})

    def export_md_content(self, doc_id: str) -> dict:
        """
        导出 Markdown 内容

        Args:
            doc_id: 文档 ID

        Returns:
            Markdown 内容
        """
        return self._request("POST", "/api/export/exportMdContent", {"id": doc_id})

    def export_md(self, doc_id: str) -> str:
        """
        导出 Markdown

        Args:
            doc_id: 文档 ID

        Returns:
            Markdown 文本
        """
        return self._request("POST", "/api/export/exportMd", {"id": doc_id})

    def export_html(self, doc_id: str, save_assets: bool = False) -> str:
        """
        导出 HTML

        Args:
            doc_id: 文档 ID
            save_assets: 是否保存资源

        Returns:
            HTML 内容
        """
        return self._request("POST", "/api/export/exportHTML", {
            "id": doc_id,
            "saveAssets": save_assets
        })

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

    def export_siyuan_md(self, doc_id: str) -> str:
        """
        导出思源 Markdown

        Args:
            doc_id: 文档 ID

        Returns:
            Markdown 内容
        """
        return self._request("POST", "/api/export/exportSY", {"id": doc_id})

    # ==================== 系统相关 API ====================

    def version(self) -> str:
        """
        获取版本号

        Returns:
            版本号
        """
        return self._request("POST", "/api/system/version")

    def get_current_time(self) -> int:
        """
        获取当前时间

        Returns:
            当前时间戳
        """
        return self._request("POST", "/api/system/currentTime")

    def get_workspace_dir(self) -> str:
        """
        获取工作空间目录

        Returns:
            工作空间目录
        """
        return self._request("POST", "/api/system/getWorkspaces")

    def get_conf(self) -> dict:
        """
        获取配置

        Returns:
            配置字典
        """
        return self._request("POST", "/api/system/getConf")

    def set_appearance_mode(self, mode: int) -> dict:
        """
        设置外观模式

        Args:
            mode: 模式，0：自动，1：亮色，2：暗色

        Returns:
            设置结果
        """
        return self._request("POST", "/api/system/setAppearanceMode", {"mode": mode})

    def get_sys_fonts(self) -> list:
        """
        获取系统字体

        Returns:
            字体列表
        """
        return self._request("POST", "/api/system/getSysFonts")

    def get_workspace_acc(self) -> dict:
        """
        获取工作空间账号

        Returns:
            账号信息
        """
        return self._request("POST", "/api/system/getWorkspaceAcc")

    def get_changelog(self) -> str:
        """
        获取更新日志

        Returns:
            更新日志
        """
        return self._request("POST", "/api/system/getChangelog")

    # ==================== 大纲相关 API ====================

    def get_doc_outline(self, doc_id: str) -> list:
        """
        获取文档大纲

        Args:
            doc_id: 文档 ID

        Returns:
            大纲列表
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

    def get_cloud_space(self) -> dict:
        """
        获取云端空间

        Returns:
            云端空间信息
        """
        return self._request("POST", "/api/sync/getCloudSpace")

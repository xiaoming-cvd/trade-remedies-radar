"""分页抓取 Federal Register 公告。

数据源探测结论：官网提供官方免费 JSON API，无需认证、国内可直连，
因此本项目不使用爬虫，直接调用 API 并按页拉取全量。
"""
import time

import requests

import config


def fetch_page(term, page):
    """抓取单页。用 tuple 列表传参以支持重复字段（fields[]）。"""
    params = [
        ("conditions[term]", term),
        ("conditions[agencies][]", config.AGENCY),
        ("per_page", str(config.PER_PAGE)),
        ("page", str(page)),
        ("order", "newest"),
    ]
    params += [("fields[]", f) for f in config.FIELDS]
    if config.START_DATE:
        params.append(("conditions[publication_date][gte]", config.START_DATE))
    if config.END_DATE:
        params.append(("conditions[publication_date][lte]", config.END_DATE))

    resp = requests.get(config.API_URL, params=params, timeout=config.TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_all(max_pages=None):
    """自动翻页抓取全部公告，按 document_number 去重后返回列表。"""
    docs = {}
    for term in config.SEARCH_TERMS:
        page = 1
        while True:
            data = fetch_page(term, page)
            results = data.get("results") or []
            for d in results:
                # 两个检索词结果有重叠：按文档号去重
                docs[d["document_number"]] = d
            total_pages = data.get("total_pages") or 1
            print("      [%s] 第 %d/%d 页，累计 %d 条"
                  % (term, page, total_pages, len(docs)))
            if page >= total_pages or not results:
                break
            if max_pages and page >= max_pages:
                break
            page += 1
            time.sleep(config.REQUEST_INTERVAL)
    return list(docs.values())

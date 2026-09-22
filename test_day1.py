"""Day 1 数据源探测脚本：验证 Federal Register API 连通性。

原项目最关键的一步：先确认官网有免费 API，再决定技术路线，
避免花几天写一个高风险爬虫。
"""
import requests

import config


def main():
    params = [
        ("conditions[term]", config.SEARCH_TERMS[0]),
        ("conditions[agencies][]", config.AGENCY),
        ("per_page", "20"),
        ("page", "1"),
        ("order", "newest"),
    ]
    params += [("fields[]", f) for f in config.FIELDS]

    resp = requests.get(config.API_URL, params=params, timeout=config.TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    print("API 连通成功，共命中 %d 条公告" % data["count"])
    print("--- 最新 5 条 ---")
    for d in data["results"][:5]:
        print("[%s] %s" % (d["publication_date"], d["title"][:70]))
        print("    -> %s" % d["html_url"])


if __name__ == "__main__":
    main()

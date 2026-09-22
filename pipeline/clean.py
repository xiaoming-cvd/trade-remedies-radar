"""数据清洗：必填字段非空、日期合法、按文档号去重、按日期排序。

验收标准（对齐原项目）：无空值、无重复、日期有效、链接可访问。
"""
from datetime import datetime

COLUMNS = [
    "document_number", "publication_date", "notice_type",
    "country", "product", "industry", "title", "html_url",
]
REQUIRED = ["document_number", "publication_date", "title", "html_url"]


def clean(rows):
    seen = set()
    out = []
    dropped = 0
    for r in rows:
        # 1. 必填字段不允许为空
        if any(not r.get(k) for k in REQUIRED):
            dropped += 1
            continue
        # 2. 日期必须合法
        try:
            datetime.strptime(r["publication_date"], "%Y-%m-%d")
        except (ValueError, TypeError):
            dropped += 1
            continue
        # 3. 按文档号去重
        if r["document_number"] in seen:
            dropped += 1
            continue
        seen.add(r["document_number"])
        out.append({k: r.get(k, "") for k in COLUMNS})
    # 4. 按日期倒序
    out.sort(key=lambda r: r["publication_date"], reverse=True)
    if dropped:
        print("      清洗剔除 %d 条（空值/非法日期/重复）" % dropped)
    return out

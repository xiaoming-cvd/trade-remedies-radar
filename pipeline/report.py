"""统计聚合 + 用 Jinja2 模板生成纯静态 HTML 看板（Chart.js 渲染图表）。"""
from collections import Counter
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

import config


def build_dashboard(rows):
    # 月度趋势
    monthly = Counter(r["publication_date"][:7] for r in rows)
    months = sorted(monthly)
    # 国别分布（一条公告可能涉及多国）
    country_counter = Counter()
    for r in rows:
        for c in r["country"].split("、"):
            if c and c != "未识别":
                country_counter[c] += 1
    # 行业分布
    industry_counter = Counter(r["industry"] for r in rows)

    top_countries = country_counter.most_common(10)
    top_industries = industry_counter.most_common(10)

    env = Environment(loader=FileSystemLoader(str(config.TEMPLATE_DIR)))
    tpl = env.get_template("dashboard.html.j2")
    html = tpl.render(
        total=len(rows),
        date_min=rows[-1]["publication_date"] if rows else "-",
        date_max=rows[0]["publication_date"] if rows else "-",
        top_country=top_countries[0][0] if top_countries else "-",
        months=months,
        monthly_counts=[monthly[m] for m in months],
        countries=[c for c, _ in top_countries],
        country_counts=[n for _, n in top_countries],
        industries=[i for i, _ in top_industries],
        industry_counts=[n for _, n in top_industries],
        rows=rows[:100],
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    config.DASHBOARD_DIR.mkdir(exist_ok=True)
    out = config.DASHBOARD_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    return out

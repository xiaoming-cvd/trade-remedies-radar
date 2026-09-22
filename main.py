"""贸易救济数据雷达 —— 一条命令完成：抓取 -> 提取 -> 清洗 -> 生成看板"""
import csv
import time

import config
from pipeline import clean, extract, fetch, report


def main():
    t0 = time.time()

    print("[1/4] 抓取 Federal Register 公告 ...")
    raw = fetch.fetch_all()
    print("      原始记录：%d 条" % len(raw))

    print("[2/4] 结构化提取（国家 / 产品 / 行业 / 公告类型）...")
    rows = [extract.enrich(d) for d in raw]

    print("[3/4] 清洗与校验 ...")
    rows = clean.clean(rows)
    print("      有效记录：%d 条" % len(rows))

    config.DATA_DIR.mkdir(exist_ok=True)
    with open(config.CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig：带 BOM，Excel 直接打开不乱码
        writer = csv.DictWriter(f, fieldnames=clean.COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print("      CSV 已写入：%s" % config.CSV_PATH)

    print("[4/4] 生成可视化看板 ...")
    out = report.build_dashboard(rows)
    print("      看板已生成：%s" % out)

    print("全部完成，耗时 %.1f 秒。双击 dashboard/index.html 即可查看。"
          % (time.time() - t0))


if __name__ == "__main__":
    main()

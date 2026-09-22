贸易救济数据雷达（Trade Remedies Data Radar）
==============================================

一键抓取美国联邦公报（Federal Register）反倾销 / 反补贴公告，
自动清洗为结构化 CSV，并生成纯静态可视化看板（双击即开，零后端部署）。

技术路线
--------
1. 数据源：Federal Register 官方免费 JSON API（无需认证、无需爬虫）
   文档：https://www.federalregister.gov/developers/documentation/api/v1
2. 数据处理：Python 流水线（抓取 -> 提取 -> 分类 -> 清洗）
3. 看板：Jinja2 模板 + Chart.js，生成单个静态 index.html
4. 部署：把 dashboard/index.html 推到 GitHub Pages 即可在线访问

快速开始
--------
    pip install -r requirements.txt
    python main.py

运行完成后，双击 dashboard/index.html 查看看板。

先验证数据源连通性（可选）：
    python test_day1.py

目录结构
--------
    main.py               主入口：一条命令串联全流程
    test_day1.py          Day1 数据源探测脚本（API 连通性验证）
    config.py             全局配置（API、检索词、字段、路径）
    pipeline/
      fetch.py            分页抓取 + 按文档号去重
      extract.py          从标题解析国家 / 产品 / 行业
      classify.py         公告类型分类（优先级规则，见文件注释）
      clean.py            非空校验、日期校验、去重、排序
      report.py           统计聚合 + 渲染 Jinja2 模板
    templates/
      dashboard.html.j2   看板模板（Chart.js：趋势折线 + 国别/行业柱状 + 明细表）
    data/                 输出的 notices.csv（已 gitignore）
    dashboard/            输出的 index.html（已 gitignore）

实现要点（复刻原帖踩过的坑）
---------------------------
1. 先调研再动手：官网有免费 API，就不要写爬虫。
2. 分类规则有优先级：先匹配具体词（如 rescission / administrative review），
   再匹配宽泛词，否则 Final Results of Administrative Review 会被误分。
3. Jinja2 中取字典字段必须写 row["title"]，
   写成 row.title 会被解析成 dict 的内置方法，导致表格整列空白。
4. antidumping / countervailing 两个检索词的结果有重叠，
   必须按 document_number 去重。

免责声明：本项目为对公开赛事作品的技术复现，仅供学习参考。

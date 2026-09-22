"""全局配置：API 地址、检索条件、输出路径"""
from pathlib import Path

# Federal Register 官方免费 JSON API，无需注册、无需认证
API_URL = "https://www.federalregister.gov/api/v1/documents.json"

# 只查国际贸易管理局（ITA）发布的公告：反倾销 / 反补贴的主管机构
AGENCY = "international-trade-administration"

# 两个检索词的结果有重叠，下游按 document_number 去重
SEARCH_TERMS = ["countervailing duty", "antidumping duty"]

# 只请求需要的字段，减小响应体积
FIELDS = [
    "title", "type", "publication_date", "html_url",
    "pdf_url", "document_number", "citation", "agencies",
]

# 可选：限定公告日期范围（MM/DD/YYYY），None 表示不限
START_DATE = None
END_DATE = None

PER_PAGE = 100          # API 单页上限 1000，取 100 更稳
REQUEST_INTERVAL = 0.4  # 礼貌抓取：请求间隔（秒）
TIMEOUT = 30

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DASHBOARD_DIR = BASE_DIR / "dashboard"
TEMPLATE_DIR = BASE_DIR / "templates"
CSV_PATH = DATA_DIR / "notices.csv"

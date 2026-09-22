"""字段提取：从公告标题解析涉案国家、产品、行业。

真实标题格式（实测）：
  "Tin Mill Products From the People's Republic of China:
   Preliminary Affirmative Determination of Sales at Less Than Fair Value ..."
即「产品 From 国家: 动作」。冒号前的部分承担国家和产品信息。
"""
import re

from .classify import classify_notice

# 常见涉案国家/地区 -> 中文名（匹配时小写、去掉开头 the）
COUNTRIES = {
    "people's republic of china": "中国", "china": "中国",
    "republic of korea": "韩国", "south korea": "韩国", "korea": "韩国",
    "republic of türkiye": "土耳其", "turkiye": "土耳其", "turkey": "土耳其",
    "socialist republic of vietnam": "越南", "vietnam": "越南",
    "japan": "日本", "india": "印度", "mexico": "墨西哥",
    "taiwan": "中国台湾", "thailand": "泰国", "indonesia": "印度尼西亚",
    "malaysia": "马来西亚", "brazil": "巴西", "canada": "加拿大",
    "germany": "德国", "italy": "意大利", "france": "法国",
    "united kingdom": "英国", "spain": "西班牙", "netherlands": "荷兰",
    "belgium": "比利时", "poland": "波兰",
    "russian federation": "俄罗斯", "russia": "俄罗斯",
    "ukraine": "乌克兰", "australia": "澳大利亚", "argentina": "阿根廷",
    "republic of south africa": "南非", "south africa": "南非",
    "united arab emirates": "阿联酋", "saudi arabia": "沙特阿拉伯",
    "egypt": "埃及", "greece": "希腊", "austria": "奥地利",
    "sweden": "瑞典", "norway": "挪威", "finland": "芬兰",
    "denmark": "丹麦", "portugal": "葡萄牙", "czech republic": "捷克",
    "romania": "罗马尼亚", "hungary": "匈牙利", "philippines": "菲律宾",
    "singapore": "新加坡", "pakistan": "巴基斯坦", "bangladesh": "孟加拉国",
    "cambodia": "柬埔寨", "morocco": "摩洛哥", "tunisia": "突尼斯",
    "chile": "智利", "colombia": "哥伦比亚", "peru": "秘鲁",
    "kazakhstan": "哈萨克斯坦", "oman": "阿曼", "qatar": "卡塔尔",
    "kuwait": "科威特", "bahrain": "巴林", "israel": "以色列",
    "new zealand": "新西兰", "sri lanka": "斯里兰卡",
}

# 产品关键词 -> 行业。同样有优先级：越具体的词越靠前。
INDUSTRY_RULES = [
    ("有色金属", ["copper", "zinc", "magnesium", "titanium", "nickel"]),
    ("钢铁", ["steel", "tin mill", "tinplate", "rebar", "wire rod",
              "pipe", "tube", "iron", "nail", "staple"]),
    ("铝制品", ["aluminum", "aluminium", "foil", "extrusion"]),
    ("轮胎", ["tire", "tyre"]),
    ("光伏", ["solar", "photovoltaic", "crystalline silicon"]),
    ("化工", ["chemical", "acid", "resin", "polyvinyl", "polyethylene",
              "polypropylene", "glycine", "citric", "fertilizer", "urea"]),
    ("造纸", ["paper"]),
    ("家具家居", ["furniture", "mattress", "cabinet", "bedroom"]),
    ("水产", ["shrimp", "fish", "seafood", "salmon", "catfish", "crawfish"]),
    ("纺织服装", ["textile", "fabric", "garment", "apparel", "staple fiber"]),
    ("木制品", ["wood", "plywood", "hardwood", "flooring", "moulding"]),
    ("玻璃", ["glass"]),
    ("陶瓷建材", ["ceramic", "tile", "quartz", "granite", "cement", "stone"]),
    ("机电", ["battery", "lithium", "motor", "generator", "transformer",
              "wind tower", "appliance"]),
]


def _country_cn(name):
    """英文名转中文名；查不到则返回原文。"""
    key = re.sub(r"^the\s+", "", name.strip(), flags=re.IGNORECASE).lower()
    return COUNTRIES.get(key, name.strip())


def _parse_head(head):
    """解析冒号前的「产品 From 国家」结构。"""
    parts = re.split(r"\s+[Ff]rom\s+", head, maxsplit=1)
    if len(parts) == 2:
        product = parts[0].strip()
        # 多涉案国：如 'India and the Republic of Türkiye'
        raw_countries = re.split(r"\s+and\s+|\s*,\s*|\s*&\s*", parts[1])
        countries = [_country_cn(c) for c in raw_countries if c.strip()]
        country = "、".join(dict.fromkeys(countries)) or "未识别"
    else:
        product = head.strip()
        country = "未识别"
    return product, country


def _industry_of(product):
    p = (product or "").lower()
    for label, keywords in INDUSTRY_RULES:
        if any(k in p for k in keywords):
            return label
    return "其他"


def enrich(doc):
    """把一条 API 原始记录扩展为结构化行。"""
    title = doc.get("title") or ""
    head = title.split(":", 1)[0]
    product, country = _parse_head(head)
    return {
        "document_number": doc.get("document_number"),
        "publication_date": doc.get("publication_date"),
        "notice_type": classify_notice(title),
        "country": country,
        "product": product,
        "industry": _industry_of(product),
        "title": title,
        "html_url": doc.get("html_url"),
    }

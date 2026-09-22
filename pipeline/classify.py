"""公告类型分类：立案 / 初裁 / 终裁 / 复审 / 命令 / 终止。

注意：规则按优先级从上到下匹配，命中即返回。
开发时曾因匹配顺序错误（宽泛词排在前面）导致约 10% 误分，
例如 "Final Results of Antidumping Duty Administrative Review"
若先匹配 final 相关词就会被误判为终裁。
调整为「越具体越靠前」的顺序后验收通过。
"""

RULES = [
    # 越具体的规则越靠前
    ("终止", ["termination", "revocation"]),
    ("复审", ["administrative review", "sunset review", "changed circumstances review",
              "new shipper review", "scope ruling", "circumvention",
              "rescission", "final results", "preliminary results"]),
    ("终裁", ["final determination", "final affirmative determination",
              "final negative determination"]),
    ("初裁", ["preliminary determination", "preliminary affirmative",
              "postponement of preliminary"]),
    ("命令", ["duty order", "duty orders", "amended order", "continuation of",
              "finding", "suspended investigation"]),
    ("立案", ["initiation"]),
]


def classify_notice(title):
    t = (title or "").lower()
    for label, keywords in RULES:
        if any(k in t for k in keywords):
            return label
    return "其他"

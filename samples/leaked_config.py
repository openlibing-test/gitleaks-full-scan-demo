"""示例文件：故意包含一个伪造的凭据，用于验证 gitleaks 扫描链路。

该值由 .gitleaks.toml 中的演示规则 openlibing-demo-token 匹配，
不是任何真实服务的密钥，也不会命中 GitHub 的推送保护。
真实仓库接入时删除本文件与本规则。
"""

DEMO_TOKEN = "demo_secret_a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6"


def build_headers() -> dict:
    return {"Authorization": f"Bearer {DEMO_TOKEN}"}

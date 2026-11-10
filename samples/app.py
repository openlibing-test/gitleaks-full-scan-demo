"""示例文件：干净代码，正常情况下不应产生任何 gitleaks 告警。"""

import os


def get_endpoint() -> str:
    return os.environ.get("DEMO_ENDPOINT", "https://example.com/api")


def main() -> None:
    print(f"endpoint = {get_endpoint()}")


if __name__ == "__main__":
    main()

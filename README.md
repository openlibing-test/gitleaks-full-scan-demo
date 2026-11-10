# gitleaks-full-scan-demo

Gitleaks 接入 GitHub Actions 的示例仓库：验证「gitleaks 扫描 → SARIF → openLiBing 平台可视化」全链路。

- 归属：`openlibing-test`（测试组织）
- 平台：GitHub Actions + openLiBing（OIDC 免密上传，`env_type: beta`）
- 工具版本：gitleaks v8.30.1（linux x64 二进制随仓提交，运行时不下载）

## 目录结构

```text
.
├── .github/
│   ├── bin/
│   │   ├── gitleaks            # gitleaks v8.30.1 linux x64 二进制（mode 100755）
│   │   └── gitleaks.LICENSE    # 上游 MIT LICENSE
│   └── workflows/
│       ├── gitleaks-scan.yml       # 场景二：全量扫描
│       └── gitleaks-precommit.yml  # 场景一：pre-commit 集成
├── .gitleaks.toml              # 规则配置（内置规则 + 演示规则 + 允许列表），两场景共享
├── .pre-commit-config.yaml     # pre-commit 钩子定义
└── samples/
    ├── app.py                  # 干净代码
    └── leaked_config.py        # 故意包含伪造凭据，用于产生告警
```

## 两条工作流

| 工作流 | 场景 | 步骤 |
| --- | --- | --- |
| `gitleaks-scan.yml` | workflow 全量扫描 | checkout → 运行 `gitleaks dir .` 输出 SARIF → `upload-sarif-action` 上传 |
| `gitleaks-precommit.yml` | pre-commit 集成 | checkout → setup-python → `pre-commit-action` 执行钩子并收集 SARIF → `upload-sarif-action` 上传 |

两者都只在 `workflow_dispatch` 与 `push: main` 触发，避免 Fork PR 拿不到 `id-token` 导致上传失败。

## 本地复现

```bash
# Windows 或 macOS 请使用对应平台的 gitleaks 二进制
chmod +x .github/bin/gitleaks
.github/bin/gitleaks dir . --config .gitleaks.toml --verbose \
  --report-format sarif --report-path gitleaks.sarif

# pre-commit 方式
pip install pre-commit
pre-commit run --all-files
```

`samples/leaked_config.py` 中的 `DEMO_TOKEN` 由 `.gitleaks.toml` 的演示规则 `openlibing-demo-token` 命中，因此本地扫描必然产生 1 条告警（exit code 1），属预期结果。

## 验证口径

| 检查点 | 期望 |
| --- | --- |
| Actions 运行状态 | 两条工作流均 success（扫描发现泄露不使 job 失败） |
| 日志-来源标记 | `[INFO] 来源标记: GITHUB_ACTION` |
| 日志-换证 | 提供商 `GitHubActions`、委托 `github-actions` |
| OBS | 桶 `openlibing-github-action`，key 形如 `gitleaks-results/<repo>/<yyyymmdd.hh>/<runId>/gitleaks.sarif` |
| 回调 | `/codescan/v1/result/receive` 返回 `{"code":200,"msg":"success"}` |
| 前端 | beta 代码检查页筛选 GitHub 平台可见 `openlibing-demo-token` 告警 |

## 注意

- 演示规则与 `samples/leaked_config.py` 仅用于验证链路，真实仓库接入时请删除，改用内置规则或项目自定义规则。
- `.gitleaks.toml` 的允许列表排除了 `.github/bin/` 与扫描产物，避免二进制和 SARIF 文件被二次扫描。
- 官方 gitleaks 仓库的 pre-commit 钩子使用 `gitleaks git --staged`，CI 干净检出场景下空转；本仓改用 `repo: local` + `language: system` 执行 `dir .` 全量扫描。
- `upload-sarif-action` 引用 `@source-platform-detection`（平台判定分支），前置版本需支持 GitHub 平台判定与 OIDC；稳定后可改为 tag 或 commit SHA。
- 上游 gitleaks 采用 MIT 协议，二进制随仓分发时保留 `gitleaks.LICENSE`。

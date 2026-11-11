'use strict';

// 探针：输出 action 进程实际运行的 Node 版本与平台信息，
// 主版本 < 20 时非零退出，便于直接判定 runs.using 是否真的生效。
const major = Number(process.versions.node.split('.')[0]);
console.log(`node runtime: ${process.versions.node}`);
console.log(`platform: ${process.platform} ${process.arch}`);
console.log(`execPath: ${process.execPath}`);

if (major < 20) {
  console.error(`NODE_RUNTIME_TOO_OLD: expected >= 20, actual ${process.versions.node}`);
  process.exit(1);
}
console.log('NODE_RUNTIME_OK');

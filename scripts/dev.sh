#!/bin/bash
# dev.sh - 同步数据并启动 Hugo 本地开发服务器
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMPL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$IMPL_DIR"

# 1. 先同步数据
echo "=== Syncing data ==="
bash "$SCRIPT_DIR/sync-data.sh"

# 2. 启动开发服务器
echo ""
echo "=== Starting Hugo dev server ==="
hugo server -D --bind 0.0.0.0 --port 1313

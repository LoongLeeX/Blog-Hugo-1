#!/bin/bash
# build.sh - 同步数据并构建 Hugo 站点
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMPL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$IMPL_DIR"

# 1. 先同步数据
echo "=== Step 1: Sync data ==="
bash "$SCRIPT_DIR/sync-data.sh"

# 2. 构建 Hugo
echo ""
echo "=== Step 2: Build Hugo site ==="
hugo --minify

echo ""
echo "=== Build complete ==="
echo "Output: ${IMPL_DIR}/public/"

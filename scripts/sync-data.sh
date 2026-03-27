#!/bin/bash
# sync-data.sh - 从 blog-data 同步内容到 Hugo 项目
# 用法: ./scripts/sync-data.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMPL_DIR="$(dirname "$SCRIPT_DIR")"
BLOG_DATA="${IMPL_DIR}/../../blog-data"

CONTENT_DIR="${IMPL_DIR}/content/posts"
STATIC_DIR="${IMPL_DIR}/static"

echo "=== Syncing blog data to Hugo implementation ==="
echo "Source: ${BLOG_DATA}"
echo "Target: ${IMPL_DIR}"

# 1. 同步并转换 Markdown 文件
echo ""
echo "[1/3] Syncing posts..."
mkdir -p "$CONTENT_DIR"

count=0
for f in "$BLOG_DATA"/posts/*.md; do
    [ -f "$f" ] || continue
    filename=$(basename "$f")
    # 替换相对路径为 Hugo 静态路径
    sed \
        -e 's|\.\./images/|/bi/|g' \
        -e 's|\.\./diagrams/drawio/|/drawio/|g' \
        "$f" > "$CONTENT_DIR/$filename"
    count=$((count + 1))
done
echo "  Synced $count posts"

# 2. 同步图片
echo "[2/3] Syncing images..."
mkdir -p "$STATIC_DIR/bi"
rsync -av --delete --quiet "$BLOG_DATA/images/" "$STATIC_DIR/bi/"
echo "  Done"

# 3. 同步图表
echo "[3/3] Syncing diagrams..."
mkdir -p "$STATIC_DIR/drawio"
rsync -av --delete --quiet "$BLOG_DATA/diagrams/drawio/" "$STATIC_DIR/drawio/"
echo "  Done"

# 4. 同步其他静态文件 (CNAME 等)
if [ -f "$BLOG_DATA/../blog-impl/hugo-tailwind/CNAME" ]; then
    cp "$BLOG_DATA/../blog-impl/hugo-tailwind/CNAME" "$STATIC_DIR/"
fi

echo ""
echo "=== Sync complete ==="
echo "Posts: $count | Images: $(ls "$STATIC_DIR/bi/" 2>/dev/null | wc -l | tr -d ' ') | Diagrams: $(ls "$STATIC_DIR/drawio/" 2>/dev/null | wc -l | tr -d ' ')"

!/bin/bash


#
获取当前 shell 脚本所在目录
# 获取当前 shell 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印当前 shell 脚本所在目录
echo "当前 shell 脚本所在目录: $SCRIPT_DIR"

cd $SCRIPT_DIR

hugo server -disableFastRender



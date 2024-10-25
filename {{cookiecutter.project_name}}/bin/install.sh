# 初始化安装脚本
# 获取脚本文件目录
BIN_DIR=$(dirname "$(readlink -f "$0")")
# 获取项目目录
PROJECT_DIR=$(dirname "$BIN_DIR")
echo "当前项目路径: $PROJECT_DIR"
cd "$PROJECT_DIR"
echo "切换到项目目录: $PROJECT_DIR"
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "开始创建虚拟环境"
    python3 -m venv venv
    echo "创建虚拟环境完成"
    echo "切换虚拟环境"
    source venv/bin/activate
    echo "开始安装poetry"
    pip3 install poetry
    echo "poetry安装完成"
    echo "开始更新poetry lock"
    poetry lock
    echo "更新poetry lock完成"
    echo "开始安装生产环境依赖"
    poetry install --only main
    echo "安装生产环境依赖完成"
    echo "退出虚拟环境"
    echo "项目初始化安装完成"
    deactivate
else
    echo "虚拟环境已存在, 无需安装虚拟环境"
fi

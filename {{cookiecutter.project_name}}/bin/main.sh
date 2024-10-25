# 获取脚本文件目录
BIN_DIR=$(dirname "$(readlink -f "$0")")
# 获取项目目录
PROJECT_DIR=$(dirname "$BIN_DIR")
echo "当前项目路径: $PROJECT_DIR"
# 进入目录
cd "$PROJECT_DIR"
echo "切换到项目目录: $PROJECT_DIR"
echo "拉取最新项目代码"
git pull
echo "切换虚拟环境"
source venv/bin/activate
echo "开始安装生产环境依赖"
poetry install --only main
echo "安装生产环境依赖完成"
echo "开始检查是否已存在运行中的进程"
pids=$(pgrep -f '{{cookiecutter.project_name}}-[A-Za-z0-9_]*-py3.[0-9]+/bin/main')
if [ -z "$pids" ]; then
  echo "无正在运行中的进程, 忽略"
else
  # 通过for循环遍历所有进程ID
  for pid in $pids; do
    echo "存在正在运行中的进程: $pid, 即将终止进程..."
    kill "$pid" # 使用引号以确保ID作为参数正确传递
    if [ $? -eq 0 ]; then
      echo "进程: $pid 已被成功终止"
    else
      echo "进程: $pid 终止失败"
    fi
  done
fi
# 执行命令
echo "开始执行命令"
nohup poetry run main --env dev >> /dev/null 2>&1 &
echo "执行成功"
echo "退出虚拟环境"
deactivate

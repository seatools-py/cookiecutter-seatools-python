import os
from .common import mkdir, create_file, add_poetry_script, add_docker_compose_script


def generate_flask(project_dir: str, package_dir: str, override: bool = False, *args, **kwargs):
    """生成flask模板代码"""
    def gen_flask_dir():
        """生成flask目录"""
        flask_dir = package_dir + os.sep + 'flask'
        flask_init_py = flask_dir + os.sep + '__init__.py'
        flask_app_py = flask_dir + os.sep + 'app.py'
        mkdir(flask_dir)
        create_file(flask_init_py, override=override)
        create_file(flask_app_py, '''from flask import Flask
from seatools.models import R
from uvicorn.middleware.wsgi import WSGIMiddleware
from {{ cookiecutter.package_name }}.config import get_config_dir
from seatools import ioc
import os
from {{ cookiecutter.package_name }}.logger import setup_loguru, setup_uvicorn, setup_sqlalchemy
from loguru import logger

# 运行ioc
ioc.run(scan_package_names='{{cookiecutter.package_name}}',
        config_dir=get_config_dir(),
        # db 模块依赖 sqlalchemy, 过滤扫描防止未使用 db 场景报错
        exclude_modules=['{{cookiecutter.package_name}}.db'],
        )

# 设置日志文件
setup_loguru('flask_{{ cookiecutter.project_name }}.log', label='flask')
setup_sqlalchemy('flask_{{ cookiecutter.project_name }}.sqlalchemy.log', label='flask')
setup_uvicorn('flask_{{ cookiecutter.project_name }}.uvicorn.log', label='flask')
app = Flask(__name__)


@app.get('/')
def hello():
    logger.info('Hello {{cookiecutter.project_name}} by Flask!')
    return R.ok(data='Hello {{cookiecutter.project_name}} by Flask!').model_dump()


# wsgi 转 asgi
asgi_app = WSGIMiddleware(app)
''', override=override)

    def gen_flask_cmd():
        """生成flask命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        flask_cmd_main_py = cmd_dir + os.sep + 'flask_main.py'
        create_file(flask_cmd_main_py, '''import os
import sys
import multiprocessing
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg, get_config_dir
from {{ cookiecutter.package_name }}.logger import setup, setup_uvicorn, setup_sqlalchemy
from {{ cookiecutter.package_name }} import utils
from typing import Optional
from seatools import ioc
from seatools.env import get_env
import uvicorn


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.option('--host', default='127.0.0.1', help='服务允许访问的ip, 若允许所有ip访问可设置0.0.0.0')
@click.option('--port', default=8000, help='服务端口')
@click.option('--workers', default=1, help='工作进程数')
@click.option('--reload', default=None, help='是否热重启服务器, 默认情况下dev环境开始热重启, test与pro环境不热重启, true: 开启, false: 不开启')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         host: Optional[str] = '127.0.0.1',
         port: Optional[int] = 8000,
         workers: Optional[int] = 1,
         reload: Optional[bool] = None) -> None:
    """{{cookiecutter.friendly_name}} Flask cmd."""
    # 如果是pyinstaller环境, 先把当前路径设置为执行路径, 以便于无参运行
    if utils.is_pyinstaller_env():
        os.environ['PROJECT_DIR'] = os.path.dirname(sys.executable)
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    if reload is None:
        reload = get_env().is_dev()
    # 运行ioc
    ioc.run(scan_package_names='{{cookiecutter.package_name}}',
            config_dir=get_config_dir(),
            # db 模块依赖 sqlalchemy, 过滤扫描防止未使用 db 场景报错
            exclude_modules=['{{cookiecutter.package_name}}.db'],
            )
    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup_loguru('flask_{}.log'.format(file_name), level=log_level, label='flask')
    setup_sqlalchemy('flask_{}.sqlalchemy.log'.format(file_name), level=log_level, label='flask')
    setup_uvicorn('flask_{}.uvicorn.log'.format(file_name), level=log_level, label='flask')
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    uvicorn.run('{{cookiecutter.package_name}}.flask.app:asgi_app', host=host, port=port, workers=workers, reload=reload)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
''', override=override)
        add_poetry_script(project_dir, 'flask = "{{cookiecutter.package_name}}.cmd.flask_main:main"')

        bin_dir = project_dir + os.sep + 'bin'
        bin_file = bin_dir + os.sep + 'flask.sh'
        create_file(bin_file, '''# 获取脚本文件目录
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
pids=$(pgrep -f '{{cookiecutter.project_name}}/venv/bin/flask')
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
pids=$(pgrep -f '{{cookiecutter.project_name}}-[A-Za-z0-9_\\\\-]*-py3.[0-9]+/bin/flask')
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
# 执行命令 --workers 工作进程数, 正式环境可根据CPU核数设置
nohup poetry run flask --host 0.0.0.0 --port 8000 --env pro --workers 4 >> /dev/null 2>&1 &
echo "执行成功"
echo "退出虚拟环境"
deactivate
''')
        dockerfile_path = project_dir + os.sep + 'flask.Dockerfile'
        create_file(dockerfile_path, '''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

RUN poetry add flask uvicorn[standard]

CMD ["poetry", "run", "flask", "--env", "pro", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
''', override=override)
        add_docker_compose_script(project_dir, '''  flask:
    container_name: {{cookiecutter.project_name}}_flask
    build:
      context: .
      dockerfile: flask.Dockerfile
    image: {{cookiecutter.project_name}}_flask:latest
    volumes:
      - ".:/app"
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
''')

    gen_flask_dir()
    gen_flask_cmd()

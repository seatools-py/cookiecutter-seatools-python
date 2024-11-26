import os
import sys
import click
from loguru import logger
from typing import Optional
from seatools.logger.setup import setup_loguru, setup_logging

from {{ cookiecutter.package_name }}.config import cfg
from {{ cookiecutter.package_name }} import utils
from {{ cookiecutter.package_name }}.boot import start


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.option('--label', default='main', help='日志标签, 默认: main')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         label: Optional[str] = 'main') -> None:
    """{{cookiecutter.friendly_name}} cmd."""
    # 如果是pyinstaller环境, 先把当前路径设置为执行路径, 以便于无参运行
    if utils.is_pyinstaller_env():
        os.environ['PROJECT_DIR'] = os.path.dirname(sys.executable)
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    if label:
        os.environ['LABEL'] = label

    # 启动项目依赖
    start()

    # 设置日志文件
    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup_loguru(utils.get_log_path('{}.log'.format(file_name)), level=log_level,
                 extra={'project': cfg().project_name, 'label': 'main'})
    # 设置日志sqlalchemy
    setup_logging(utils.get_log_path('{}.sqlalchemy.log'.format(file_name)), 'sqlalchemy', level=log_level,
                  extra={'project': cfg().project_name, 'label': 'main'})
    logger.info('运行成功, 当前项目: {}', cfg().project_name)


if __name__ == "__main__":
    main()

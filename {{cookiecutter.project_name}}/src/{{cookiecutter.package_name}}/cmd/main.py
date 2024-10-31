import os
import sys
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg, get_config_dir
from {{ cookiecutter.package_name }}.logger import setup_loguru, setup_sqlalchemy
from {{ cookiecutter.package_name }} import utils
from seatools import ioc
from typing import Optional


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO') -> None:
    """{{cookiecutter.friendly_name}} cmd."""
    # 如果是pyinstaller环境, 先把当前路径设置为执行路径, 以便于无参运行
    if utils.is_pyinstaller_env():
        os.environ['PROJECT_DIR'] = os.path.dirname(sys.executable)
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    # 运行ioc
    ioc.run(scan_package_names='{{cookiecutter.package_name}}',
            config_dir=get_config_dir(),
            # db 模块依赖 sqlalchemy, 过滤扫描防止未使用 db 场景报错
            exclude_modules=['{{cookiecutter.package_name}}.db'],
            )
    # 设置日志文件
    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup_loguru('{}.log'.format(cfg().project_name), level=log_level, label='main')
    setup_sqlalchemy('{}.sqlalchemy.log'.format(cfg().project_name), level=log_level, label='main')
    logger.info('运行成功, 当前项目: {}', cfg().project_name)


if __name__ == "__main__":
    main()

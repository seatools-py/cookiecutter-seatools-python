import click
from loguru import logger
from typing import Optional
from .generators import *
from {{ cookiecutter.package_name }}.config import get_project_dir, get_package_dir


@click.group()
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main() -> None:
    """代码生成命令行工具"""
    pass


@main.command()
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def fastapi(override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    logger.info('开始生成[fastapi]模板代码')
    generate_fastapi(project_dir=project_dir, package_dir=package_dir, override=override)
    logger.success('生成[fastapi]模板代码完成')


@main.command()
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def flask(override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    logger.info('开始生成[flask]模板代码')
    generate_flask(project_dir=project_dir, package_dir=package_dir, override=override)
    logger.success('生成[flask]模板代码完成')


@main.command()
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--task_class', '--class', default=None, help='任务类名, 支持驼峰、下划线名称解析, 生成的文件名下划线分隔, 类名驼峰, 例如: HelloWorld, 生成task模板时必填该参数')
@click.option('--task_name', '--name', default="默认任务", help='任务名称, 中英文任务描述, 默认值: 默认任务')
@click.option('--async', is_flag=True, default=False, help='是否创建异步任务, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def task(override: Optional[bool] = False,
         task_class: Optional[str] = None,
         task_name: Optional[str] = "默认任务",
         is_async: Optional[bool] = False):
    if not task_class:
        logger.error('[--task_class]参数不能为空')
        return
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_task(project_dir=project_dir, package_dir=package_dir,
                  task_class=task_class, task_name=task_name,
                  override=override, is_async=is_async)


@main.command()
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy(override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_scrapy(project_dir=project_dir, package_dir=package_dir, override=override)


@main.command()
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def django(override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_django(project_dir=project_dir, package_dir=package_dir, override=override)


@main.command()
@click.option('--name', default=None, help='cmd命令名称, 使用poetry run {name} 执行生成的命令, 必填')
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--label', default=None, help='日志label, 不填默认为命令名称')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def cmd(name: str, label: Optional[str] = None, override: Optional[bool] = False):
    if not name:
        logger.error('[--name]参数不能为空')
        return
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_cmd(project_dir=project_dir, package_dir=package_dir, override=override, command=name, label=label)


if __name__ == "__main__":
    main()

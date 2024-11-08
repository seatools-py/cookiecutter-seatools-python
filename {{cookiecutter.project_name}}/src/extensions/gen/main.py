import os
import click
from loguru import logger
from typing import Optional
from seatools.codegen.ioc import *
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
@click.option('--is_async', '--async', is_flag=True, default=False, help='是否创建异步任务, 默认false')
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


@main.group()
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy():
    pass


@scrapy.command('init')
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy_init(override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_scrapy(project_dir=project_dir, package_dir=package_dir, override=override)


@scrapy.command('genspider')
@click.argument('name')
@click.argument('domain')
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy_genspider(name: str,
                     domain: str,
                     override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    generate_scrapy_spider(project_dir=project_dir, package_dir=package_dir,
                           name=name, domain=domain, override=override)


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


@main.command()
@click.option("--name", default=None, help='protobuf文件名称, proto文件仅支持在src/proto目录下, 例如存在xxx.proto, 则name应该传递xxx, 若不传递该参数, 则默认将src/proto目录下所有proto文件一起生成')
@click.option("--pyi", is_flag=True, default=False, help='是否生成pyi文件, 默认false不生成')
@click.option('--override', is_flag=True, default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def grpc(name: Optional[str] = None, pyi: Optional[bool] = False, override: Optional[bool] = False):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    proto_dir = get_project_dir() + os.sep + 'src' + os.sep + 'proto'
    if not os.path.exists(proto_dir):
        logger.error("proto目录[{}]不存在, 无法生成pb2代码".format(proto_dir))
        return
    if not name:
        import glob
        names = [file.replace('.proto', '').split(os.sep)[-1] for file in glob.glob(os.path.join(proto_dir, '*.proto'))]
    else:
        names = [name]

    for name in names:
        generate_grpc(project_dir, package_dir, override, name, pyi=pyi)
        # 仅第一次需要override, 防止多次重复override
        override = False


if __name__ == "__main__":
    main()

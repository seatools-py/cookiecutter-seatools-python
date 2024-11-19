import click
from typing import Optional
from {{ cookiecutter.package_name }}.config import get_project_dir, get_package_dir, get_extensions_dir
from seatools.ext.chrome import list_chrome, common_download_chrome
from loguru import logger
from {{ cookiecutter.package_name }}.utils import get_absolute_path

__allow_system__ = ["linux64", "mac-arm64", "mac-x64", "win64", "win32"]
__allow_type__ = ['chrome', 'chromedriver', 'all']


@click.group()
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main() -> None:
    """谷歌工具"""
    return None


@main.command()
@click.version_option(version="1.0.0", help='查看命令版本')
@click.option('--grep', default=None, help='筛选查询')
@click.help_option('-h', '--help', help='查询所有chrome/chromedriver版本, 仅支持114以上版本')
def list(grep: Optional[str] = None):
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    logger.success('\n'.join([item for item in list_chrome(project_dir=project_dir, package_dir=package_dir) if not grep or grep in item]))


@main.command()
@click.option('-v', '--version', default=None, help='下载的chrome版本, 该参数不能为空')
@click.option('-s', '--system', default='win64', help='下载的chrome系统, 支持: linux64, mac-arm64, mac-x64, win64, win32, 默认: win64')
@click.option('-t', '--type', default='chromedriver',
              help='下载的chrome类型, 支持: chrome, chromedriver, all(同时下载chrome和chromedriver) 默认: chromedriver')
@click.help_option('-h', '--help', help='下载chrome, 并保存至项目extensions目录')
def download(version: Optional[str] = None,
             system: Optional[str] = 'win64',
             type: Optional[str] = 'chromedriver'):
    if not version:
        logger.error('版本不能为空')
        exit(1)
    if system not in __allow_system__:
        logger.error('系统[{}]不支持, 请使用-h参数查看支持的系统类型'.format(system))
        exit(1)
    if type not in __allow_type__:
        logger.error('类型[{}]不支持, 请使用-h参数查看支持的系统类型'.format(type))
        exit(1)
    project_dir = get_project_dir()
    package_dir = get_package_dir()
    installer_dir = get_absolute_path(get_extensions_dir())
    if type in ('chrome', 'all'):
        common_download_chrome(project_dir=project_dir, package_dir=package_dir,
                               version=version, system=system, type_='chrome',
                               installer_dir=installer_dir)
    if type in ('chromedriver', 'all'):
        common_download_chrome(project_dir=project_dir, package_dir=package_dir,
                               version=version, system=system, type_='chromedriver',
                               installer_dir=installer_dir)

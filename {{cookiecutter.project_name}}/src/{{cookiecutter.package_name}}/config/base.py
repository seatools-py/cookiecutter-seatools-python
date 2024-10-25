import os

from {{cookiecutter.package_name}}.models.config import Config
from seatools.ioc.config import cfg as ioc_cfg

_cfg = None


def get_project_dir():
    """获取项目目录, 建议读取的所有文件都从项目目录开始

    Returns:
        项目目录路径
    """
    return os.environ.get('PROJECT_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def get_src_dir():
    """获取包目录, 建议读取的所有代码文件都从该目录开始

    Returns:
        项目代码包目录
    """
    return get_project_dir() + os.sep + 'src'


def get_package_dir():
    """获取默认业务包目录, 建议读取的所有业务包文件都从该目录开始

    Returns:
        默认业务包目录
    """
    return get_src_dir() + os.sep + '{{cookiecutter.package_name}}'


def get_extensions_dir():
    """获取拓展目录"""
    return get_project_dir() + os.sep + 'extensions'


def cfg() -> Config:
    """获取配置对象

    Returns:
        配置对象
    """
    global _cfg
    if not _cfg:
        _cfg = Config(**(ioc_cfg()))
    return _cfg

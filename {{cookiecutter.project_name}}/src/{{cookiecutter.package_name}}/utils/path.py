import os
from typing import Optional
from {{cookiecutter.package_name}}.config import get_project_dir, cfg


def get_absolute_path(path: Optional[str] = None) -> str:
    """获取路径的绝对路径地址, 若path是一个绝对路径, 则直接返回, 否则返回以当前项目为根目录拼接的相对路径的绝对路径

    Args:
        path: 相对路径/绝对路径

    Returns:
        绝对路径
    """
    if not path:
        return get_project_dir()
    if os.path.isabs(path):
        return path
    return get_project_dir() + os.sep + path


def get_log_path(file_name: str) -> str:
    """获取"""
    log_dir = cfg().log_dir or (get_project_dir() + os.sep + 'logs')
    log_dir = log_dir.replace('\\', '/')
    if not log_dir.endswith('/'):
        log_dir += '/'
    return log_dir + file_name

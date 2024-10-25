from .path import get_absolute_path, get_log_path


def is_pyinstaller_env():
    """判断是否是pyinstaller环境"""
    import sys
    return hasattr(sys, 'frozen')

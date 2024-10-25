import logging
from logging.handlers import TimedRotatingFileHandler
from seatools.logger import get_loguru_adapter_logging_formatter
from {{cookiecutter.package_name}}.utils import get_log_path
from {{cookiecutter.package_name}}.config import cfg


def setup_sqlalchemy(file_name,
                     rotation_type: str = 'd',
                     rotation: int = 1,
                     serialize: bool = True,
                     retention_count: int = 3,
                     level: str = 'INFO',
                     label=''):
    """ 设置sqlalchemy日志记录, 与loguru相同的日志格式 """
    # 开启序列化则注入
    if serialize:
        # 增加一个适配loguru序列化的日志格式化器
        formatter_cls = get_loguru_adapter_logging_formatter()
        # 增加一个文件handler
        file_handler = TimedRotatingFileHandler(
            filename=get_log_path(file_name),
            when=rotation_type,
            interval=rotation,
            backupCount=retention_count,
            encoding='utf-8',
        )

        file_handler.setFormatter(formatter_cls('%(message)s', extra={'service_name': cfg().project_name, 'label': label}))
        file_handler.addFilter(lambda e: e.levelno >= logging._nameToLevel[level])
        logging_logger = logging.getLogger('sqlalchemy')
        logging_logger.addHandler(file_handler)

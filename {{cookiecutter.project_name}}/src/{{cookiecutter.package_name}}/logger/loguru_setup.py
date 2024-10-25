from loguru import logger
from {{cookiecutter.package_name}}.config import cfg
from {{cookiecutter.package_name}}.utils import get_log_path
from seatools.logger import setup


def setup_loguru(file_name,
                 rotation="1 days",
                 serialize=True,
                 backtrace=True,
                 diagnose=False,
                 retention="3 days",
                 level='INFO',
                 label=''):
    logger.configure(extra={'service_name': cfg().project_name, 'label': label})
    setup(f'{get_log_path(file_name)}',
           rotation=rotation,
           serialize=serialize,
           backtrace=backtrace,
           diagnose=diagnose,
           retention=retention,
           level=level)

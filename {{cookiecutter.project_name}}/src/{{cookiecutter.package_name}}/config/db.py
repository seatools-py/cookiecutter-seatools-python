from seatools.ioc import Bean, get_environment
from {{cookiecutter.package_name}}.models.config import MultiDBConfig, CommonDBConfig
from {{cookiecutter.package_name}}.db import db_select
from loguru import logger
from typing import get_args
import inspect


@Bean
def init_db_beans():
    db_config_dict = [item[1] for item in inspect.getmembers(MultiDBConfig, lambda a: not (inspect.isroutine(a))) if
                      item[0] == '__annotations__'][0]
    environment = get_environment()
    for attr_name, _type in db_config_dict.items():
        if len(get_args(_type)) > 0:
            _type = get_args(_type)[0]
        config = environment.get_property(f'db.{attr_name}', _type)
        if not isinstance(config, CommonDBConfig):
            logger.warning('DB配置[{}]未继承CommonDBConfig类, 无法自动注入db实例')
            continue
        # 注册bean
        client = db_select(config)
        Bean(name=attr_name, primary=config.primary)(client)

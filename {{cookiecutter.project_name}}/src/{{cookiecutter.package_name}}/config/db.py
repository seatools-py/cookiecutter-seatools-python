from seatools.ioc import Bean, get_environment
from seatools.sqlalchemy.dbconfig import CommonDBConfig
from seatools.sqlalchemy.utils import new_client
from {{cookiecutter.package_name}}.models.config import MultiDBConfig
from {{cookiecutter.package_name}}.config import cfg
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
        client = new_client(config, cfg().sqlalchemy)
        Bean(name=attr_name, primary=config.primary)(client)

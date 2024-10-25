from seatools.sqlalchemy import SqlAlchemyClient, AsyncSqlAlchemyClient
from seatools.env import get_env
from seatools.ioc import Bean, get_environment
from {{cookiecutter.package_name}}.models.config import MultiDBConfig, CommonDBConfig
from loguru import logger
from typing import get_args
from sqlalchemy import URL
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
        client = __new_client(config)
        Bean(name=attr_name, primary=config.primary)(client)
        logger.success('初始化[{}]的[{}], 连接串[{}]', attr_name,
                       AsyncSqlAlchemyClient.__name__ if config.is_async else SqlAlchemyClient.__name__,
                       __gen_sqlalchemy_url(config))


def __new_client(config: CommonDBConfig):
    url = __gen_sqlalchemy_url(config)
    cls = AsyncSqlAlchemyClient if config.is_async else SqlAlchemyClient
    # hive 需要额外处理
    if config.sqlalchemy_schema == 'hive':
        try:
            from pyhive import hive
        except ImportError as e:
            logger.error('未安装pyhive依赖, sqlalchemy无法配置hive')
            raise e
        return cls(url=url, echo=not get_env().is_pro(),
                   creator=lambda: hive.Connection(
                       host=config.host, port=config.port, username=config.user, database=config.db)
                   )
    return cls(url=url, echo=not get_env().is_pro())


def __gen_sqlalchemy_url(config: CommonDBConfig):
    return URL.create(config.sqlalchemy_schema,
                      host=config.host,
                      port=config.port,
                      username=config.user,
                      password=config.password,
                      database=config.db)

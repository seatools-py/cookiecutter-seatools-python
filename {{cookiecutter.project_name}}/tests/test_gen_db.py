from seatools.sqlalchemy import SqlAlchemyClient, Base
from {{ cookiecutter.package_name }}.boot import start


def test_gen_db():
    """通过sqlalchemy model生成表"""
    # 启动ioc
    start()
    cli: SqlAlchemyClient = ioc.Autowired(cls=SqlAlchemyClient)
    Base.metadata.create_all(cli.engine())


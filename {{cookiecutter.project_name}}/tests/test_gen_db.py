from seatools import ioc
from seatools.sqlalchemy import SqlAlchemyClient, Base
from {{ cookiecutter.package_name }}.config import get_config_dir


def test_gen_db():
    """通过sqlalchemy model生成表"""
    # 启动ioc
    ioc.run(scan_package_names='{{cookiecutter.package_name}}',
            config_dir=get_config_dir(),
            exclude_modules=[],
            )
    cli: SqlAlchemyClient = ioc.Autowired(cls=SqlAlchemyClient)
    Base.metadata.create_all(cli.engine())


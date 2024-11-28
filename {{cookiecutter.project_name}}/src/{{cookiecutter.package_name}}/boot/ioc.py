from seatools import ioc
from {{ cookiecutter.package_name }}.config import get_config_dir


def ioc_starter():
    # 运行ioc
    ioc.run(scan_package_names=[
        '{{cookiecutter.package_name}}'
    ],
            config_dir=get_config_dir(),
            # 需要过滤扫描的模块, 示例: {{ cookiecutter.package_name }}.xxx
            exclude_modules=[])

import os

from colorama import Fore
from extensions.gen.generators.common import mkdir, create_file


def generate_grpc(project_dir: str, package_dir: str, override: bool = False,
                  name: str = None,
                  pyi: bool = False,
                  **kwargs):
    """生成grpc代码命令"""
    src_dir = project_dir + os.sep + 'src'
    protobuf_dir = src_dir + os.sep + 'proto'
    protobuf_file = protobuf_dir + os.sep + '{}.proto'.format(name)
    # 检查proto文件是否存在
    if not os.path.exists(protobuf_file):
        print(Fore.RED + "文件: {} 不存在, 无法生成grpc pb2代码".format(protobuf_file))
        return

    grpc_dir = package_dir + os.sep + 'grpc'
    grpc_init_py = grpc_dir + os.sep + '__init__.py'
    mkdir(grpc_dir)
    create_file(grpc_init_py, override=override)

    proto_dir = grpc_dir + os.sep + 'proto'
    proto_init_py = proto_dir + os.sep + '__init__.py'
    mkdir(proto_dir)
    create_file(proto_init_py, override=override)

    from grpc_tools import protoc

    args = [
        "-I{}".format(src_dir),
        "--python_out={}".format(grpc_dir),
        "--grpc_python_out={}".format(grpc_dir),
        "-I{}".format(src_dir),
        protobuf_file,
    ]
    if pyi:
        args.append("--pyi_out={}".format(grpc_dir))
    protoc.main(args)



    # 重写文件
    grpc_pb2_file = proto_dir + os.sep + '{}_pb2.py'.format(name)
    with open(grpc_pb2_file, 'r', encoding='utf-8') as f:
        grpc_pb2_file_content = f.read()
    create_file(grpc_pb2_file, grpc_pb2_file_content, override=True)

    grpc_pb2_grpc_file = proto_dir + os.sep + '{}_pb2_grpc.py'.format(name)
    with open(grpc_pb2_grpc_file, 'r', encoding='utf-8') as f:
        grpc_pb2_grpc_file_content = f.read()
    grpc_pb2_grpc_file_content = grpc_pb2_grpc_file_content.replace('from proto', 'from .')
    create_file(grpc_pb2_grpc_file, grpc_pb2_grpc_file_content, override=True)

    if pyi:
        grpc_pyi_file = proto_dir + os.sep + '{}_pb2.pyi'.format(name)
        with open(grpc_pyi_file, 'r', encoding='utf-8') as f:
            grpc_pyi_file_content = f.read()
        create_file(grpc_pyi_file, grpc_pyi_file_content, override=True)

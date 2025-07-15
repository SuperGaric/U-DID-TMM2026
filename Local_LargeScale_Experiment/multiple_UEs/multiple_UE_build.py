import os
import subprocess

def build_project(directory, imsi):
    # 进入指定的目录
    os.chdir(directory)
    print(f"Building in {directory}...")
    
    # 执行构建命令
    try:
        result = subprocess.run(
            ['./build_oai', '-w', 'USRP', '--ninja', '--nrUE', '--gNB', '--build-lib', 'nrscope', '-C'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Build completed successfully in {directory}")
        print(result.stdout.decode())  # 打印输出结果


        # 修改执行文件
        target_directory = os.path.join(directory, 'ran_build', 'build')
        startup_file_path = os.path.join(target_directory, 'nr-uesoftmodem')
        new_file_name = f"nr-uesoftmodem-{imsi}"
        new_file_path = os.path.join(target_directory, new_file_name)

        if os.path.exists(startup_file_path):
            os.rename(startup_file_path, new_file_path)
            print(f"renamed startup file to {new_file_name}")
        else:
            print(f"startup file not found in {target_directory}")

        

    except subprocess.CalledProcessError as e:
        print(f"Build failed in {directory}")
        print(e.stdout.decode())
        print(e.stderr.decode())

def main():
    count = 5
    base_directory = os.path.expanduser('~/multiple_UEs')  # 修改为你的基础目录路径
    imsi = 208950000000031

    projects = [f"openairinterface5g_copy_{i}" for i in range(1, count + 1)]

    # j = 1
    for project in projects:
        project_path = os.path.join(base_directory, project, 'cmake_targets')
        build_project(project_path, imsi)
        imsi = 1 + imsi

if __name__ == '__main__':
    main()

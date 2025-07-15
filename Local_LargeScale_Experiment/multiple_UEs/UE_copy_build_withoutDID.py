import os
import shutil
import re
import subprocess

def copy_and_modify_file(src, pattern, new_value):
    with open(src, 'r') as file:
        content = file.read()

    # new_content = re.sub(
    #     pattern,
    #     lambda m: f'{m.group(1)}{int(m.group(2)) + increment_by:015d}{m.group(3)}',
    #     content
    # )

    new_content = re.sub(
        pattern,
        lambda m: f'{m.group(1)}{new_value}{m.group(3)}',
        content
    )

    with open(src, 'w') as file:
        file.write(new_content)

def modify_port_in_file(src, pattern, new_value):
    with open(src, 'r') as file:
        content = file.read()

    # new_content = re.sub(
    #     pattern,
    #     lambda m: f'{m.group(1)}{int(m.group(2)) + increment_by}{m.group(3)}',
    #     content
    # )

    new_content = re.sub(
        pattern,
        lambda m: f'{m.group(1)}{new_value}{m.group(3)}',
        content
    )

    with open(src, 'w') as file:
        file.write(new_content)

def modify_files(directory, imsi_pattern, port_pattern, imsi, port):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'usim_interface.c':
                file_path = os.path.join(root, file)
                copy_and_modify_file(file_path,  imsi_pattern, imsi)
            if file == 'nr_nas_msg_sim.c':
                file_path = os.path.join(root, file)
                modify_port_in_file(file_path,  port_pattern, port)

def build_project(directory, imsi, output_directory):
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

        # 修改执行文件名称并移动到目标目录
        # target_directory = os.path.join(directory, 'ran_build', 'build')
        target_directory = os.path.join( 'ran_build', 'build')
        print(f"Checking target directory: {target_directory}")

        startup_file_path = os.path.join(target_directory,'nr-uesoftmodem')
        print(f"Startup file path: {startup_file_path}")

        new_file_name = f"nr-uesoftmodem-{imsi}"
        new_file_path = os.path.join(output_directory, new_file_name)
        print(f"New file path: {new_file_path}")

        # if os.path.exists(target_directory):
        #     print(f"Contents of {target_directory}: {os.listdir(target_directory)}")
        # else:
        #     print(f"Target directory {target_directory} does not exist.")


        if os.path.exists(startup_file_path):
            renamed_startup_file_path = os.path.join(target_directory, new_file_name)
            # os.rename(startup_file_path, renamed_startup_file_path)
            # shutil.move(renamed_startup_file_path, new_file_path)
            shutil.move(startup_file_path, new_file_path)
            print(f"Moved and renamed startup file to {new_file_path}")
        else:
            print(f"Startup file not found in {target_directory}")
            print(f"Contents of {target_directory}: {os.listdir(target_directory)}")

    except subprocess.CalledProcessError as e:
        print(f"Build failed in {directory}")
        print(e.stdout.decode())
        print(e.stderr.decode())

if __name__ == "__main__":
    # 设置相对路径
    # base_directory = os.path.dirname(__file__)
    # base_directory = os.path.join('dmt','home','multiple_UEs')
    base_directory = '/home/dmt/multiple_UEs'
    src_directory = os.path.join(base_directory, 'openairinterface5g_withoutDID')
    imsi_pattern = r'("imsi",\s+"USIM IMSI\\n",\s+0,\s+.strptr=&uicc->imsiStr,\s+.defstrval=")(\d{15})(")'
    port_pattern = r'(server\.sin_port\s*=\s*htons\()(\d+)(\);)'

    # 初始IMSI和端口值的增量
    current_imsi_increment = 0
    current_port_increment = 0
    initial_port = 8080

    # 拷贝5份，每份递增1
    count = 100
    output_directory = os.path.join(base_directory, 'compiled_binaries_withoutDID')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    initial_imsi = 208950000000031

    for i in range(1, count + 1):
        # dst_directory = os.path.join(base_directory, f'openairinterface5g_copy_{i}')
        
        # if not os.path.exists(dst_directory):
        #     shutil.copytree(src_directory, dst_directory)
        
        modify_files(src_directory, imsi_pattern, port_pattern, initial_imsi + current_imsi_increment, initial_port + current_port_increment)
        
        current_imsi_increment += 1
        current_port_increment += 1

        # 编译项目并重命名可执行文件
        project_path = os.path.join(src_directory, 'cmake_targets')
        imsi = initial_imsi + current_imsi_increment - 1
        build_project(project_path, imsi, output_directory)

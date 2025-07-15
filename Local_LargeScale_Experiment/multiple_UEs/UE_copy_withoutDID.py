import os
import shutil
import re

def copy_and_modify_file(src, dst, pattern, increment_by=1):
    with open(src, 'r') as file:
        content = file.read()

    new_content = re.sub(
        pattern,
        lambda m: f'{m.group(1)}{int(m.group(2)) + increment_by:015d}{m.group(3)}',
        content
    )

    with open(dst, 'w') as file:
        file.write(new_content)

def modify_port_in_file(src, dst, pattern, increment_by=1):
    with open(src, 'r') as file:
        content = file.read()

    new_content = re.sub(
        pattern,
        lambda m: f'{m.group(1)}{int(m.group(2)) + increment_by}{m.group(3)}',
        content
    )

    with open(dst, 'w') as file:
        file.write(new_content)

def copy_directory(src_dir, dst_dir, imsi_pattern,  imsi_increment_by=1):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)

    for root, _, files in os.walk(dst_dir):
        for file in files:
            if file == 'usim_interface.c':
                src_file_path = os.path.join(root, file)
                dst_file_path = src_file_path
                copy_and_modify_file(src_file_path, dst_file_path, imsi_pattern, imsi_increment_by)
            # if file == 'nr_nas_msg_sim.c':
            #     src_file_path = os.path.join(root, file)
            #     dst_file_path = src_file_path
            #     modify_port_in_file(src_file_path, dst_file_path, port_pattern, port_increment_by)

if __name__ == "__main__":
    # 设置相对路径
    base_directory = os.path.dirname(__file__)
    # src_directory = os.path.join(base_directory, '01-modified-openairinterface5g')
    src_directory = os.path.join(base_directory, 'openairinterface5g_withoutDID')
    imsi_pattern = r'("imsi",\s+"USIM IMSI\\n",\s+0,\s+.strptr=&uicc->imsiStr,\s+.defstrval=")(\d{15})(")'
    # port_pattern = r'(server\.sin_port\s*=\s*htons\()(\d+)(\);)'

    # 初始IMSI和端口值的增量
    current_imsi_increment = 0
    # current_port_increment = 0
    # initial_port = 8080

    # 拷贝5份，每份递增1
    for i in range(1, 6):
        dst_directory = os.path.join(base_directory, f'openairinterface5g_copy_{i}')
        copy_directory(src_directory, dst_directory, imsi_pattern,  current_imsi_increment)
        current_imsi_increment += 1
        # current_port_increment += 1

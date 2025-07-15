import os
import re
from datetime import datetime
import csv
import subprocess

# 基本路径设置
base_path_ue = '/home/dmt/multiple_UEs/'
base_path_p3Chain = '/home/dmt/Lee-P3chainforOai-main/dper/client/auto/dper_dper4'

#当前ue的数量
count = 5

# 正则表达式用于匹配时间
time_pattern_ue = r'UE启动的时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
time_pattern_p3Chain = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'


# 存储时间的列表
times = []

# 创建timelogsaggregate.csv的文件
output_file = "timelogsaggreaget_core_withoutDID.csv"

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['PDU message received time', 'PDU success time'])


# # 遍历所有相关的目录
# for i in range(1, count + 1):
#     dir_path = os.path.join(base_path_ue, f'openairinterface5g_copy_{i}','cmake_targets','ran_build','build')
#     print(dir_path)
#     log_file_path = os.path.join(dir_path, 'timelogs.txt')
    
#     # 检查文件是否存在
#     if os.path.exists(log_file_path):
#         with open(log_file_path, 'r') as file:
#             # for line in file:
#                 first_line = file.readline()
#                 # match = re.search(time_pattern, line)
#                 match = re.search(time_pattern_ue, first_line)
#                 if match:
#                     # 提取时间并转换为 datetime 对象
#                     time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                     print(time)
#                     times.append(time)

# 改成单个执行文件后，用这个方法

# dir_path = os.path.join(base_path_ue, 'compiled_binaries_withDID')
# print(dir_path)
# log_file_path = os.path.join(dir_path, 'timelogs.txt')

# # 检查文件是否存在
# if os.path.exists(log_file_path):
#     with open(log_file_path, 'r') as file:
#         # for line in file:
#             first_line = file.readline()
#             # match = re.search(time_pattern, line)
#             match = re.search(time_pattern_ue, first_line)
#             if match:
#                 # 提取时间并转换为 datetime 对象
#                 time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print(time)
#                 times.append(time)

# time_pattern1 = r'pdu会话建立信令接受时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
# time_pattern2 = r'转发U-DID时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'



# try:
#     docker_command = 'docker exec -it oai-amf cat timelogs.txt'
#     result = subprocess.run(docker_command, shell = True, check = True, stdout = subprocess.PIPE, text=True)
#     match1 = re.search(time_pattern1, result.stdout)
#     match2 = re.search(time_pattern2, result.stdout)

#     if match1: 
#         PDU_message_received_time = datetime.strptime(match1.group(1), '%Y-%m-%d %H:%M:%S.%f')
#         print("PDU message received time:", PDU_message_received_time)
#     else: 
#         oai_time = None
#     if match2: 
#         UDID_send_BC_time = datetime.strptime(match2.group(1), '%Y-%m-%d %H:%M:%S.%f')
#         print("U-DID send BC time:", UDID_send_BC_time)
#     else: 
#         oai_time = None 
# except subprocess.CalledProcessError as e:
#     print("failed to get time from docker:", e)
#     oai_time = None


time_pattern = re.compile(
    r'(pdu会话建立信令接受时间): '
    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
)

# 初始化变量（避免未定义风险）
PDU_message_received_time  = None


try:
    # 获取 Docker 日志
    docker_command = 'docker exec -it oai-amf cat timelogs.txt'
    result = subprocess.run(
        docker_command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'  # 明确指定编码避免乱码
    )
    # 逐行处理日志
    for line in result.stdout.split('\n'):
        match = time_pattern.search(line)
        if match:
            event_type, time_str = match.groups()
            time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
            
            # 根据事件类型分配时间
            if event_type == 'pdu会话建立信令接受时间':
                PDU_message_received_time = time_obj

    # 打印结果（检查是否为 None）
    print("PDU消息接收时间:", PDU_message_received_time or "未找到")

except subprocess.CalledProcessError as e:
    print("Docker命令执行失败:", e)
except Exception as e:
    print("发生其他错误:", e)





time_pattern = r'pdu会话完成时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'

try:
    docker_command = 'docker exec -it oai-smf cat timelogs.txt'
    result = subprocess.run(docker_command, shell = True, check = True, stdout = subprocess.PIPE, text=True)
    match = re.search(time_pattern, result.stdout)
    if match: 
        PDU_success_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
        print("PDU success time:", PDU_success_time)
    else: 
        oai_time = None
except subprocess.CalledProcessError as e:
    print("failed to get time from docker:", e)
    oai_time = None


# dir_path = os.path.join(base_path_p3Chain)
# print(dir_path)
# log_file_path = os.path.join(dir_path, 'timelogs.txt')
    
# # 检查文件是否存在
# if os.path.exists(log_file_path):
#     with open(log_file_path, 'r') as file:
#         # for line in file:
#         first_line = file.readline()
#         # match = re.search(time_pattern, line)
#         match = re.search(time_pattern_p3Chain, first_line)
#         if match:
#                 # 提取时间并转换为 datetime 对象
#                 # print("p3Chain matching string:", match.group(1))
#                 blockchain_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print("blockchain success time:", blockchain_time)



# # 找出最早的时间
# if times:
#     earliest_time = min(times)
#     print(f"The earliest time is: {earliest_time}")
#     with open(output_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([PDU_message_received_time, U-DID_send_BC_time, PDU_success_time, blockchain_time])
# else:
#     print("No valid times found in the files.")

# 找出最早的时间
# if times:
#     earliest_time = min(times)
#     print(f"The earliest time is: {earliest_time}")
with open(output_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([PDU_message_received_time, PDU_success_time])
# else:
#     print("No valid times found in the files.")

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

# # 正则表达式用于匹配时间
# time_pattern_ue1 = r'UE启动的时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
# time_pattern_ue2 = r'UE发送IMSI时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
# time_pattern_ue3 = r'接受did时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
# time_pattern_ue4 = r'UE发送PDU会话请求时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'



time_pattern_p3Chain = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'


# 存储时间的列表
times = []

# 创建timelogsaggregate.csv的文件
output_file = "timelogsaggreaget_ran_withDID.csv"

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['activat time','send IMSI time','received U-DID time','send PDU time'])


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

dir_path = os.path.join(base_path_ue, '01-modified-openairinterface5g','cmake_targets','ran_build','build')
print(dir_path)
log_file_path = os.path.join(dir_path, 'timelogs.txt')

# # 检查文件是否存在
# if os.path.exists(log_file_path):
#     with open(log_file_path, 'r') as file:
#         # for line in file:
#             first_line = file.readline()
#             # match = re.search(time_pattern, line)
#             match1 = re.search(time_pattern_ue1, first_line)
#             if match1:
#                 # 提取时间并转换为 datetime 对象
#                 activate_time = datetime.strptime(match1.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print(activate_time)
#             match2 = re.search(time_pattern_ue2, first_line)
#             if match2:
#                 # 提取时间并转换为 datetime 对象
#                 send_IMSI_time = datetime.strptime(match2.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print(send_IMSI_time)
#             match3 = re.search(time_pattern_ue3, first_line)
#             if match3:
#                 # 提取时间并转换为 datetime 对象
#                 received_UDID_time = datetime.strptime(match3.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print(received_UDID_time)
#             match4 = re.search(time_pattern_ue4, first_line)
#             if match4:
#                 # 提取时间并转换为 datetime 对象
#                 send_PDU_time = datetime.strptime(match4.group(1), '%Y-%m-%d %H:%M:%S.%f')
#                 print(send_PDU_time)



# 正则表达式合并为单个模式（更高效）
time_pattern = re.compile(
    r'(UE启动的时间|UE发送IMSI时间|接受did时间|UE发送PDU会话请求时间): '
    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
)

# 初始化变量（避免未定义风险）
activate_time = send_IMSI_time = received_UDID_time = send_PDU_time = None

if os.path.exists(log_file_path):
    with open(log_file_path, 'r') as file:
        for line in file:
            match = time_pattern.search(line)
            if match:
                event_type, time_str = match.groups()
                time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
                
                # 根据事件类型赋值
                if event_type == 'UE启动的时间':
                    activate_time = time_obj
                elif event_type == 'UE发送IMSI时间':
                    send_IMSI_time = time_obj
                elif event_type == '接受did时间':
                    received_UDID_time = time_obj
                elif event_type == 'UE发送PDU会话请求时间':
                    send_PDU_time = time_obj

# 打印结果（可选）
print("UE激活时间:", activate_time)
print("发送IMSI时间:", send_IMSI_time)
print("接收DID时间:", received_UDID_time)
print("发送PDU时间:", send_PDU_time)











with open(output_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([activate_time, send_IMSI_time, received_UDID_time, send_PDU_time])


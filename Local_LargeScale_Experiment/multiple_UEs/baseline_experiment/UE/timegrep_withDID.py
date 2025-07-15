import os
import re
from datetime import datetime
import csv
import subprocess

# 基本路径设置
base_path_ue = '/home/dmt/multiple_UEs/baseline_experiment/UE'
base_path_p3Chain = '/home/dmt/Lee-P3chainforOai-main/dper/client/auto/dper_dper4'

#当前ue的数量
count = 5

# 正则表达式用于匹配时间
time_pattern_ue = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
time_pattern_p3Chain = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'


# 存储时间的列表
times = []

# 创建timelogsaggregate.csv的文件
output_file = "1timelogsaggreaget.csv"

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['activat time','blockchain success time'])




# dir_path = os.path.join(base_path_ue, 'compiled_binaries_withDID')
print(base_path_ue)
log_file_path = os.path.join(base_path_ue, 'timelogs.txt')

# 检查文件是否存在
if os.path.exists(log_file_path):
    with open(log_file_path, 'r') as file:
        # for line in file:
            first_line = file.readline()
            # match = re.search(time_pattern, line)
            match = re.search(time_pattern_ue, first_line)
            if match:
                # 提取时间并转换为 datetime 对象
                time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
                print(time)
                times.append(time)




dir_path = os.path.join(base_path_p3Chain)
print(dir_path)
log_file_path = os.path.join(dir_path, 'timelogs.txt')
    
# 检查文件是否存在
if os.path.exists(log_file_path):
    with open(log_file_path, 'r') as file:
        # for line in file:
        first_line = file.readline()
        # match = re.search(time_pattern, line)
        match = re.search(time_pattern_p3Chain, first_line)
        if match:
                # 提取时间并转换为 datetime 对象
                # print("p3Chain matching string:", match.group(1))
                blockchain_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
                print("blockchain success time:", blockchain_time)



# 找出最早的时间
if times:
    earliest_time = min(times)
    print(f"The earliest time is: {earliest_time}")
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([earliest_time, blockchain_time])
else:
    print("No valid times found in the files.")

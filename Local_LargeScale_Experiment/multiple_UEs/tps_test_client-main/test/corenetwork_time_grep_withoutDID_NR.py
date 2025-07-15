# corenetwork_time_grep_withDID.py
# 修复版：合并同数量 UE 的所有数据后计算平均值

import os
import pandas as pd
import csv

# DIR_PATTERN = re.compile(r'^(\d+)ue_withDID_(\d+)$')  # 匹配形如 10ue_withDID_1

def safe_avg(data_list):
    return sum(data_list)/len(data_list) if len(data_list) > 0 else 0

def aggregate_time_data():
    """聚合逻辑：按 UE 数量合并所有数据后计算平均"""
    base_path = os.path.expanduser('~/multiple_UEs/experimentdata/withoutDID/NR_experiment')
    # subdirs = [d for d in os.listdir(base_path) 
    #            if os.path.isdir(os.path.join(base_path, d)) and d.endswith('ue_withDID')]
    subdirs = os.listdir(base_path) 
    
    # 按 UE 数量分组存储原始时间差数据
    data_groups = {}  # 结构: { count: { 'pdu': [时间列表], 'blockchain': [时间列表] } }


    global_UL_PDU_time = []

    
    for subdir in subdirs:
        subdir_path = os.path.join(base_path, subdir)
        file_path2 = os.path.join(subdir_path, 'timelogsaggreaget_core_withoutDID.csv')
        file_path1 = os.path.join(subdir_path, 'timelogsaggreaget_ran_withoutDID.csv')
        
        if not os.path.exists(file_path1):
            print(f"跳过缺失文件: {file_path1}")
            continue
        
        try:
            df1 = pd.read_csv(file_path1)
            df2 = pd.read_csv(file_path2)
            count = int(subdir)  # 提取 UE 数量
            
            # 转换时间列为 datetime 并计算所有行的时间差

            # blockchain_diff = (pd.to_datetime(df['blockchain success time']) - ue_activate).dt.total_seconds()
            send_PDU_time = pd.to_datetime(df1['send PDU time'])
            UL_PDU_time = (pd.to_datetime(df2['PDU message received time']) - send_PDU_time).dt.total_seconds()

            
            # # 将数据存入对应分组
            # if count not in data_groups:
            #     data_groups[count] = {
            #         'UDID_create': [],
            #         'UL_PDU_time': [],
            #         'parse_UDID_time':[],
            #         'blockchain_success_time':[]
            #     }
            # data_groups[count]['UDID_create'].extend(UDID_create_diff.tolist())
            # data_groups[count]['UL_PDU_time'].extend(UL_PDU_time.tolist())
            # data_groups[count]['parse_UDID_time'].extend(parse_UDID_time.tolist())
            # data_groups[count]['blockchain_success_time'].extend(blockchain_success_time.tolist())


            global_UL_PDU_time.extend(UL_PDU_time.dropna().tolist())



            
        except Exception as e:
            print(f"处理 {file_path1} 出错: {str(e)}")
            print(f"处理 {file_path2} 出错: {str(e)}")
            continue
    
    # 计算每个 UE 数量的全局平均值

    UL_PDU_time_avg = safe_avg(global_UL_PDU_time)

    # }   
    aggregated_data = []
    aggregated_data=[
        [UL_PDU_time_avg]
        ]
    
    
    # 保存结果
    output_file = "scenario1_timecost_time_withoutDID_NR.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ 'UL_PDU_time_avg'])
        writer.writerows(aggregated_data)
    

    # 保存原始数据
    raw_output_file = "scenario1_timecost_time_withoutDID_NR_raw.csv"
    with open(raw_output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['UL_PDU_time'])
        for time in global_UL_PDU_time:
            writer.writerow([time])

    
    print(f"聚合数据已保存至 {output_file} 和 {raw_output_file}")
    return output_file

if __name__ == "__main__":
    aggregate_time_data()

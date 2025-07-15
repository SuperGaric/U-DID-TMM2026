

import os
import pandas as pd
import re
from collections import defaultdict

# ====================== 配置部分 ======================
BASE_DIR = os.path.expanduser('~/multiple_UEs/experimentdata/withoutDID/large_experiment')
OUTPUT_FILE = "core-network_cpu_mem_withoutDID_large.csv"
COMPONENTS = ['oai-amf', 'oai-ausf', 'oai-ext-dn', 'oai-nrf', 
             'oai-smf', 'oai-udm', 'oai-udr', 'oai-upf', 'mysql']
DIR_PATTERN = re.compile(r'^(\d+)ue_withoutDID_(\d+)$')  # 匹配形如 10ue_withDID_1
# ======================================================

def process_single_experiment(exp_dir):
    """处理单个实验目录（如 10ue_withDID_1）"""
    total_cpu, total_mem, valid_components = 0.0, 0.0, 0
    
    for comp in COMPONENTS:
        csv_path = os.path.join(exp_dir, f"{comp}_usage_log.csv")
        if not os.path.exists(csv_path):
            continue
            
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                continue

            # 特殊处理 p3Chain
            if comp == 'p3Chain':
                if len(df) >= 6:
                    cpu = df.iloc[5]['Average CPU%']
                    mem = df.iloc[5]['Average MEM(MB)']
                else:
                    print(f"[WARN] {csv_path} 行数不足 ({len(df)} < 6)")
                    continue
            else:
                cpu = df['Average CPU%'].mean()
                mem = df['Average MEM(MB)'].mean()

            total_cpu += cpu
            total_mem += mem
            valid_components += 1
            
        except Exception as e:
            print(f"[ERROR] 处理文件 {csv_path} 失败: {str(e)}")
    
    return total_cpu, total_mem

def main():
    # 数据结构: {ue_count: {'cpu': [values], 'mem': [values]}}
    aggregated_data = defaultdict(lambda: {'cpu': [], 'mem': []})
    
    # 遍历所有实验目录
    for dir_name in os.listdir(BASE_DIR):
        dir_path = os.path.join(BASE_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue
        
        # 匹配目录名
        match = DIR_PATTERN.match(dir_name)
        if not match:
            print(f"[SKIP] 忽略无效目录: {dir_name}")
            continue
        
        ue_count = int(match.group(1))
        exp_id = int(match.group(2))
        
        # 处理单个实验
        cpu, mem = process_single_experiment(dir_path)
        aggregated_data[ue_count]['cpu'].append(cpu)
        aggregated_data[ue_count]['mem'].append(mem)
        print(f"[OK] 已处理 {dir_name}: CPU={cpu:.2f}%, MEM={mem:.2f}MB")

    # 生成最终结果
    results = []
    for ue in sorted(aggregated_data.keys()):
        cpu_list = aggregated_data[ue]['cpu']
        mem_list = aggregated_data[ue]['mem']
        
        avg_cpu = sum(cpu_list) / len(cpu_list)
        avg_mem = sum(mem_list) / len(mem_list)
        
        results.append({
            'UE count': ue,
            'Overall CPU%': round(avg_cpu, 2),
            'Overall MEM(MB)': round(avg_mem, 2)
        })
    
    # 保存结果
    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
    print(f"\n[SUCCESS] 结果已保存到 {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()

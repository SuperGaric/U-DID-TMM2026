import os
import pandas as pd
from collections import defaultdict

# ====================== 配置部分 ======================
BASE_DIR = os.path.expanduser('~/multiple_UEs/dmt_experiment_no')
OUTPUT_FILE = "core-network_cpu_mem_dmt.csv"
COMPONENTS = ['oai-amf', 'oai-ausf', 'oai-ext-dn', 'oai-nrf',
              'oai-smf', 'oai-udm', 'oai-udr', 'oai-upf', 'mysql', 'p3Chain']
# ======================================================

def process_single_experiment(exp_dir):
    """处理单个实验目录"""
    total_cpu, total_mem, valid_components = 0.0, 0.0, 0

    for comp in COMPONENTS:
        csv_path = os.path.join(exp_dir, f"{comp}_usage_log.csv")
        if not os.path.exists(csv_path):
            continue

        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                continue

            if comp == 'p3Chain':
                if len(df) >= 4:
                    row = df.iloc[3]

                    # 字段容错映射
                    cpu_raw = row.get('Average CPU%', 0)
                    mem_raw = row.get('Average MEM(MB)', row.get('Average MEM%', 0))  # 容错处理

                    # 转换为数值类型，忽略非数字内容
                    cpu = pd.to_numeric(cpu_raw, errors='coerce')
                    mem = pd.to_numeric(mem_raw, errors='coerce')

                    # 填默认值
                    if pd.isna(cpu): cpu = 0.0
                    if pd.isna(mem): 
                        print(f"[WARN] {csv_path} 内存字段为空或拼写错误")
                        mem = 0.0
                else:
                    print(f"[WARN] {csv_path} 行数不足 ({len(df)} < 4)")
                    continue
            else:
                cpu = pd.to_numeric(df['Average CPU%'], errors='coerce').mean()
                mem = pd.to_numeric(df['Average MEM(MB)'], errors='coerce').mean()

            total_cpu += cpu
            total_mem += mem
            valid_components += 1

        except Exception as e:
            print(f"[ERROR] 处理文件 {csv_path} 失败: {str(e)}")

    return total_cpu, total_mem


def main():
    aggregated_data = {'cpu': [], 'mem': [], 'exp': []}

    for dir_name in sorted(os.listdir(BASE_DIR)):
        dir_path = os.path.join(BASE_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue
        if not dir_name.isdigit():
            print(f"[SKIP] 忽略无效目录: {dir_name}")
            continue

        cpu, mem = process_single_experiment(dir_path)
        aggregated_data['exp'].append(dir_name)
        aggregated_data['cpu'].append(cpu)
        aggregated_data['mem'].append(mem)
        print(f"[OK] 已处理 {dir_name}: CPU={cpu:.2f}%, MEM={mem:.2f}MB")

    # 输出为 DataFrame
    df = pd.DataFrame({
        'Experiment ID': aggregated_data['exp'],
        'Overall CPU%': aggregated_data['cpu'],
        'Overall MEM(MB)': aggregated_data['mem']
    })

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[SUCCESS] 结果已保存到 {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()

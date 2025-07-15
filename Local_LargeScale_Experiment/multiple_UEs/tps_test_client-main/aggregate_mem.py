import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# ----------- 全局配置 -----------
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 16,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'pdf.fonttype': 42,
    'axes.spines.top': False,
    'axes.spines.right': False
})

# 设置系统总内存（MB），请根据实际机器调整
SYSTEM_TOTAL_MEM_MB = 13821  # 16 GB

# ----------- 工具函数 -----------

def calc_ci(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, ci

def remove_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return series[(series >= q1 - 1.5 * iqr) & (series <= q3 + 1.5 * iqr)]

def read_mem_value(path, column='Average MEM(MB)'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    if column not in df.columns:
        raise ValueError(f"Missing '{column}' column in {path}")
    return df[column].iloc[0]

# ----------- 数据加载 -----------

def load_ue_only_memory_usage(base_dir, subdirs):
    ue_client, ue_server = [], []
    for subdir in subdirs:
        path = lambda name: os.path.join(base_dir, subdir, name)
        ue_c = read_mem_value(path("nr-uesoftmodem-208950000000031_usage_average_log.csv"))
        ue_s = read_mem_value(path("nr-uesoftmodem-208950000000032_usage_average_log.csv"))
        ue_client.append(ue_c)
        ue_server.append(ue_s)
    return pd.Series(ue_client), pd.Series(ue_server)

def load_combined_memory_usage(base_dir, subdirs):
    combo_client, combo_server = [], []
    for subdir in subdirs:
        path = lambda name: os.path.join(base_dir, subdir, name)
        ue_c = read_mem_value(path("nr-uesoftmodem-208950000000031_usage_average_log.csv"))
        ue_s = read_mem_value(path("nr-uesoftmodem-208950000000032_usage_average_log.csv"))
        go_c = read_mem_value(path("client_go_dmt_usage_averge_log.csv"))
        go_s = read_mem_value(path("server_go_dmt_usage_averge_log.csv"))
        combo_client.append(ue_c + go_c)
        combo_server.append(ue_s + go_s)
    return pd.Series(combo_client), pd.Series(combo_server)

def load_core_memory_usage(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    df = pd.read_csv(csv_path)
    if "Overall MEM(MB)" not in df.columns:
        raise ValueError(f"'Overall MEM(MB)' column not found in {csv_path}")
    return pd.Series(df["Overall MEM(MB)"].values)

# ----------- 绘图函数 -----------

def plot_memory_comparison_grouped(mem_client, mem_server, mem_combo_client, mem_combo_server, core_no, core_combo):
    mem_client = remove_outliers(mem_client)
    mem_server = remove_outliers(mem_server)
    mem_combo_client = remove_outliers(mem_combo_client)
    mem_combo_server = remove_outliers(mem_combo_server)
    core_no = remove_outliers(core_no)
    core_combo = remove_outliers(core_combo)

    # 转换为百分比
    def to_percent(series): return series / SYSTEM_TOTAL_MEM_MB * 100

    means = [
        np.mean(to_percent(mem_client)), np.mean(to_percent(mem_combo_client)),
        np.mean(to_percent(mem_server)), np.mean(to_percent(mem_combo_server)),
        np.mean(to_percent(core_no)), np.mean(to_percent(core_combo))
    ]
    cis = [
        calc_ci(to_percent(mem_client))[1], calc_ci(to_percent(mem_combo_client))[1],
        calc_ci(to_percent(mem_server))[1], calc_ci(to_percent(mem_combo_server))[1],
        calc_ci(to_percent(core_no))[1], calc_ci(to_percent(core_combo))[1]
    ]

    labels = ['UE1', 'UE2', 'Core']
    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(x - width/2, [means[0], means[2], means[4]], width,
           yerr=[cis[0], cis[2], cis[4]], label='UE',
           color='#f0f0f0', capsize=6, edgecolor='black', hatch=None)

    ax.bar(x + width/2, [means[1], means[3], means[5]], width,
           yerr=[cis[1], cis[3], cis[5]], label='UE with U-DID',
           color='#f0f0f0', capsize=6, edgecolor='black', hatch='///')

    ax.set_ylabel('Memory Utilization (%)')
    ax.set_title('MEM Utilization of U-DID based Service')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('MEM Utilization of U-DID based Service.pdf', bbox_inches='tight')
    plt.show()
    plt.close()

# ----------- 主程序入口 -----------

if __name__ == "__main__":
    subdirs = ['1', '2', '3', '4', '5']
    base_dir_ue = os.path.expanduser("~/multiple_UEs/dmt_experiment_no")
    base_dir_combo = os.path.expanduser("~/multiple_UEs/dmt_experiment")
    core_path_no = os.path.join(os.getcwd(), "core-network_cpu_mem_dmt_no.csv")
    core_path_combo = os.path.join(os.getcwd(), "core-network_cpu_mem_dmt.csv")

    mem_c, mem_s = load_ue_only_memory_usage(base_dir_ue, subdirs)
    mem_combo_c, mem_combo_s = load_combined_memory_usage(base_dir_combo, subdirs)
    core_no = load_core_memory_usage(core_path_no)
    core_combo = load_core_memory_usage(core_path_combo)

    plot_memory_comparison_grouped(mem_c, mem_s, mem_combo_c, mem_combo_s, core_no, core_combo)

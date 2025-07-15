import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# 图像样式设置
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

def calc_ci(data, confidence=0.95):
    """计算均值和置信区间"""
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, ci

def remove_outliers(series):
    """IQR法去除异常值"""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return series[(series >= q1 - 1.5 * iqr) & (series <= q3 + 1.5 * iqr)]

def read_cpu_value(path, column='Average CPU%'):
    """读取CSV中CPU列的值"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    if column not in df.columns:
        raise ValueError(f"Missing '{column}' column in {path}")
    return df[column].iloc[0]

def load_ue_only_cpu_usage(base_dir, subdirs):
    """从dmt_experiment_no目录读取UE-only数据"""
    ue_client, ue_server = [], []
    for subdir in subdirs:
        path = lambda name: os.path.join(base_dir, subdir, name)
        ue_c = read_cpu_value(path("nr-uesoftmodem-208950000000031_usage_average_log.csv"))
        ue_s = read_cpu_value(path("nr-uesoftmodem-208950000000032_usage_average_log.csv"))
        ue_client.append(ue_c)
        ue_server.append(ue_s)
    return pd.Series(ue_client), pd.Series(ue_server)

def load_combined_cpu_usage(base_dir, subdirs):
    """从dmt_experiment目录读取UE + GO数据"""
    combo_client, combo_server = [], []
    for subdir in subdirs:
        path = lambda name: os.path.join(base_dir, subdir, name)
        ue_c = read_cpu_value(path("nr-uesoftmodem-208950000000031_usage_average_log.csv"))
        ue_s = read_cpu_value(path("nr-uesoftmodem-208950000000032_usage_average_log.csv"))
        go_c = read_cpu_value(path("client_go_dmt_usage_averge_log.csv"))
        go_s = read_cpu_value(path("server_go_dmt_usage_averge_log.csv"))
        combo_client.append(ue_c + go_c)
        combo_server.append(ue_s + go_s)
    return pd.Series(combo_client), pd.Series(combo_server)

def load_core_cpu_usage(csv_path):
    """读取核心网络的 CPU 利用率数据"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    df = pd.read_csv(csv_path)
    if "Overall CPU%" not in df.columns:
        raise ValueError(f"'Overall CPU%' column not found in {csv_path}")
    return pd.Series(df["Overall CPU%"].values)

def plot_cpu_comparison_grouped(ue_client, ue_server, combo_client, combo_server, core_no, core_combo):
    """绘制分组柱状图（包含 Core Network）"""
    ue_client = remove_outliers(ue_client)
    ue_server = remove_outliers(ue_server)
    combo_client = remove_outliers(combo_client)
    combo_server = remove_outliers(combo_server)
    core_no = remove_outliers(core_no)
    core_combo = remove_outliers(core_combo)

    means = [
        np.mean(ue_client), np.mean(combo_client),
        np.mean(ue_server), np.mean(combo_server),
        np.mean(core_no), np.mean(core_combo)
    ]
    cis = [
        calc_ci(ue_client)[1], calc_ci(combo_client)[1],
        calc_ci(ue_server)[1], calc_ci(combo_server)[1],
        calc_ci(core_no)[1], calc_ci(core_combo)[1]
    ]

    labels = ['UE1', 'UE2', 'Core']
    x = np.arange(len(labels))  # [0, 1, 2]
    width = 0.2

    fig, ax = plt.subplots(figsize=(9, 5))
    bar1 = ax.bar(x - width/2, [means[0], means[2], means[4]], width,
                  yerr=[cis[0], cis[2], cis[4]], label='UE',
                  color='#f0f0f0', capsize=6, edgecolor='black')
    bar2 = ax.bar(x + width/2, [means[1], means[3], means[5]], width,
                  yerr=[cis[1], cis[3], cis[5]], label='UE with U-DID',
                  color='#f0f0f0', capsize=6, edgecolor='black', hatch='///')

    ax.set_ylabel('CPU Utilization (%)')
    ax.set_title('CPU Utilization of U-DID based Service')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('CPU Utilization of U-DID based Service.pdf', bbox_inches='tight')
    plt.show()
    plt.close()

if __name__ == "__main__":
    subdirs = ['1', '2', '3', '4', '5']
    base_dir_ue = os.path.expanduser("~/multiple_UEs/dmt_experiment_no")
    base_dir_combo = os.path.expanduser("~/multiple_UEs/dmt_experiment")
    core_path_no = os.path.join(os.getcwd(), "core-network_cpu_mem_dmt_no.csv")
    core_path_combo = os.path.join(os.getcwd(), "core-network_cpu_mem_dmt.csv")

    ue_c, ue_s = load_ue_only_cpu_usage(base_dir_ue, subdirs)
    combo_c, combo_s = load_combined_cpu_usage(base_dir_combo, subdirs)
    core_no = load_core_cpu_usage(core_path_no)
    core_combo = load_core_cpu_usage(core_path_combo)

    plot_cpu_comparison_grouped(ue_c, ue_s, combo_c, combo_s, core_no, core_combo)

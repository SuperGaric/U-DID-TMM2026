import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False   # 正确显示负号

# ================= 公共配置 =================
plt.rcParams['pdf.fonttype'] = 42  # 确保PDF输出可编辑文本
MILLISECOND_THRESHOLD = 1 # 超过该阈值自动转换为毫秒显示
plt.rcParams.update({
    'font.family': 'serif',        # 主字体
    'font.size': 18,               # 基础字号
    'axes.titlesize': 18,          # 图表标题
    'axes.labelsize': 18,          # 坐标轴标签
    'xtick.labelsize': 16,         # X轴刻度
    'ytick.labelsize': 16,         # Y轴刻度
    'legend.fontsize': 18,         # 图例文字
    'pdf.fonttype': 42,             # 确保矢量字体
    'axes.spines.top': False,      # 隐藏顶部边框
    'axes.spines.right': False     # 隐藏右侧边框
})

# ================= 核心函数先定义 =================
def calc_ci(data, confidence=0.95):
    """计算均值和置信区间"""
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = std_err * stats.t.ppf((1 + confidence)/2, n-1)
    return mean, ci

# ================= 数据预处理 =================
def load_data():
    # 读取带DID数据
    with_did_df = pd.read_csv("scenario1_timecost_time_withDID_NR_raw.csv")
    with_did_df['parse_UDID_time'] = with_did_df['parse_UDID_time'].apply(
        lambda x: float(x.split('e')[0]) * 10**int(x.split('e')[1]) if isinstance(x, str) else x)
    
    q1 = with_did_df['blockchain_success_time'].quantile(0.25)
    q3 = with_did_df['blockchain_success_time'].quantile(0.75)
    iqr = q3 - q1
    with_did_df = with_did_df[
        (with_did_df['blockchain_success_time'] >= q1 - 1.5*iqr) &
        (with_did_df['blockchain_success_time'] <= q3 + 1.5*iqr)
    ]

    # 读取不带DID数据
    without_did_ul = pd.read_csv("scenario1_timecost_time_withoutDID_NR_raw.csv", 
                               usecols=['UL_PDU_time'])['UL_PDU_time'].tolist()
    return with_did_df, without_did_ul

# ================= 图表1：细粒度时间分析 =================
def plot_fine_grained_times():
    # 数据筛选
    selected_cols = ['UDID_create', 'parse_UDID_time', 'blockchain_success_time']
    categories = ["U-DID Create", "U-DID Parse", "BC Function Consensus"]
  
    # 计算统计量
    means, cis = [], []
    for col in selected_cols:
        m, ci = calc_ci(with_did_df[col])
        means.append(m)
        cis.append(ci)

    # 单位自动转换
    ylabel, scale = ('ms', 1000) if max(means) < MILLISECOND_THRESHOLD else ('seconds', 1)
    scaled_means = [m * scale for m in means]
    scaled_cis = [ci * scale for ci in cis]

    # 可视化配置
    fig, ax = plt.subplots(figsize=(8, 4.94))  # 16:10比例
    bars = ax.bar(categories, scaled_means, width=0.3, 
                edgecolor='black', linewidth=1, 
                # facecolor='white')
                facecolor = '#f0f0f0')
  
    # 误差条配置
    ax.errorbar(categories, scaled_means, yerr=scaled_cis, fmt='none',
               ecolor='black', elinewidth=1.5, capsize=6, capthick=1.5)

    # 标签优化
    ax.set_ylabel(f'Time Cost ({ylabel})')
    ax.set_title('U-DID Process Time')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
  
    # 保存PDF
    plt.tight_layout()
    plt.savefig('UDID_create_parse_consensus_time.pdf', bbox_inches='tight')
    plt.show()
    plt.close()

# ================= 图表2：上下行PDU对比 ================= 
def plot_pdu_comparison():
    # 数据准备
    did_ul = with_did_df['UL_PDU_time'].tolist()
    categories = ["Uplink PDU Message\n(Carrying U-DID)", "Uplink PDU Message\n(Original)"]
  
    # 计算统计量
    m1, ci1 = calc_ci(did_ul)
    m2, ci2 = calc_ci(without_did_ul)
  
    # 单位转换
    ylabel, scale = ('ms', 1000) if max(m1, m2) < MILLISECOND_THRESHOLD else ('seconds', 1)
    scaled_means = [m * scale for m in [m1, m2]]
    scaled_cis = [ci * scale for ci in [ci1, ci2]]

    # 可视化配置
    fig, ax = plt.subplots(figsize=(8, 4.94))  # 16:10比例
    bars = ax.bar(categories, scaled_means, width=0.2,
                edgecolor='black', linewidth=1, 
                color=['#f0f0f0', '#d3d3d3'], hatch=['', '//'])
  
    # 误差条配置
    ax.errorbar(categories, scaled_means, yerr=scaled_cis, fmt='none',
               ecolor='black', elinewidth=1.5, capsize=8, capthick=1.5, alpha=0.7)
               
    ax.yaxis.grid(True, linestyle=':', alpha=0.5)
        # 旋转X轴标签
    # plt.xticks(rotation=30, ha='right')

    # 标签优化
    ax.set_ylabel(f'Time Cost ({ylabel})')
    ax.set_title('Uplink PDU Message Transmission Time')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
  
    # 保存PDF
    plt.tight_layout()
    plt.savefig('UDID_uplink_pdu_time_comparison.pdf', bbox_inches='tight')
    plt.show()
    plt.close()
if __name__ == "__main__":
    with_did_df, without_did_ul = load_data()
    plot_fine_grained_times()
    plot_pdu_comparison()
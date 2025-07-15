import os
import subprocess
import time
import threading
import csv

def corenetwork_monitor_resource_usage(process_name):
    # 确定输出文件的文件名
    output_file = f"{process_name}_usage_log.csv"
    
    # 检查文件是否存在，若不存在则创建并写入标题行
    if not os.path.exists(output_file):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PID', 'CPU%', 'MEM%', 'CMD'])

    while True:
        try:
            # 使用ps命令获取进程信息
            result = subprocess.run(['ps', '-C', process_name, '-o', 'pid,%cpu,%mem,cmd'], 
                                    capture_output=True, text=True)
            # 处理ps命令的输出
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = output.split('\n')
                if len(lines) > 1:
                    # 打开CSV文件并追加数据
                    with open(output_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        for info in lines[1:]:  # 跳过标题行
                            writer.writerow(info.split(None, 3))
                else:
                    print(f"No process found with name {process_name}")
            else:
                print("Error executing ps command")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(0.5)



def monitor_resource_usage(process_name, log_file):
    """
    Monitor and log the cpu and memory usage of a specific process in a non-blocking way.
    """
    try:
        with open(log_file, 'w') as file:
            csv_writer = csv.writer(file)
            # CSV header
            csv_writer.writerow(['PID', 'CPU(%)', 'MEM(%)', 'COMMAND'])

            while True:
                try:
                    # using 'pgrep' to find process IDs
                    pids = subprocess.check_output(f"pgrep -f  {process_name}", shell=True).decode().strip().split()
                except subprocess.CalledProcessError:
                    pids = []

                if pids:  # Check if there are any process IDs
                    for pid in pids:
                        try:
                            process_info = subprocess.check_output(f"ps -p {pid} -o pid,%cpu,%mem,cmd", shell=True).decode().strip().split('\n')[1:]  # Skip header
                            for info in process_info:
                                parts = info.split()
                                if parts:
                                    csv_writer.writerow(parts)  # Write each line of info
                        except subprocess.CalledProcessError:
                            # Handle the case where the process might have ended between `pgrep` and `ps`
                            pass
                else:
                    csv_writer.writerow(["未找到匹配的进程。", "", "", ""])
                time.sleep(0.5)  # Adjust the monitoring frequency as needed
    except Exception as e:
        with open(log_file, 'a') as file:
            file.write(f"发生错误: {str(e)}\n")

def monitor_resource_usage_ports(ports, log_file):
    """
    Monitor and log the cpu and memory usage of a specific process in a non-blocking way.
    """
    try:
        with open(log_file, 'w') as file:
            csv_writer = csv.writer(file)
            # CSV header
            csv_writer.writerow(['PID', 'CPU(%)', 'MEM(%)', 'COMMAND'])                
            while True:
                for port in ports:
                    try:
                        netstat_output = subprocess.check_output(f"netstat -tuln | grep :{port}", shell=True).decode().strip()
                        if netstat_output:
                            parts = netstat_output.split()
                            print("netstat_output\n")
                            if parts:
                                print("执行到lsof\n")
                                pid_info = subprocess.check_output(f"lsof -i:{port} -t", shell=True).decode().strip()
                                if pid_info:
                                    print("执行到pid_info.spli\n")
                                    pids = pid_info.split()
                                    for pid in pids:
                                        print("执行到ps这里了\n")
                                        process_info = subprocess.check_output(f"ps -p {pid} -o pid,%cpu,%mem,cmd",shell=True).decode().strip().split('\n')[1:]
                                        for info in process_info:
                                            parts = info.split()
                                            if parts:
                                                print("开始写了")
                                                csv_writer.writerow(parts)
                    except subprocess.CalledProcessError:
                        file.write(f"not find match port: {port}\n")
                time.sleep(0.5)  # Adjust the monitoring frequency as needed
    except Exception as e:
        with open(log_file, 'a') as file:
            file.write(f"发生错误: {str(e)}\n")



def run_softmodem(directory, imsi):
    # 构建命令行参数
    command = ' '.join([
        f'./nr-uesoftmodem-{imsi}', '-r', '106', '--numerology', '1',
        '--band', '78', '-C', '3619200000', '--sa', f'--uicc0.imsi', str(imsi), '--rfsim'
    ])

    # 执行命令
    terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True, check=True)
        print(f"Command launched in a new terminal for directory {directory} with IMSI {imsi}")
        # start monitoring in a separate thread
        monitor_process_name = f"nr-uesoftmodem.*{imsi}"
        # monitor_ports = []
        log_file = f"nr-uesoftmodem_{imsi}_usage.csv"
        monitoring_thread = threading.Thread(target=monitor_resource_usage, args=(monitor_process_name, log_file))
        monitoring_thread.start()
    except subprocess.CalledProcessError as e:
        print(f"Failed to start terminal for directory {directory}")


def run_gnb(directory):
    command = ' '.join([
        './nr-softmodem', '-O', '../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf', '--gNBs.[0].min_rxtxtime', '6' ,'--rfsim', '--sa'
    ])
    #执行命令
    terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True, check=True)
        print(f"Command launched in a new terminal for directory {directory} with gNB")
        # start monitoring in a separate thread
        monitor_process_name = f"nr-softmodem"
        # monitor_ports = []
        log_file = f"nr-softmodem_gnb_usage.csv"
        monitoring_thread = threading.Thread(target=monitor_resource_usage, args=(monitor_process_name, log_file))
        monitoring_thread.start()
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start terminal for directory {directory}")


def main():
    count = 5
    base_directory = os.path.expanduser('~/multiple_UEs')  # 确保这是正确的路径
    initial_imsi = 208950000000031
    projects = [f"openairinterface5g_copy_{i}" for i in range(1, count + 1)]

   
    monitor_ports = [8080 + i for i in range(count)]
    log_file = os.path.join(base_directory,"didserver_usage_log.csv")
    monitoring_thread = threading.Thread(target=monitor_resource_usage_ports,args=(monitor_ports,log_file))
    monitoring_thread.start()

    monitor_process_names=["oai_amf"]
    # log_file = os.path.join(base_directory,"amf_usage_log.csv")
    monitoring_thread = threading.Thread(target=corenetwork_monitor_resource_usage, args=(monitor_process_names))
    monitoring_thread.start()

    monitor_process_names=["oai_smf"]
    # log_file = os.path.join(base_directory,"amf_usage_log.csv")
    monitoring_thread = threading.Thread(target=corenetwork_monitor_resource_usage, args=(monitor_process_names))
    monitoring_thread.start()

    # monitor_process_name =["p3Chain"]
    # log_file = os.path.join(base_directory,"p3Chain_usage_log.csv")
    # monitoring_thread = threading.Thread(target=monitor_resource_usage,args=(monitor_process_name,log_file))
    # monitoring_thread.start()

    monitor_process_names=["p3Chain"]
    # log_file = os.path.join(base_directory,"amf_usage_log.csv")
    monitoring_thread = threading.Thread(target=corenetwork_monitor_resource_usage, args=(monitor_process_names))
    monitoring_thread.start()

    for i, project in enumerate(projects):
        project_path = os.path.join(base_directory, project, 'cmake_targets', 'ran_build', 'build')
        if i == 0 :
            run_gnb(project_path)
        run_softmodem(project_path, initial_imsi + i)

if __name__ == '__main__':
    main()


import subprocess
import time
import csv
import psutil

def find_main_process(process_name):
  
    main_pid = None
    candidate_pids = []
    
    # 遍历所有进程，查找命令行中包含指定名称的进程
    for proc in psutil.process_iter(['pid', 'ppid', 'cmdline']):
        try:
            if any(process_name in cmd for cmd in proc.info['cmdline']):
                candidate_pids.append((proc.info['pid'], proc.info['ppid']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(f"Candidate PIDs: {candidate_pids}")

    # 找到父进程不是目标进程的进程
    for pid, ppid in candidate_pids:
        try:
            parent = psutil.Process(ppid)
            if not any(process_name in cmd for cmd in parent.cmdline()):
                main_pid = pid
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            main_pid = pid
            break

    return main_pid

def monitor_process_with_pidstat(pid, process_name):
    output_file = f"{process_name}_usage_log.csv"

    # 打开文件，写入模式（'w'）以覆盖之前的记录
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'PID', 'CPU%', 'MEM%'])

        try:
            print(f"Monitoring process {pid} with pidstat")

            while True:
                result_cpu = subprocess.run(['pidstat', '-p', str(pid), '-u'], capture_output=True, text=True)
                lines_cpu = result_cpu.stdout.split('\n')
                # print(f"{lines_cpu}")
                if len(lines_cpu) > 3:
                    data_cpu = lines_cpu[3].split()
                    if len(data_cpu) >= 8:
                        # timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        cpu_usage = float(data_cpu[7])
                        # mem_usage = float(data[8])
                        # print(f"Time: {timestamp}, CPU Usage: {cpu_usage:.4f}%")
                        # print(f"CPU Usage: {cpu_usage:.4f}%")
                        # writer.writerow([timestamp, pid, f"{cpu_usage:.4f}"])
                
                
                result_mem = subprocess.run(['pidstat', '-p', str(pid),'-r'], capture_output=True, text=True)
                lines_mem = result_mem.stdout.split('\n')
                # print(f"{lines_mem}")
                if len(lines_mem) > 3:
                    data_mem = lines_mem[3].split()
                    if len(data_mem) >= 8:
                        # timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        # cpu_usage = float(data[7])
                        mem_usage = float(data_mem[7])
                        # print(f"Memory Usage: {mem_usage:.4f}%")
                        # writer.writerow([ f"{mem_usage:.4f}"])
                if cpu_usage is not None and mem_usage is not None:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Time: {timestamp}, CPU Usage: {cpu_usage:.4f}%, Memory Usage: {mem_usage:.4f}%")
                    writer.writerow([timestamp, pid, f"{cpu_usage:.4f}", f"{mem_usage:.4f}"])


                time.sleep(5)
        except KeyboardInterrupt:
            print("Monitoring stopped.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    process_name = 'nr-uesoftmodem-208950000000035'
    pid = find_main_process(process_name)  # Assuming find_main_process is defined

    if pid:
        print(f"Main PID: {pid}")
        monitor_process_with_pidstat(pid, process_name)
    else:
        print(f"No main process found with name {process_name}.")

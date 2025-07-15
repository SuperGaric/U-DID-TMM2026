import os
import subprocess
import time
import threading
import csv
import psutil
from multiprocessing import Process
from threading import Lock
import pandas as pd 

def p3chain_monitor_resource_usage(process_name,interval,duration):
    # 确定输出文件的文件名
    output_file = f"{process_name}_usage_log.csv"
    
    # 检查文件是否存在，若不存在则创建并写入标题行
    # if not os.path.exists(output_file):
    with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PID', 'Average CPU%', 'Average MEM(MB)','Command'])
    

    process_data = {}
    start_time = time.time()

    try:
        while (time.time() - start_time) < duration:
            # 使用ps命令获取进程信息
            result = subprocess.run(['ps', '-C', process_name, '-o', 'pid,%cpu,rss,cmd'], 
                                    capture_output=True, text=True)
            # 处理ps命令的输出
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = output.split('\n')
                if len(lines) > 1:
                    # 打开CSV文件并追加数据
                    for info in lines[1:]:  # 跳过标题行
                        pid, cpu, rss, cmd = info.split(None, 3)
                        if pid not in process_data:
                            process_data[pid] = {'cpu':[], 'mem':[], 'cmd': cmd}
                        process_data[pid]['cpu'].append(float(cpu))
                        process_data[pid]['mem'].append(float(rss)/1024)

                else:
                    print(f"No process found with name {process_name}")
            else:
                print("Error executing ps command")

            time.sleep(interval)
        
        with open(output_file, mode = 'a', newline = '') as file:
            writer = csv.writer(file)
            for pid, data in process_data.items():
                avg_cpu = sum(data['cpu']) / len(data['cpu']) if data['cpu'] else 0
                avg_mem = sum(data['mem']) / len(data['mem']) if data['mem'] else 0
                writer.writerow([pid, f"{avg_cpu:.2f}", f"{avg_mem:.2f}", data['cmd']])

        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
def monitor_process_average(pid, process_name, interval,duration):
    # 输出文件名
    output_file = f"{process_name}_usage_averge_log.csv"

    # if not os.path.exists(output_file):
    with open(output_file,mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PID','Average CPU%','Average MEM(MB)']) 


    try:
        process = psutil.Process(pid)
        print(f"Monitoring process {pid}: {process.name()}")

        start_time = time.time()
        cpu_usage_samples = []
        memory_usage_samples = []

        while (time.time() - start_time) < duration:
            cpu_usage = process.cpu_percent(interval=0.5)
            memory_info = process.memory_info()
            memory_usage = memory_info.rss / (1024 ** 2)  # Convert to MB

            # if cpu_usage > 0 :
            #     cpu_usage_samples(cpu_usage)
            # if memory_usage > 0:
            #     memory_usage_samples.append(memory_usage)

            cpu_usage_samples.append(cpu_usage)
            memory_usage_samples.append(memory_usage)

            
            # print(f"CPU Usage: {cpu_usage:.4f}%")
            # print(f"Memory Usage: {memory_usage:.4f} MB")
        average_cpu = sum(cpu_usage_samples) / len(cpu_usage_samples)
        average_memory = sum(memory_usage_samples) / len(memory_usage_samples)

        print(f"Average CPU Usage: {average_cpu:.2f}%")
        print(f"Average Memory Usage: {average_memory:.2f} MB")


        with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([pid,f"{average_cpu:.2f}",f"{average_memory:.2f}"])
            
            # time.sleep(0.5)
    except psutil.NoSuchProcess:
        print(f"Process {pid} has terminated.")
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error: {e}")

def monitor_process_average_whole(process_name, interval, duration):
    main_pid = None
    candidate_pids = []
    pid = None
    ppid = None

    
    # 遍历所有进程，查找命令行中包含指定名称的进程
    for proc in psutil.process_iter(['pid', 'ppid', 'cmdline']):
        try:
            if any(process_name in cmd for cmd in proc.info['cmdline']):
                if 'exec bash' not in ''.join(proc.info['cmdline']):
                    candidate_pids.append(( proc.info['pid'], proc.info['ppid'], proc.info['cmdline']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(f"Candidate PIDs: {candidate_pids}")

    # 找到父进程不是目标进程的进程
    # for pid, ppid, cmdline in candidate_pids:
    #     try:
    #         # if 'exec bash' not in ''.join(cmdline):
    #         # if (cpu != 0) :
    #             parent = psutil.Process(ppid)
    #             # if not any(process_name in cmd for cmd in parent.cmdline()):
    #             main_pid = parent.pid
    #                 # break
    #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #         # main_pid = pid
    #         # break
    #         continue


    # if main_pid is None:
    #     print("No suitable process found for monitoring.")
    #     return
    
        # 输出文件名
    output_file = f"{process_name}_usage_average_log.csv"

    # if not os.path.exists(output_file):
    with open(output_file,mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PID','Average CPU%','Average MEM(MB)']) 


    try:
        process = psutil.Process(candidate_pids)
        print(f"Monitoring process {candidate_pids}: {process.name()}")

        start_time = time.time()
        cpu_usage_samples = []
        memory_usage_samples = []

        while (time.time() - start_time) < duration:
            cpu_usage = process.cpu_percent(interval=0.5)
            memory_info = process.memory_info()
            memory_usage = memory_info.rss / (1024 ** 2)  # Convert to MB

            # if cpu_usage > 0 :
            #     cpu_usage_samples(cpu_usage)
            # if memory_usage > 0:
            #     memory_usage_samples.append(memory_usage)

            cpu_usage_samples.append(cpu_usage)
            memory_usage_samples.append(memory_usage)

            
            # print(f"CPU Usage: {cpu_usage:.4f}%")
            # print(f"Memory Usage: {memory_usage:.4f} MB")
        average_cpu = sum(cpu_usage_samples) / len(cpu_usage_samples)
        average_memory = sum(memory_usage_samples) / len(memory_usage_samples)

        print(f"Average CPU Usage: {average_cpu:.2f}%")
        print(f"Average Memory Usage: {average_memory:.2f} MB")


        with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([main_pid,f"{average_cpu:.2f}",f"{average_memory:.2f}"])
            
            # time.sleep(0.5)
    except psutil.NoSuchProcess:
        print(f"Process {main_pid} has terminated.")
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error: {e}")
    
# def monitor_process_average_whole(process_name, interval, duration):
#     output_file = f"{process_name}_usage_average_log.csv"
  
#     # 创建空文件（覆盖模式）
#     with open(output_file, 'w') as f:
#         f.write('PID,Average CPU%,Average MEM(MB)\n')

#     # 进程发现
#     target_pids = []
#     for proc in psutil.process_iter(['pid', 'cmdline']):
#         try:
#             cmdline = ' '.join(proc.info['cmdline'])
#             # print(f"Debug: 检查进程 {proc.pid} -> {cmdline}")  # 调试输出
#             if f'./{process_name}' in cmdline:
#                 target_pids.append(proc.info['pid'])
#         except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
#             print(f"进程 {proc.pid} 访问失败: {e}")
#             continue

#     if not target_pids:
#         print(f"错误: 未找到{process_name}的活跃进程")
#         return

#     # 多进程监控
#     for pid in target_pids:
#         threading.Thread(
#             target=monitor_single_process,
#             args=(pid, output_file, interval, duration)
#         ).start()

# csv_write_lock = Lock()

# def monitor_single_process(pid, output_file, interval, duration):
#     """监控单个进程资源占用的完整实现"""
#     try:
#         # 1. 获取进程对象
#         process = psutil.Process(pid)
#         proc_name = process.name()
#         print(f"[{pid}] 开始监控进程 {proc_name} ({duration}s)")
      
#         # 2. 初始化采样数据
#         cpu_samples = []
#         mem_samples = []
#         start_time = time.time()
#         last_sample_time = start_time

#         # 3. 主监控循环
#         while (time.time() - start_time) < duration:
#             try:
#                 # 3.1 获取CPU使用率（间隔需≥0.1）
#                 cpu_usage = process.cpu_percent(interval=max(0.1, interval/2))
#                 cpu_samples.append(cpu_usage)

#                 # 3.2 获取内存使用（MB）
#                 mem_usage = process.memory_info().rss / (1024 ** 2)
#                 mem_samples.append(mem_usage)

#                 # 3.3 计算实际间隔
#                 elapsed = time.time() - last_sample_time
#                 sleep_time = max(0, interval - elapsed)
#                 time.sleep(sleep_time)
#                 last_sample_time = time.time()

#             except psutil.NoSuchProcess:
#                 print(f"[{pid}] 进程已终止")
#                 break
#             except psutil.AccessDenied:
#                 print(f"[{pid}] 权限不足")
#                 break
#             except Exception as e:
#                 print(f"[{pid}] 监控错误: {str(e)}")
#                 break

#         # 4. 计算结果
#         avg_cpu = sum(cpu_samples)/len(cpu_samples) if cpu_samples else 0
#         avg_mem = sum(mem_samples)/len(mem_samples) if mem_samples else 0
#         print(f"[{pid}] 监控结束 | CPU: {avg_cpu:.2f}% | MEM: {avg_mem:.2f}MB")

#         # 5. 线程安全写入（带异常处理）
#         with csv_write_lock:
#             try:
#                 with open(output_file, 'a') as f:
#                     f.write(f"{pid},{avg_cpu:.2f},{avg_mem:.2f}\n")
#             except IOError as e:
#                 print(f"[{pid}] 写入失败: {str(e)}")

#     except psutil.NoSuchProcess:
#         print(f"[{pid}] 初始检查: 进程不存在")
#     except psutil.AccessDenied as e:
#         print(f"[{pid}] 初始检查: 权限拒绝 ({e.msg})")
#     except Exception as e:
#         print(f"[{pid}] 意外错误: {str(e)}")

def monitor_docker_stats(container_name, interval, duration):
    output_file = f"{container_name}_usage_log.csv"

    # if not os.path.exists(output_file):
    with open(output_file,mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['container name','Average CPU%','Average MEM(MB)']) 

    cpu_usage_samples = []
    memory_usage_samples = []
    start_time = time.time()

    try:
        while (time.time()-start_time) < duration:
            result = subprocess.run(['docker','stats', container_name, '--no-stream','--format',"{{.CPUPerc}} {{.MemUsage}}"],capture_output=True,text=True)
            output = result.stdout.strip()
            if output:
                cpu_percent,mem_usage = output.split()[:2]

                cpu_percent = float(cpu_percent.replace('%',''))

                # mem_usage = float(mem_usage.split('/')[0].replace('MiB','').replace('GiB','') if 'MiB' in mem_usage or 'GiB' in mem_usage else 0)

                # Handle memory usage
                if 'MiB' in mem_usage:
                    mem_usage = float(mem_usage.replace('MiB', ''))
                elif 'GiB' in mem_usage:
                    mem_usage = float(mem_usage.replace('GiB', '')) * 1024
                else:
                    mem_usage = 0

                cpu_usage_samples.append(cpu_percent)
                memory_usage_samples.append(mem_usage)
        
            time.sleep(interval)
        
        if cpu_usage_samples and memory_usage_samples:
            average_cpu = sum(cpu_usage_samples) / len(cpu_usage_samples)
            average_memory = sum(memory_usage_samples) / len(memory_usage_samples)

            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([container_name, f"{average_cpu:.2f}",f"{average_memory:.2f}"])

            print(f"Average CPU Usage: {average_cpu:.2f}%")
            print(f"Average Memory Usage: {average_memory:.2f} MB")
        else:
            print("No data collected. Check if the container is running.")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to get docker stats: {e}")
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error: {e}")


def run_ue_process(directory, imsi):

    command = [
         f'./UE{imsi}'
    ]

    try: 
        subprocess.run(command, cwd=directory)
        print(f"Command launched in a new terminal for directory {directory} with UE{imsi}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start process for IMSI {imsi}: {e}")


def run_ue(directory, imsi, threads, interval, duration):

        ue_process = threading.Thread(target = run_ue_process, args = (directory, imsi))
        threads.append(ue_process)

    
       
        monitor_process_name = f"UE{imsi}"
        
        t_ue = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))
        threads.append(t_ue)

        ue_process.start()
        t_ue.start()


def run_Organization_process(directory):

    command = [
        './Organization'
    ]

    try: 
        subprocess.run(command, cwd=directory)
        print(f"Command launched in a new terminal for directory {directory} with gnb")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start process for gnb: {e}")

def run_Organization(directory, threads, interval, duration):
        gnb_process = threading.Thread(target=run_Organization_process, args=(directory,))

        threads.append(gnb_process)

        print(f"Command launched in a new terminal for directory {directory} with Organization")
        # start monitoring in a separate thread
        monitor_process_name = f"Organization"

        t_gnb = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))
        threads.append(t_gnb)
        
        gnb_process.start()
        time.sleep(10)
        t_gnb.start()




def get_dynamic_duration(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates = ['activat time','blockchain success time'])
        # if (df['blockchain success time'].iloc[0] == None ) :
        #     duration02 = (df['oai success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
        #     return duration02
        # else:
        duration01 = (df['blockchain success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
            # duration02 = (df['oai success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
            # return max(duration01, duration02)
        return duration01 + 5
    except Exception as e:
        print(f"error reading duration from file: {e}")
        return 60 


def main():
    count = 100
    
    base_directory = os.path.expanduser('~/multiple_UEs/baseline_experiment/UE')  
    initial_imsi = 0
    # projects = [f"openairinterface5g_copy_{i}" for i in range(1, count + 1)]
    gnb_project = os.path.expanduser('~/multiple_UEs/baseline_experiment/Organization')
    # ue_projects = [f"nr-uesoftmodem-{i}" for i in range(1 , count+1) ]

    duration_path = os.path.join(base_directory, 'timelogsaggreaget.csv')

    # 监测间隔，将会从时间集合的本子里提取
    duration = get_dynamic_duration(duration_path)
    print(f"the duration is :{duration}")
    interval = 0.2   
    threads = []



    
    
    t_p3Chain = threading.Thread(target = p3chain_monitor_resource_usage, args = ('p3Chain', interval, duration))
    threads.append(t_p3Chain)
    t_p3Chain.start()
    

    

    run_Organization(gnb_project, threads, interval, duration)

    ## activate UE
    # ue_project_path = os.path.join(base_directory)
    for  i in range(0, count):
        run_ue(base_directory, initial_imsi + i, threads, interval, duration)

        

    
    for thread in threads:
        thread.join()
    
    print("All threads have completed")



if __name__ == '__main__':
    main()


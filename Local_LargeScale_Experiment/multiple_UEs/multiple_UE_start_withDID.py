import os
import subprocess
import time
import threading
import csv
import psutil
from multiprocessing import Process
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
    for pid, ppid, cmdline in candidate_pids:
        try:
            # if 'exec bash' not in ''.join(cmdline):
            # if (cpu != 0) :
                parent = psutil.Process(ppid)
                # if not any(process_name in cmd for cmd in parent.cmdline()):
                main_pid = parent.pid
                    # break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # main_pid = pid
            # break
            continue
    # for pid, ppid, cmdline in candidate_pids:
    #     try:
    #         if 'exec bash' not in ' '.join(cmdline):
    #             parent = psutil.Process(ppid)
    #             parent_cmdline = ' '.join(parent.cmdline())
    #             if not any(process_name in cmd for cmd in parent.cmdline()):
    #                 main_pid = pid
    #                 break
    #             else:
    #                 print(f"Skipping process {pid} with parent {ppid} because parent cmdline contains the process name: {parent_cmdline}")
    #         else:
    #             print(f"Skipping process {pid} because cmdline contains 'exec bash': {' '.join(cmdline)}")
    #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
    #         print(f"Exception while processing parent of PID {pid}: {e}")
    #         continue    

    if main_pid is None:
        print("No suitable process found for monitoring.")
        return
    
        # 输出文件名
    output_file = f"{process_name}_usage_average_log.csv"

    # if not os.path.exists(output_file):
    with open(output_file,mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PID','Average CPU%','Average MEM(MB)']) 


    try:
        process = psutil.Process(main_pid)
        print(f"Monitoring process {main_pid}: {process.name()}")

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



def run_ue(directory, imsi, threads, interval, duration):
    # 构建命令行参数
    command = ' '.join([
         f'./nr-uesoftmodem-{imsi}', '-r', '106', '--numerology', '1',
        '--band', '78', '-C', '3619200000', '--sa', f'--uicc0.imsi', str(imsi), '--rfsim'
    ])

    # command =[
    #      f'./nr-uesoftmodem-{imsi}', 
    #      '-r', '106', 
    #      '--numerology', '1',
    #     '--band', '78', 
    #     '-C', '3619200000', 
    #     '--sa', 
    #     f'--uicc0.imsi', str(imsi), 
    #     '--rfsim'
    # ]

    # 执行命令
    terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True, check=True)
        # proc = subprocess.Popen(command, cwd = directory)
        
        print(f"Command launched in a new terminal for directory {directory} with IMSI {imsi}")
        # start monitoring in a separate thread
        monitor_process_name = f"nr-uesoftmodem-{imsi}"
        # monitor_process_average_whole(monitor_process_name, interval, duration)
        t_ue = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))
        # t_ue = threading.Thread(target=monitor_process_average, args=(proc.pid, monitor_process_name, interval, duration))
        threads.append(t_ue)
        t_ue.start()
        # monitor_ports = []
        # log_file = f"nr-uesoftmodem_{imsi}_usage.csv"
        # monitoring_thread = threading.Thread(target=monitor_resource_usage, args=(monitor_process_name, log_file))
        # monitoring_thread.start()
    except subprocess.CalledProcessError as e:
        print(f"Failed to start terminal for directory {directory}")


def run_gnb(directory, threads, interval, duration):
    command = ' '.join([
        './nr-softmodem', '-O', '../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf', '--gNBs.[0].min_rxtxtime', '6' ,'--rfsim', '--sa'
    ])

    # command = [
    #     './nr-softmodem', 
    #     '-O', '../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf', 
    #     '--gNBs.[0].min_rxtxtime', '6',
    #     '--rfsim', '--sa'
    # ]
    #执行命令
    terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True, check=True)
        # proc = subprocess.Popen(command, cwd = directory)
        print(f"Command launched in a new terminal for directory {directory} with gNB")
        # start monitoring in a separate thread
        monitor_process_name = f"nr-softmodem"
        # monitor_ports = []
        # log_file = f"nr-softmodem_gnb_usage.csv"
        # t_gnb = threading.Thread(target=monitor_process_average, args=(proc.pid, monitor_process_name, interval, duration))
        t_gnb = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))
        threads.append(t_gnb)
        t_gnb.start()
        # monitor_process_average_whole(monitor_process_name, interval, duration)
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start terminal for directory {directory}")

def get_dynamic_duration(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates = ['activat time', 'oai success time', 'blockchain success time'])
        # if (df['blockchain success time'].iloc[0] == None ) :
        #     duration02 = (df['oai success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
        #     return duration02
        # else:
        duration01 = (df['blockchain success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
            # duration02 = (df['oai success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()
            # return max(duration01, duration02)
        return duration01
    except Exception as e:
        print(f"error reading duration from file: {e}")
        return 60 


def main():
    count = 5
    
    base_directory = os.path.expanduser('~/multiple_UEs')  
    initial_imsi = 208950000000031
    # projects = [f"openairinterface5g_copy_{i}" for i in range(1, count + 1)]
    gnb_project = "01-modified-openairinterface5g-onlyapp-try" 
    ue_projects = [f"nr-uesoftmodem-{i}" for i in range(1 , count+1) ]

    duration_path = os.path.join(base_directory, 'timelogsaggreaget.csv')

    # 监测间隔，将会从时间集合的本子里提取
    duration = get_dynamic_duration(duration_path)
    print(f"the duration is :{duration}")
    interval = 0.5   
    

    # monitor_ports = [8080 + i for i in range(count)]
    # log_file = os.path.join(base_directory,"didserver_usage_log.csv")
    # monitoring_thread = threading.Thread(target=monitor_resource_usage_ports,args=(monitor_ports,log_file))
    # monitoring_thread.start()

    didserver_names = [f"{i}" for i in range(8080, 8080 + count + 1)]
    docker_containers = ['oai-amf', 'oai-smf', 'oai-upf', 'oai-ausf', 'oai-udm', 'oai-udr', 'mysql', 'oai-nrf', 'oai-ext-dn']
    threads = []
    processes = []
    for container in docker_containers: 
        t = threading.Thread(target= monitor_docker_stats, args=(container, interval, duration))
        threads.append(t)
        t.start()
    
    t_p3Chain = threading.Thread(target = p3chain_monitor_resource_usage, args = ('p3Chain', interval, duration))
    threads.append(t_p3Chain)
    t_p3Chain.start()
    

    ###old version for simply copy ue activation
    # for i, project in enumerate(projects):
    #     project_path = os.path.join(base_directory, project, 'cmake_targets', 'ran_build', 'build')
    #     if i == 0 :
    #         run_gnb(project_path, threads, interval, duration)
    #         # p_gnb = Process(target = run_gnb, args = (project_path, threads, interval, duration))
    #         # p_gnb.start()
    #         # processes.append(p_gnb)
    #     # monitor_process_average_whole(monitor_ports[i], interval, duration)
    #     run_ue(project_path, initial_imsi + i, threads, interval, duration)
    #     # ue_thread = threading.Thread(target = run_ue, args = (project_path, initial_imsi + i, threads, interval, duration))
    #     # threads.append(ue_thread)
    #     # ue_thread.start()

    #     # p_ue = Process(target = run_ue, args = (project_path, initial_imsi + i, threads, interval, duration))
    #     # p_ue.start()
    #     # processes.append(p_ue)

        
    #     t_didserver = threading.Thread(target = monitor_process_average_whole, args = (didserver_names[i], interval, duration))
    #     threads.append(t_didserver)
    #     t_didserver.start()        

        ## activate gnb
    gnb_project_path = os.path.join(base_directory, gnb_project, 'cmake_targets', 'ran_build', 'build')

    run_gnb(gnb_project_path, threads, interval, duration)

    ## activate UE
    ue_project_path = os.path.join(base_directory, 'compiled_binaries_withDID')
    for  i, ue_project in enumerate(ue_projects):
        run_ue(ue_project_path, initial_imsi + i, threads, interval, duration)

        
        t_didserver = threading.Thread(target = monitor_process_average_whole, args = (didserver_names[i], interval, duration))
        threads.append(t_didserver)
        t_didserver.start()     



if __name__ == '__main__':
    main()


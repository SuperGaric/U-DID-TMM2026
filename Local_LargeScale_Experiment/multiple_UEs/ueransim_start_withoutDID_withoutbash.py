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

            cpu_usage_samples.append(cpu_usage)
            memory_usage_samples.append(memory_usage)

            

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
                parent = psutil.Process(ppid)
                main_pid = parent.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            
            continue
 

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

# 启动UE(ueransim版本)
def run_core_network_process(directory):
    command = [
         'docker-compose', '-f', 'docker-compose-basic-vpp-nrf.yaml', 'up', '-d'
    ]

    try: 
        subprocess.run(command, cwd=directory)
        print(f"Command launched in a new terminal for directory {directory} with Core")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start process for Core: {e}")


def run_core_network(directory,  threads, interval, duration):
        core_network_process = threading.Thread(target = run_core_network_process, args = (directory,))
        threads.append(core_network_process)
        core_network_process.start()
        time.sleep(18)





def run_ueransim_process(directory):
    command = [
         'docker-compose', '-f', 'docker-compose-ueransim-vpp.yaml', 'up', '-d'
    ]

    try: 
        subprocess.run(command, cwd=directory)
        print(f"Command launched in a new terminal for directory {directory} with UERANSIM")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start process for UERANSIM: {e}")


def run_ueransim(directory,  threads, interval, duration):
        ueransim_process = threading.Thread(target = run_ueransim_process, args = (directory,))
        threads.append(ueransim_process)
        ueransim_process.start()

        container = "ueransim"

        t_ueransim = threading.Thread(target= monitor_docker_stats, args=(container, interval, duration)) 
        threads.append(t_ueransim)
        t_ueransim.start()




# def run_ue_process(directory, imsi):
#     command = [
#          f'./nr-uesoftmodem-{imsi}', '-r', '106', '--numerology', '1',
#         '--band', '78', '-C', '3619200000', '--sa', f'--uicc0.imsi', str(imsi), '--rfsim'
#     ]

#     try: 
#         subprocess.run(command, cwd=directory)
#         print(f"Command launched in a new terminal for directory {directory} with IMSI {imsi}")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to start process for IMSI {imsi}: {e}")


# def run_ue(directory, imsi, threads, interval, duration):
#         ue_process = threading.Thread(target = run_ue_process, args = (directory, imsi))
#         threads.append(ue_process)
#         ue_process.start()

#         monitor_process_name = f"nr-uesoftmodem-{imsi}"

#         t_ue = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))

#         threads.append(t_ue)
#         t_ue.start()


# def run_gnb_process(directory):
#     command = [
#         './nr-softmodem', '-O', '../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf', '--gNBs.[0].min_rxtxtime', '6' ,'--rfsim', '--sa'
#     ]

#     try: 
#         subprocess.run(command, cwd=directory)
#         print(f"Command launched in a new terminal for directory {directory} with gnb")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to start process for gnb: {e}")

# def run_gnb(directory, threads, interval, duration):
#         gnb_process = threading.Thread(target=run_gnb_process, args=(directory,))
#         gnb_process.start()
#         threads.append(gnb_process)

#         print(f"Command launched in a new terminal for directory {directory} with gNB")
#         monitor_process_name = f"nr-softmodem"
 
#         t_gnb = threading.Thread(target=monitor_process_average_whole, args=(monitor_process_name, interval, duration))
#         threads.append(t_gnb)
#         t_gnb.start()

#         time.sleep(5)


def get_dynamic_duration(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates = ['activat time', 'oai success time'])
        duration01 = (df['oai success time'].iloc[0] - df['activat time'].iloc[0]).total_seconds()

        return duration01
    except Exception as e:
        print(f"error reading duration from file: {e}")
        return 60 


def main():
    # count = 100  # 选择ueransim中启动的UE数量，但是切记一定要去docker-compose-ueransim-vpp.yaml里面进行对应地修改
    CORE_UERANSIM_base_directory = os.path.expanduser('/home/dmt/oai-cn5g-fed/docker-compose')
    Activation_Monitor_base_directory = os.path.expanduser('/home/dmt/multiple_UEs')
    
    # 定义监测和时间的
    duration_path = os.path.join(Activation_Monitor_base_directory, 'timelogsaggreaget.csv')

    # 监测间隔，将会从时间集合的本子里提取
    duration = get_dynamic_duration(duration_path)
    print(f"the duration is :{duration}")
    interval = 0.5   
    
    threads = []
    processes = []

    # 启动核心网
    run_core_network(CORE_UERANSIM_base_directory, threads, interval, duration)
    
    # 监测didserver, 监测各个网元，监测p3chain
    # didserver_names = [f"{i}" for i in range(8081, 8081 + count + 1)]
    docker_containers = ['oai-amf', 'oai-smf', 'oai-upf', 'oai-ausf', 'oai-udm', 'oai-udr', 'mysql', 'oai-nrf', 'oai-ext-dn']

    for container in docker_containers: 
        t = threading.Thread(target= monitor_docker_stats, args=(container, interval, duration + 5 )) #因为启动比ue早，所以给一个5s的冗余
        threads.append(t)
        t.start()
    
    # 同样不需要这个
    # t_p3Chain = threading.Thread(target = p3chain_monitor_resource_usage, args = ('p3Chain', interval, duration + 5)) 
    # threads.append(t_p3Chain)
    # t_p3Chain.start()

    #启动ueransim（启动之前需要去docker-compose-ueransim-vpp.yaml里面修改
    run_ueransim(CORE_UERANSIM_base_directory, threads, interval, duration)

    # 启动监控DIDserver(withoutDID的版本不需要监测)
    # for i, _ in enumerate (didserver_names) :
    #     t_didserver = threading.Thread(target = monitor_process_average_whole, args = (didserver_names[i], interval, duration))
    #     threads.append(t_didserver)
    #     t_didserver.start() 


    for thread in threads:
        thread.join()
    
    print("All threads have completed")



if __name__ == '__main__':
    main()



    
    
#     ## ----------------------------------------------------------------------------------------------------

#     base_directory = os.path.expanduser('~/multiple_UEs')  
#     initial_imsi = 208950000000031

#     gnb_project = "01-modified-openairinterface5g-onlyapp-try" 
#     ue_projects = [f"nr-uesoftmodem-{i}" for i in range(1 , count+1) ]

#     duration_path = os.path.join(base_directory, 'timelogsaggreaget.csv')

#     # 监测间隔，将会从时间集合的本子里提取
#     duration = get_dynamic_duration(duration_path)
#     print(f"the duration is :{duration}")
#     interval = 0.5   
    


#     didserver_names = [f"{i}" for i in range(8080, 8080 + count + 1)]
#     docker_containers = ['oai-amf', 'oai-smf', 'oai-upf', 'oai-ausf', 'oai-udm', 'oai-udr', 'mysql', 'oai-nrf', 'oai-ext-dn']
#     threads = []
#     processes = []
#     for container in docker_containers: 
#         t = threading.Thread(target= monitor_docker_stats, args=(container, interval, duration))
#         threads.append(t)
#         t.start()
    
#     t_p3Chain = threading.Thread(target = p3chain_monitor_resource_usage, args = ('p3Chain', interval, duration))
#     threads.append(t_p3Chain)
#     t_p3Chain.start()
    


#     gnb_project_path = os.path.join(base_directory, gnb_project, 'cmake_targets', 'ran_build', 'build')

#     run_gnb(gnb_project_path, threads, interval, duration)

#     ## activate UE
#     ue_project_path = os.path.join(base_directory, 'compiled_binaries_withDID')
#     for  i, ue_project in enumerate(ue_projects):
#         run_ue(ue_project_path, initial_imsi + i, threads, interval, duration)

        
#         t_didserver = threading.Thread(target = monitor_process_average_whole, args = (didserver_names[i], interval, duration))
#         threads.append(t_didserver)
#         t_didserver.start()     
    
#     for thread in threads:
#         thread.join()
    
#     print("All threads have completed")



# if __name__ == '__main__':
#     main()


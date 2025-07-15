import os
import subprocess
import threading

def run_didserver_process(directory,port):
    command = [
    f"./{port}"
    ]
    try:
        subprocess.run(command, cwd=directory)
        print(f"Command launched in a new didserver for directory {directory} with port {port}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start didserver for directory {directory}")


def run_didserver(directory, port, thread):
    # 构建命令行参数
    # command = ' '.join([
    #     './',str(port)
    # ])

    # command = f"./{port}"

    # print(f"{command}")

    # 执行命令
    # terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    didserver_process = threading.Thread(target = run_didserver_process, args = (directory, port))
    thread.append(didserver_process)
    didserver_process.start()
    print(f"Command launched in a new terminal for Didserver {port}")


def main():
    threads = []
    base_directory = os.path.expanduser('~/multiple_UEs/didserver_local')  
    initial_port = 8081

    count = 100 #chage the number to open the didserver count
    

    projects = [f"{initial_port -1 + i}" for i in range(1, count+1)]

    for i, project in enumerate(projects):
        project_path = os.path.join(base_directory)
        run_didserver(project_path, initial_port +i, threads)
        print(f"{initial_port  +i}")
    
    for thread in threads:
        thread.join()
    
    print("All threads have completed")

if __name__ == '__main__':
    main()


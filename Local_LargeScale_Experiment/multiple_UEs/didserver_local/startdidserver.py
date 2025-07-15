import os
import subprocess

def run_didserver(directory, port):
    # 构建命令行参数
    # command = ' '.join([
    #     './',str(port)
    # ])

    command = f"./{port}"

    print(f"{command}")

    # 执行命令
    terminal_command = f"gnome-terminal --working-directory={directory} -- bash -c '{command}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True, check=True)
        print(f"Command launched in a new didserver for directory {directory} with port {port}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start didserver for directory {directory}")

def main():
    base_directory = os.path.expanduser('~/multiple_UEs/didserver_local')  
    initial_port = 8081

    count = 100 #chage the number to open the didserver count

    # projects = [f"{initial_port -1 + i}" for i in range(1, count+1)]
    

    
    # for i, project in enumerate(projects):
    #     project_path = os.path.join(base_directory)
    #     run_didserver(project_path, initial_port +i)
    #     print(f"{initial_port  +i}")

    for i in range(count):
        project_path = os.path.join(base_directory)
        port = initial_port + i
        run_didserver(project_path, port)
        print(f"launched server at {port}")

if __name__ == '__main__':
    main()


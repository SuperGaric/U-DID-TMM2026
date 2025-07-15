import os

# configuration
go_file_path = os.path.expanduser('~/multiple_UEs/didserver_local/main.go')
output_dir = os.path.expanduser('~/multiple_UEs/didserver_local')

base_port = 8081
num_versions = 100  # 需要生成的版本数量，这里修改为5，从8080到8084

original_file_data = None

# compilation
for i in range(num_versions):
    new_port = base_port + i

    if original_file_data is None:
        with open(go_file_path, 'r') as file: 
            original_file_data = file.read()

    # read file
    with open(go_file_path, 'r') as file:
        file_data = file.read()

    # change port 
    if i == 0:
        file_data = file_data.replace(':8080',f':{new_port}')
        now_port = new_port
    else:
        file_data = file_data.replace(f':{now_port}',f':{new_port}')
        now_port = new_port
    # base_port = new_port


    # write the original file
    with open(go_file_path,'w') as file:
        file.write(file_data)
    
    # compilation
    executable_name = os.path.join(output_dir, f'{new_port}')
    compile_command = f'go build -o {executable_name} {go_file_path}'

    os.system(compile_command)
    print(f"compiled executable {executable_name} with port {new_port}")


# print("所有版本编译完成。")
restored_file_data = original_file_data
with open(go_file_path,'w') as file:
#         file.write(file_data)
    file.write(restored_file_data)

print("编译完成,并恢复原始端口8080。")


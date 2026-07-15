import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
REMOTE_DIR = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP/FP_NO'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)

# 1. List all files in the project
print("="*60)
print("【1】FP_NO 项目文件列表")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'ls -la {REMOTE_DIR}/')
print(stdout.read().decode())

# 2. Read gtree.dat (project tree and variables)
print("="*60)
print("【2】gtree.dat - 项目树与变量")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/gtree.dat')
print(stdout.read().decode())

# 3. Read sde_dvs.cmd (structure)
print("="*60)
print("【3】sde_dvs.cmd - SDE 结构代码")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/sde_dvs.cmd')
print(stdout.read().decode())

# 4. Read sdevice_des.cmd (device simulation)
print("="*60)
print("【4】sdevice_des.cmd - 器件仿真配置")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/sdevice_des.cmd')
print(stdout.read().decode())

# 5. Check if there's a common file
print("="*60)
print("【5】其他 .cmd 文件")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/*.cmd 2>/dev/null || echo "No other cmd files"')
print(stdout.read().decode())

# 6. Check .project file
print("="*60)
print("【6】.project 文件")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/.project')
print(stdout.read().decode())

client.close()

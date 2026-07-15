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

# gtree.dat
print("="*60)
print("gtree.dat - 项目树与变量定义")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/gtree.dat')
print(stdout.read().decode())

# Check all files
print("="*60)
print("文件列表")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'ls -la {REMOTE_DIR}/')
print(stdout.read().decode())

# common_des.cmd
print("="*60)
print("common_des.cmd")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {REMOTE_DIR}/common_des.cmd')
print(stdout.read().decode())

client.close()

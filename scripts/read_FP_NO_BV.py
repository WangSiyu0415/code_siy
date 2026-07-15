import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
DIR = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP/FP_NO'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)

# 1. Status file
print("="*50)
print("[1] n89_des.sta - 状态")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/n89_des.sta')
print(stdout.read().decode())

# 2. Last 200 lines of log file (look for breakdown info)
print("="*50)
print("[2] n89_des.log - 末尾200行")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'tail -200 {DIR}/n89_des.log')
print(stdout.read().decode())

# 3. First 100 lines of log
print("="*50)
print("[3] n89_des.log - 开头50行")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'head -50 {DIR}/n89_des.log')
print(stdout.read().decode())

# 4. gsummary.txt
print("="*50)
print("[4] gsummary.txt - 项目概要")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/gsummary.txt')
print(stdout.read().decode())

# 5. Check what other BV-related result files exist
print("="*50)
print("[5] BV 相关结果文件")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'ls -lh {DIR}/n89* {DIR}/BV* 2>/dev/null')
print(stdout.read().decode())

# 6. Try to extract text from plt - first check if it's binary
print("="*50)
print("[6] n89_des.plt - 文件类型和开头")
print("="*50)
stdin, stdout, stderr = client.exec_command(f'file {DIR}/n89_des.plt && xxd {DIR}/n89_des.plt 2>/dev/null | head -20 || od -c {DIR}/n89_des.plt 2>/dev/null | head -20')
print(stdout.read().decode())

client.close()

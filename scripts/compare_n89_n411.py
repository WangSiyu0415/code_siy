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

# 1. n411 status
print("="*60)
print("[1] n411_des.sta - 状态")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/n411_des.sta')
print(stdout.read().decode())

# 2. n411 config
print("="*60)
print("[2] pp411_des.cmd - n411 仿真配置")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/pp411_des.cmd')
print(stdout.read().decode())

# 3. n89 status for comparison
print("="*60)
print("[3] n89_des.sta - n89 状态对比")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/n89_des.sta')
print(stdout.read().decode())

# 4. n89 config
print("="*60)
print("[4] pp89_des.cmd - n89 仿真配置")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/pp89_des.cmd')
print(stdout.read().decode())

# 5. Check gtree.dat for n89 and n411 position
print("="*60)
print("[5] gtree - n89 和 n411 在任务树中的位置")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep -n "89\\|411" {DIR}/gtree.dat | head -30')
print(stdout.read().decode())

# 6. n411 log file - check the exit type and final Vd
print("="*60)
print("[6] n411_des.log - 末尾30行 (看终止原因)")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'tail -30 {DIR}/n411_des.log')
print(stdout.read().decode())

# 7. Also check n411 plt header for drain voltage range
print("="*60)
print("[7] n411_des.plt - 检查 Vd 范围")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'head -20 {DIR}/n411_des.plt')
print(stdout.read().decode())

client.close()

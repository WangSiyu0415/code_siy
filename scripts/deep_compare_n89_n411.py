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

# 1. Check which grid/mesh each uses
print("="*60)
print("[1] Grid file used by n89 vs n411")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep "Grid" {DIR}/pp89_des.cmd {DIR}/pp411_des.cmd')
print(stdout.read().decode())

# 2. Check the .par files
print("="*60)
print("[2] pp89_des.par 内容")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/pp89_des.par')
print(stdout.read().decode())

print("="*60)
print("[3] pp411_des.par 内容")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/pp411_des.par')
print(stdout.read().decode())

# 3. Find n220 and n405 in the gtree - what variables do they have?
print("="*60)
print("[4] gtree中n220和n405的参数")
print("="*60)

# From gtree, find the lines around n220 and n405
# The format seems to be: depth node_id parent_id {value} {scenario} misc
stdin, stdout, stderr = client.exec_command(f'grep -n " 220\\| 405\\| 89\\|411" {DIR}/gtree.dat')
print(stdout.read().decode())

# 4. Check the SDE cmd files for n220 and n405 
print("="*60)
print("[5] n220用的是哪个sde cmd？")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'ls -la {DIR}/n220* {DIR}/n405*')
print(stdout.read().decode())

stdin, stdout, stderr = client.exec_command(f'readlink -f {DIR}/n220_dvs.cmd && readlink -f {DIR}/n405_dvs.cmd')
real_paths = stdout.read().decode()
print("Real paths:", real_paths)

# 5. Check what variables are different - Lgd? 
# Read the gtree.dat more fully around these entries
print("="*60)
print("[6] gtree 参数树 - 找n89和n411对应的参数")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/gtree.dat')
gtree = stdout.read().decode()

# Let me parse the gtree structure more carefully
# I see format: depth node parent {value} {scenario} status
# The first few numbers are depth indicators
lines = gtree.strip().split('\n')
print("Looking for parameter values...")
for line in lines:
    parts = line.strip().split()
    if len(parts) >= 4:
        node = parts[1]
        # Find nodes 220 and 405 (the SDE structure nodes)
        if node in ['220', '405', '89', '411']:
            print(f"  Node {node}: {line.strip()}")

# Also check the gexec.cmd for the actual parameter values
print("="*60)
print("[7] gexec.cmd - 参数赋值")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/gexec.cmd')
print(stdout.read().decode())

# 8. Check the gvars.dat
print("="*60)
print("[8] gvars.dat")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/gvars.dat')
print(stdout.read().decode())

client.close()

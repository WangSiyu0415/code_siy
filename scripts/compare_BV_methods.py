import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
BASE = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP'
PROJECTS = ['FP_GD_1', 'FP_GSD_2', 'FP_NO', 'FP_SD']

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)

# 1. Compare BV_des.cmd across all projects
print("=" * 70)
print("1. BV_des.cmd 对比（所有项目）")
print("=" * 70)
for proj in PROJECTS:
    print(f"\n--- {proj}/BV_des.cmd ---")
    stdin, stdout, stderr = client.exec_command(f'cat {BASE}/{proj}/BV_des.cmd')
    print(stdout.read().decode())

# 2. Compare common_des.cmd across projects
print("=" * 70)
print("2. common_des.cmd 差异对比")
print("=" * 70)
for i in range(len(PROJECTS)):
    for j in range(i+1, len(PROJECTS)):
        p1, p2 = PROJECTS[i], PROJECTS[j]
        stdin, stdout, stderr = client.exec_command(f'diff {BASE}/{p1}/common_des.cmd {BASE}/{p2}/common_des.cmd && echo "IDENTICAL" || echo "DIFFERENT (see above)"')
        result = stdout.read().decode()
        if 'IDENTICAL' not in result:
            print(f"\n--- {p1} vs {p2} common_des.cmd ---")
            print(result)

# 3. Pick one BV pp*_des.cmd from each project and compare
print("=" * 70)
print("3. BV 节点命令 (pp*_des.cmd) 简单对比")
print("=" * 70)

# Get one BV-related pp file from each project
bv_nodes = {
    'FP_GD_1': None,
    'FP_GSD_2': None,
    'FP_NO': 'pp89_des.cmd',
    'FP_SD': 'pp89_des.cmd',
}

# For FP_GD_1, find which pp file does BV
stdin, stdout, stderr = client.exec_command(f'grep -l "Avalanche\\|eAvalanche\\|BreakCriteria" {BASE}/FP_GD_1/pp*_des.cmd')
print(f"FP_GD_1 BV pp files: {stdout.read().decode()}")

stdin, stdout, stderr = client.exec_command(f'grep -l "Avalanche\\|eAvalanche\\|BreakCriteria" {BASE}/FP_GSD_2/pp*_des.cmd')
print(f"FP_GSD_2 BV pp files: {stdout.read().decode()}")

# Also check common_des.cmd for Avalanche
print("\n--- common_des.cmd 中是否有 Avalanche ---")
for proj in PROJECTS:
    stdin, stdout, stderr = client.exec_command(f'grep -n "Avalanche\\|BreakCriteria\\|eAvalanche" {BASE}/{proj}/common_des.cmd || echo "None found"')
    print(f"{proj}: {stdout.read().strip()}")

client.close()

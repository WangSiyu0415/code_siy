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

# Check the SDE command files - look for how Lgd is defined
# pp220_dvs.cmd and pp405_dvs.cmd should be symlinks to the same sde_dvs.cmd
# but with different parameter substitutions

print("="*60)
print("[1] pp220_dvs.cmd 和 pp405_dvs.cmd 是否相同？")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'diff {DIR}/pp220_dvs.cmd {DIR}/pp405_dvs.cmd && echo "IDENTICAL" || echo "DIFFERENT"')
print(stdout.read().decode())

# The SDE cmd has @Lgd@ variable. Let's check what values were substituted
print("="*60)
print("[2] 检查 n220_dvs.log 中 Lgd 的值")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep -i "lgd\\|Lgd" {DIR}/n220_dvs.log')
print(stdout.read().decode())

print("="*60)
print("[3] 检查 n405_dvs.log 中 Lgd 的值")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep -i "lgd\\|Lgd" {DIR}/n405_dvs.log')
print(stdout.read().decode())

# Also check from the topology: what parameters feed into each
print("="*60)
print("[4] gtree 参数追溯 - 215的父节点")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep -n " 215 " {DIR}/gtree.dat')
print(stdout.read().decode())

# Print full parameter tree for Lgd branches
print("="*60)
print("[5] 完整参数树结构分析")
print("="*60)
stdin, stdout, stderr = client.exec_command(f"awk '{{if($1==7||$1==8||$1==9) print}}' {DIR}/gtree.dat | head -40")
print(stdout.read().decode())

# Compare the two SDE log files to find the variable differences
print("="*60)
print("[6] 从SDE log提取关键参数")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'grep -E "define|Lgd|Lg|Lsg|tpGaN|NpGaN|tAlGaN|xAlGaN|FPg1|tFP" {DIR}/n220_dvs.log | head -20')
print("--- n220 ---")
print(stdout.read().decode())
stdin, stdout, stderr = client.exec_command(f'grep -E "define|Lgd|Lg|Lsg|tpGaN|NpGaN|tAlGaN|xAlGaN|FPg1|tFP" {DIR}/n405_dvs.log | head -20')
print("--- n405 ---")
print(stdout.read().decode())

# Actually, the SDE log might not show the define values directly. 
# Let me check n220_dvs.out and n405_dvs.out
print("="*60)
print("[7] n220_dvs.out - 变量值")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'head -30 {DIR}/n220_dvs.out')
print(stdout.read().decode())

print("="*60)
print("[8] n405_dvs.out - 变量值")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'head -30 {DIR}/n405_dvs.out')
print(stdout.read().decode())

# Let me also check the .history file for the project
print("="*60)
print("[9] .history - 项目运行历史")
print("="*60)
stdin, stdout, stderr = client.exec_command(f'cat {DIR}/.history')
print(stdout.read().decode())

client.close()

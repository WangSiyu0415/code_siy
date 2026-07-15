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

for proj in PROJECTS:
    print(f"\n{'='*70}")
    print(f"  项目: {proj}")
    print(f"{'='*70}")
    
    # Find BV-related files
    stdin, stdout, stderr = client.exec_command(f'ls {BASE}/{proj}/BV* {BASE}/{proj}/*BV* 2>/dev/null')
    print(f"BV相关文件:")
    print(stdout.read().decode())
    
    # Find all pp*_des.cmd files (sdevice commands)
    stdin, stdout, stderr = client.exec_command(f'ls {BASE}/{proj}/pp*_des.cmd 2>/dev/null')
    pp_files = stdout.read().decode().strip().split('\n')
    print(f"sdevice命令文件 ({len(pp_files)}个):")
    for pf in pp_files:
        print(f"  {pf.split('/')[-1]}")
    
    # Check common_des.cmd
    stdin, stdout, stderr = client.exec_command(f'wc -l {BASE}/{proj}/common_des.cmd 2>/dev/null')
    print(f"common_des.cmd: {stdout.read().strip()}")
    
    # Check if there's a central sdevice_des.cmd
    stdin, stdout, stderr = client.exec_command(f'wc -l {BASE}/{proj}/sdevice_des.cmd 2>/dev/null')
    print(f"sdevice_des.cmd: {stdout.read().strip()}")

    # List all BV or transient/cmd related
    stdin, stdout, stderr = client.exec_command(f'ls {BASE}/{proj}/*.cmd 2>/dev/null | head -20')
    print(f"所有cmd文件:")
    print(stdout.read().decode())

client.close()

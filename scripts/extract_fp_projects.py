import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
REMOTE_DIR = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP'

FILES = ['FP_GD_1.gzp', 'FP_GSD_2.gzp', 'FP_NO.gzp', 'FP_SD.gzp']

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)
print("Connected!")

for fname in FILES:
    proj_name = fname.replace('.gzp', '')
    print(f"\n{'='*50}")
    print(f"Extracting {fname} ...")
    
    command = f'cd {REMOTE_DIR} && swbunpack {fname} 2>&1'
    stdin, stdout, stderr = client.exec_command(command)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    
    if out:
        print(f"  stdout: {out}")
    if err:
        print(f"  stderr: {err}")
    
    if exit_code == 0:
        print(f"  [OK] {fname} extracted successfully!")
    else:
        print(f"  [FAILED] exit code: {exit_code}")

print(f"\n{'='*50}")
print("Verifying extracted directories...")
stdin, stdout, stderr = client.exec_command(f'ls -lh {REMOTE_DIR}/')
print(stdout.read().decode())

client.close()
print("Done!")

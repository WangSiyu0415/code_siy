import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko
import os
import time

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
REMOTE_DIR = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP'
LOCAL_DIR = 'D:/a_experiment/sentauruse/sentaurus_data/世平仿真'

FILES = ['FP_GD_1.gzp', 'FP_GSD_2.gzp', 'FP_NO.gzp', 'FP_SD.gzp']

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)
print("Connected!")

# Create directory
stdin, stdout, stderr = client.exec_command(f'mkdir -p {REMOTE_DIR}')
print("mkdir done")

sftp = client.open_sftp()
success = 0

for fname in FILES:
    local_path = os.path.join(LOCAL_DIR, fname)
    remote_path = f'{REMOTE_DIR}/{fname}'
    
    if not os.path.exists(local_path):
        print(f"[{fname}] NOT FOUND locally!")
        continue
    
    size_mb = os.path.getsize(local_path) / (1024*1024)
    print(f"[{fname}] Uploading ({size_mb:.1f} MB) to {remote_path} ...")
    
    try:
        # Use sftp.put with confirmation
        sftp.put(local_path, remote_path)
        
        # Verify: check file size on remote
        remote_attr = sftp.stat(remote_path)
        local_size = os.path.getsize(local_path)
        print(f"  Local: {local_size} bytes, Remote: {remote_attr.st_size} bytes")
        
        if remote_attr.st_size == local_size:
            print(f"  VERIFIED OK!")
            success += 1
        else:
            print(f"  SIZE MISMATCH! Retrying...")
            # Delete partial and retry
            try:
                sftp.remove(remote_path)
            except:
                pass
            sftp.put(local_path, remote_path)
            remote_attr = sftp.stat(remote_path)
            if remote_attr.st_size == local_size:
                print(f"  Retry VERIFIED OK!")
                success += 1
            else:
                print(f"  Still mismatch!")
                
    except Exception as e:
        print(f"  FAILED: {e}")

sftp.close()
client.close()

print(f"\n=== Result: {success}/{len(FILES)} files uploaded to {REMOTE_DIR} ===")

# Final verification
print("\n=== Final verification ===")
client2 = paramiko.SSHClient()
client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client2.connect(HOST, port=PORT, username=USER, password=PASSWORD,
                allow_agent=False, look_for_keys=False)
stdin, stdout, stderr = client2.exec_command(f'ls -lh {REMOTE_DIR}/')
print(stdout.read().decode())
client2.close()

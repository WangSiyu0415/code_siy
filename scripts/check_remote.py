import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('58.199.136.91', port=22, username='klren',
               password='987654321', allow_agent=False, look_for_keys=False)

# Check ShiPing_FP directory
stdin, stdout, stderr = client.exec_command('ls -lh /home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP/')
print('=== ShiPing_FP/ ===')
print(stdout.read().decode())
err = stderr.read().decode()
if err:
    print('STDERR:', err)

# Check parent directory for any FP files that might be loose
stdin, stdout, stderr = client.exec_command('find /home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ -name "FP_*.gzp" -maxdepth 2')
print('=== All FP_*.gzp files ===')
print(stdout.read().decode())

client.close()

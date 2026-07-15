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

sftp = client.open_sftp()

# Read n411.plt
with sftp.open(f'{DIR}/n411_des.plt') as f:
    content_n411 = f.read().decode('utf-8')

# Also read n89.plt again for comparison
with sftp.open(f'{DIR}/n89_des.plt') as f:
    content_n89 = f.read().decode('utf-8')

sftp.close()
client.close()

def parse_plt(content, label):
    lines = content.split('\n')
    in_data = False
    all_numbers = []
    for line in lines:
        line_stripped = line.strip()
        if line_stripped == 'Data {':
            in_data = True
            continue
        if in_data:
            if line_stripped == '}':
                break
            parts = line_stripped.split()
            for p in parts:
                try:
                    all_numbers.append(float(p))
                except:
                    pass
    
    NCOLS = 25
    npoints = len(all_numbers) // NCOLS
    
    vd_list = []
    id_list = []
    id_mm_list = []
    
    for i in range(npoints):
        row = all_numbers[i*NCOLS:(i+1)*NCOLS]
        vd = row[17]
        id_tot = row[23]
        vd_list.append(vd)
        id_list.append(id_tot)
        id_mm_list.append(id_tot * 1000)
    
    return vd_list, id_list, id_mm_list

vd_n89, id_n89, id_mm_n89 = parse_plt(content_n89, "n89 (Lgd=5.7, FPg1=1.7)")
vd_n411, id_n411, id_mm_n411 = parse_plt(content_n411, "n411 (Lgd=5.5, FPg1=1.5)")

print("="*100)
print(f"{'Vd (V)':>10} {'n89 Id(A/mm)':>18} {'n411 Id(A/mm)':>18} {'Ratio':>12}")
print("="*100)

# Print side by side (interpolate or closest match)
# Since time steps might be different, let's match by index at key regions
max_pts = max(len(vd_n89), len(vd_n411))
for i in range(min(len(vd_n89), len(vd_n411))):
    if i % max(1, min(len(vd_n89), len(vd_n411))//25) == 0 or i == min(len(vd_n89), len(vd_n411))-1:
        v89 = vd_n89[i]
        v411 = vd_n411[i]
        i89 = id_mm_n89[i]
        i411 = id_mm_n411[i]
        ratio = i411/i89 if i89 > 0 else float('inf')
        print(f"{v89:>10.3f} {i89:>18.6e} {i411:>18.6e} {ratio:>12.2f}")

print(f"\n{'='*100}")
print(f"统计对比:")
print(f"{'='*100}")
print(f"{'指标':<40} {'n89 (Lgd=5.7)':>18} {'n411 (Lgd=5.5)':>18}")
print(f"{'-'*76}")
print(f"{'最大 Vd (V)':<40} {vd_n89[-1]:>18.2f} {vd_n411[-1]:>18.2f}")
print(f"{'最大 Id (A/mm)':<40} {id_mm_n89[-1]:>18.6e} {id_mm_n411[-1]:>18.6e}")
print(f"{'数据点数':<40} {len(vd_n89):>18} {len(vd_n411):>18}")
print(f"{'Id @ Vd≈100V (A/mm)':<40} ", end="")
# Find Id at ~100V
for v,i in zip(vd_n89, id_mm_n89):
    if abs(v-100)<5:
        print(f"{i:>18.6e} ", end="")
        break
for v,i in zip(vd_n411, id_mm_n411):
    if abs(v-100)<5:
        print(f"{i:>18.6e}")
        break
print(f"{'Id @ Vd≈300V (A/mm)':<40} ", end="")
for v,i in zip(vd_n89, id_mm_n89):
    if abs(v-300)<5:
        print(f"{i:>18.6e} ", end="")
        break
for v,i in zip(vd_n411, id_mm_n411):
    if abs(v-300)<5:
        print(f"{i:>18.6e}")
        break
print(f"{'Id @ Vd≈500V (A/mm)':<40} ", end="")
for v,i in zip(vd_n89, id_mm_n89):
    if abs(v-500)<5:
        print(f"{i:>18.6e} ", end="")
        break
for v,i in zip(vd_n411, id_mm_n411):
    if abs(v-500)<5:
        print(f"{i:>18.6e}")
        break

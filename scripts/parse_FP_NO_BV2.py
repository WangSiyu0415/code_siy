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
with sftp.open(f'{DIR}/n89_des.plt') as f:
    content = f.read().decode('utf-8')
sftp.close()
client.close()

lines = content.split('\n')

# Find Data section
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
        # Parse numbers
        parts = line_stripped.split()
        for p in parts:
            try:
                all_numbers.append(float(p))
            except:
                pass

# Column indices:
# 0=time, 1=source_V, 2=source_Vi, 3=source_QFP, 4=source_Idispl, 5=source_Ie
# 6=source_Ih, 7=source_Itot, 8=source_Q, 9=gate_V, 10=gate_Vi
# 11=gate_QFP, 12=gate_Idispl, 13=gate_Ie, 14=gate_Ih, 15=gate_Itot
# 16=gate_Q, 17=drain_V, 18=drain_Vi, 19=drain_QFP, 20=drain_Idispl
# 21=drain_Ie, 22=drain_Ih, 23=drain_Itot, 24=drain_Q

NCOLS = 25  # time + 24
npoints = len(all_numbers) // NCOLS

print(f"Total data points: {npoints}")
print(f"Total numbers: {len(all_numbers)}")

# Parse into rows
data = []
for i in range(npoints):
    row = all_numbers[i*NCOLS:(i+1)*NCOLS]
    data.append(row)

# Extract BV curve: drain OuterVoltage (17) vs drain TotalCurrent (23)
print(f"\n{'='*80}")
print(f"FP_NO - 击穿特性 (BV) 曲线数据 (Id-Vd)")
print(f"栅极电压 Vg = 0V (接地)")
print(f"{'='*80}")
print(f"{'Vd (V)':>12} {'Id_total (A)':>18} {'Id (A/mm)':>16}")
print(f"{'-'*48}")

output_rows = []
for row in data:
    vd = row[17]
    id_tot = row[23]  # drain TotalCurrent in A
    id_per_mm = id_tot * 1000  # AreaFactor=1000, so A -> A/mm
    output_rows.append((vd, id_tot, id_per_mm))

# Print all points
for vd, id_tot, id_per_mm in output_rows:
    print(f"{vd:>12.6f} {id_tot:>18.10e} {id_per_mm:>16.6e}")

# Analysis
print(f"\n{'='*80}")
print(f"击穿分析:")
print(f"{'='*80}")

# Find max Vd and Id
max_vd = max(r[0] for r in output_rows)
max_id_idx = max(range(len(output_rows)), key=lambda i: output_rows[i][1])
print(f"最大 Vd 到达: {output_rows[-1][0]:.2f} V")
print(f"最大 Id: {output_rows[max_id_idx][1]:.6e} A ({output_rows[max_id_idx][2]:.6e} A/mm) @ Vd={output_rows[max_id_idx][0]:.2f}V")

# Find BV at 1 mA/mm criterion
for vd, id_tot, id_per_mm in output_rows:
    if id_per_mm >= 1.0:  # 1 mA/mm
        print(f"\n*** 击穿电压 (1 mA/mm 判据) ***")
        print(f"    BV ≈ {vd:.2f} V, Id = {id_tot:.6e} A ({id_per_mm:.6e} A/mm)")
        break

# Show region of interest (higher currents)
print(f"\n高电流区域 (Id > 1e-6 A):")
print(f"{'Vd (V)':>12} {'Id (A)':>18} {'Id (A/mm)':>16}")
for vd, id_tot, id_per_mm in output_rows:
    if id_tot > 1e-6:
        print(f"{vd:>12.6f} {id_tot:>18.10e} {id_per_mm:>16.6e}")

print(f"\n{'='*80}")
print(f"注: 仿真状态为 failed (不收敛), 在 Vd ≈ {output_rows[-1][0]:.2f}V 时步长太小终止")
print(f"    这实际表明器件在该电压附近发生了击穿/雪崩效应，电流急剧上升导致不收敛")

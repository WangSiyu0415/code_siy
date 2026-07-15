import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko
import io

HOST = '58.199.136.91'
PORT = 22
USER = 'klren'
PASSWORD = '987654321'
DIR = '/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/ShiPing_FP/FP_NO'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USER, password=PASSWORD,
               allow_agent=False, look_for_keys=False, timeout=30)

# Download the plt file via SFTP and read it
sftp = client.open_sftp()
with sftp.open(f'{DIR}/n89_des.plt') as f:
    content = f.read().decode('utf-8')

sftp.close()
client.close()

# Parse the DF-ISE text format
lines = content.split('\n')

# Find the data section
data_start = None
data_end = None
datasets = []
current_dataset = None

for i, line in enumerate(lines):
    if line.startswith('data'):
        data_start = i
    if data_start is not None and line.strip() == '}':
        data_end = i
        break

# Extract dataset names
in_datasets = False
for line in lines:
    if 'datasets' in line and '=' in line:
        in_datasets = True
        continue
    if in_datasets:
        if ']' in line:
            in_datasets = False
            continue
        name = line.strip().strip('"').strip(',')
        if name:
            datasets.append(name)

# Parse data section
if data_start is not None and data_end is not None:
    data_lines = lines[data_start+1:data_end]
    data_text = '\n'.join(data_lines)
    
    # The data is in columns format
    # Split by whitespace and collect
    rows = []
    for line in data_lines:
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 2:
                rows.append(parts)
    
    print(f"Total datasets ({len(datasets)}):")
    for i, d in enumerate(datasets):
        print(f"  [{i}] {d}")
    
    print(f"\nTotal data points: {len(rows)}")
    print(f"\nFirst 5 rows:")
    for r in rows[:5]:
        print(f"  {r}")
    print(f"\nLast 5 rows:")
    for r in rows[-5:]:
        print(f"  {r}")
    
    # Find column indices
    # 2 = time, 3 = source OuterVoltage, ... drain OuterVoltage, drain TotalCurrent
    col_names = datasets
    
    # Find drain OuterVoltage and drain TotalCurrent
    drain_v_idx = None
    drain_i_idx = None
    gate_v_idx = None
    
    for i, name in enumerate(col_names):
        if 'drain' in name and 'OuterVoltage' in name:
            drain_v_idx = i
        if 'drain' in name and 'TotalCurrent' in name:
            drain_i_idx = i
        if 'gate' in name and 'OuterVoltage' in name:
            gate_v_idx = i
    
    print(f"\nColumn indices: drain_V={drain_v_idx}, drain_I={drain_i_idx}, gate_V={gate_v_idx}")
    
    if drain_v_idx is not None and drain_i_idx is not None:
        # Extract BV curve data
        print(f"\n{'='*80}")
        print(f"BV 击穿特性曲线 (Id-Vd):")
        print(f"{'='*80}")
        print(f"{'Vd (V)':>12} {'Id (A)':>16} {'Id (A/mm)':>16}")
        print(f"{'-'*44}")
        
        data_points = []
        for r in rows:
            if len(r) > max(drain_v_idx, drain_i_idx):
                try:
                    vd = float(r[drain_v_idx])
                    id_val = float(r[drain_i_idx])
                    id_per_mm = id_val * 1000  # AreaFactor=1000, so A -> A/mm
                    data_points.append((vd, id_val, id_per_mm))
                except:
                    pass
        
        # Print every Nth point to avoid too much output
        step = max(1, len(data_points) // 50)
        for i, (vd, id_val, id_per_mm) in enumerate(data_points):
            if i % step == 0 or i == len(data_points) - 1:
                print(f"{vd:>12.4f} {id_val:>16.6e} {id_per_mm:>16.6e}")
        
        # Find breakdown voltage (current reaches 1e-3 A/mm or sudden increase)
        print(f"\n{'='*80}")
        print(f"BV 分析:")
        print(f"{'='*80}")
        
        # Find Vd where Id starts rising sharply
        prev_id = data_points[0][1] if data_points else 0
        bv_candidates = []
        for vd, id_val, id_per_mm in data_points:
            if id_val > 1e-3 and id_per_mm > 1.0:  # 1 mA/mm
                bv_candidates.append((vd, id_val, id_per_mm))
                break
            if id_val > 1e-6 and prev_id > 0 and id_val/prev_id > 10:
                bv_candidates.append((vd, id_val, id_per_mm))
            prev_id = id_val
        
        if bv_candidates:
            print(f"  BV onset (Id > 1 mA/mm): Vd = {bv_candidates[0][0]:.2f} V, Id = {bv_candidates[0][1]:.6e} A ({bv_candidates[0][2]:.6e} A/mm)")
        
        # Final max voltage
        last = data_points[-1]
        print(f"  Max Vd reached: {last[0]:.2f} V, Id = {last[1]:.6e} A ({last[2]:.6e} A/mm)")
        
        # Find min and max values
        min_id = min(p[1] for p in data_points)
        max_id = max(p[1] for p in data_points)
        min_vd = min(p[0] for p in data_points)
        max_vd = max(p[0] for p in data_points)
        
        print(f"  Id range: {min_id:.2e} ~ {max_id:.2e} A")
        print(f"  Vd range: {min_vd:.2f} ~ {max_vd:.2f} V")

else:
    print("Could not find data section in plt file")
    # Print first 50 lines for debugging
    for line in lines[:50]:
        print(line)

import sys
sys.path.insert(0, 'C:\\Python314\\Lib\\site-packages')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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

vd_vals = []
id_vals = []
id_per_mm_vals = []

for i in range(npoints):
    row = all_numbers[i*NCOLS:(i+1)*NCOLS]
    vd = row[17]
    id_tot = row[23]
    vd_vals.append(vd)
    id_vals.append(id_tot)
    id_per_mm_vals.append(id_tot * 1000)

# Convert to numpy arrays
vd_arr = np.array(vd_vals)
id_arr = np.array(id_vals)
id_mm_arr = np.array(id_per_mm_vals)

# ========== Plot 1: Id-Vd linear scale ==========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Linear scale
ax1.plot(vd_arr, id_mm_arr, 'b-', linewidth=1.5, label='FP_NO (No Field Plate)')
ax1.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, label='1 mA/mm (BV criterion)')
ax1.axvline(x=583.4, color='orange', linestyle=':', alpha=0.7, label='Simulation failed @ 583V')
ax1.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax1.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax1.set_title('BV Curve - Linear Scale', fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 650)

# Right: Semi-log scale
ax2.semilogy(vd_arr, id_mm_arr, 'b-', linewidth=1.5, label='FP_NO (No Field Plate)')
ax2.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, label='1 mA/mm (BV criterion)')
ax2.axvline(x=583.4, color='orange', linestyle=':', alpha=0.7, label='Simulation failed @ 583V')
ax2.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax2.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax2.set_title('BV Curve - Semi-log Scale', fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 650)
ax2.set_ylim(1e-10, 1e-2)

plt.tight_layout()
plt.savefig('d:/a_experiment/sentauruse/sentaurus_data/FP_NO_BV_curve.png', dpi=150, bbox_inches='tight')
print("Saved: FP_NO_BV_curve.png")

# ========== Plot 2: Zoomed high-field region ==========
fig2, ax3 = plt.subplots(figsize=(8, 5))

# Find index where Vd > 500
idx_start = np.searchsorted(vd_arr, 500)
vd_zoom = vd_arr[idx_start:]
id_mm_zoom = id_mm_arr[idx_start:]

ax3.plot(vd_zoom, id_mm_zoom, 'b-o', markersize=3, linewidth=1.5, label='FP_NO')
ax3.axvline(x=583.4, color='orange', linestyle=':', linewidth=2, label='Simulation termination')
ax3.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax3.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax3.set_title('BV Curve - High Voltage Region (Zoom)', fontsize=13)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(500, 600)

# Annotate last point
last_vd = vd_arr[-1]
last_id = id_mm_arr[-1]
ax3.annotate(f'Vd={last_vd:.1f}V\nId={last_id:.2e} A/mm',
             xy=(last_vd, last_id),
             xytext=(last_vd-30, last_id*3),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')

plt.tight_layout()
plt.savefig('d:/a_experiment/sentauruse/sentaurus_data/FP_NO_BV_curve_zoom.png', dpi=150, bbox_inches='tight')
print("Saved: FP_NO_BV_curve_zoom.png")

print("\nDone! Both plots saved successfully.")

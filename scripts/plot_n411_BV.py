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

for fname, label in [('n89_des.plt', 'n89'), ('n411_des.plt', 'n411')]:
    with sftp.open(f'{DIR}/{fname}') as f:
        content = f.read().decode('utf-8')
    
    lines = content.split('\n')
    in_data = False
    nums = []
    for line in lines:
        s = line.strip()
        if s == 'Data {':
            in_data = True
            continue
        if in_data:
            if s == '}':
                break
            for p in s.split():
                try:
                    nums.append(float(p))
                except:
                    pass
    
    NCOLS = 25
    npts = len(nums) // NCOLS
    vd, id_mm = [], []
    for i in range(npts):
        row = nums[i*NCOLS:(i+1)*NCOLS]
        vd.append(row[17])
        id_mm.append(row[23] * 1000)
    
    if label == 'n89':
        vd_89, id_89 = vd, id_mm
        label_89 = f'n89 (Lgd=5.7, failed @ {vd[-1]:.0f}V)'
    else:
        vd_411, id_411 = vd, id_mm
        label_411 = f'n411 (Lgd=5.5, BV @ {vd[-1]:.0f}V)'

sftp.close()
client.close()

# ========== Figure 1: n411 BV curve only ==========
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Linear
ax1.plot(vd_411, id_411, 'g-', linewidth=2)
ax1.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, linewidth=1.5, label='1 mA/mm (BV criterion)')
ax1.axvline(x=689, color='orange', linestyle=':', alpha=0.7, label=f'BV ~ 689V')

# Annotate BV point
idx_bv = next(i for i, v in enumerate(id_411) if v >= 1e-3)
ax1.annotate(f'BV ≈ {vd_411[idx_bv]:.0f}V\nId = {id_411[idx_bv]:.2e} A/mm',
             xy=(vd_411[idx_bv], id_411[idx_bv]),
             xytext=(vd_411[idx_bv]-100, id_411[idx_bv]*2),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1.5),
             fontsize=11, color='red', fontweight='bold')

ax1.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax1.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax1.set_title('n411 — BV Curve (Linear)', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 750)

# Right: Semi-log
ax2.semilogy(vd_411, id_411, 'g-', linewidth=2)
ax2.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, linewidth=1.5, label='1 mA/mm (BV criterion)')
ax2.axvline(x=689, color='orange', linestyle=':', alpha=0.7, label=f'BV ~ 689V')

# Mark BV region
ax2.fill_between(vd_411[idx_bv:], [1e-8]*len(vd_411[idx_bv:]), id_411[idx_bv:],
                 color='red', alpha=0.1, label='Avalanche region')

ax2.annotate(f'BV ≈ {vd_411[idx_bv]:.0f}V\nId = {id_411[idx_bv]:.2e} A/mm',
             xy=(vd_411[idx_bv], id_411[idx_bv]),
             xytext=(vd_411[idx_bv]-120, id_411[idx_bv]*3),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1.5),
             fontsize=11, color='red', fontweight='bold')

ax2.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax2.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax2.set_title('n411 — BV Curve (Semi-log)', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 750)
ax2.set_ylim(1e-9, 1e-1)

plt.tight_layout()
plt.savefig('d:/a_experiment/sentauruse/sentaurus_data/FP_NO_n411_BV_curve.png', dpi=150, bbox_inches='tight')
print("Saved: FP_NO_n411_BV_curve.png")

# ========== Figure 2: n89 vs n411 comparison ==========
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 6))

# Linear comparison
ax3.plot(vd_89, id_89, 'b-', linewidth=1.5, label=label_89)
ax3.plot(vd_411, id_411, 'g-', linewidth=2, label=label_411)
ax3.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, linewidth=1.5, label='1 mA/mm BV criterion')
ax3.axvline(x=583, color='blue', linestyle=':', alpha=0.5)
ax3.axvline(x=689, color='green', linestyle=':', alpha=0.5)
ax3.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax3.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax3.set_title('n89 vs n411 — BV Comparison (Linear)', fontsize=13, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 750)

# Semi-log comparison
ax4.semilogy(vd_89, id_89, 'b-', linewidth=1.5, label=label_89)
ax4.semilogy(vd_411, id_411, 'g-', linewidth=2, label=label_411)
ax4.axhline(y=1e-3, color='r', linestyle='--', alpha=0.7, linewidth=1.5, label='1 mA/mm BV criterion')
ax4.axvline(x=583, color='blue', linestyle=':', alpha=0.5)
ax4.axvline(x=689, color='green', linestyle=':', alpha=0.5)

ax4.fill_between(vd_411[idx_bv:], [1e-9]*len(vd_411[idx_bv:]), id_411[idx_bv:],
                 color='green', alpha=0.08, label='n411 avalanche')
ax4.fill_between(vd_89[-5:], [1e-9]*5, id_89[-5:],
                 color='blue', alpha=0.08, label='n89 numerical failure')

ax4.set_xlabel('Drain Voltage V$_{DS}$ (V)', fontsize=12)
ax4.set_ylabel('Drain Current I$_D$ (A/mm)', fontsize=12)
ax4.set_title('n89 vs n411 — BV Comparison (Semi-log)', fontsize=13, fontweight='bold')
ax4.legend(fontsize=10, loc='upper left')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 750)
ax4.set_ylim(1e-9, 1e-1)

plt.tight_layout()
plt.savefig('d:/a_experiment/sentauruse/sentaurus_data/FP_NO_n89_vs_n411_BV.png', dpi=150, bbox_inches='tight')
print("Saved: FP_NO_n89_vs_n411_BV.png")

print("\nDone!")

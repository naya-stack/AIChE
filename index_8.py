import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor('#0f172a')
fig.suptitle("Slide 8: The High-K Solution", color='white', fontsize=16)

# --- SETUP LEFT (SiO2 - Problem) ---
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 6)
ax1.set_facecolor('#1e1e1e')
ax1.set_title("SiO₂ (Thin Barrier)", color='white')
wall_left = patches.Rectangle((4.9, 0), 0.2, 6, color='gray')
ax1.add_patch(wall_left)

# --- SETUP RIGHT (HfO2 - Solution) ---
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 6)
ax2.set_facecolor('#1e1e1e')
ax2.set_title("HfO₂ (High-K Barrier)", color='white')
wall_right = patches.Rectangle((4.5, 0), 1.0, 6, color='#10b981', alpha=0.7) # Thicker, Green
ax2.add_patch(wall_right)

# Label for shield
shield_text = ax2.text(5, 3, "SHIELD", color='white', ha='center', va='center', alpha=0.0, fontweight='bold')

# --- ELECTRONS ---
# Left electrons (Leakers)
elecs_left = []
for _ in range(10):
    e = plt.Circle((np.random.uniform(0, 4), np.random.uniform(0.5, 5.5)), 0.12, color='cyan')
    ax1.add_patch(e)
    elecs_left.append({'patch': e, 'x': e.center[0], 'vx': np.random.uniform(0.1, 0.2)})

# Right electrons (Bouncers)
elecs_right = []
for _ in range(10):
    e = plt.Circle((np.random.uniform(0, 4), np.random.uniform(0.5, 5.5)), 0.12, color='cyan')
    ax2.add_patch(e)
    elecs_right.append({'patch': e, 'x': e.center[0], 'vx': np.random.uniform(0.1, 0.2)})

def update(frame):
    # --- UPDATE LEFT (SiO2) ---
    for e_obj in elecs_left:
        e = e_obj['patch']
        e_obj['x'] += e_obj['vx']
        
        # Interaction with Thin Wall (4.9 - 5.1)
        if 4.9 < e_obj['x'] < 5.1:
            # 90% Tunnel rate (The Problem)
            if np.random.rand() > 0.1: 
                pass # Tunnel through
            else:
                e_obj['vx'] *= -1 # Bounce
        
        # Reset
        if e_obj['x'] > 10 or e_obj['x'] < -2:
            e_obj['x'] = -1
            e_obj['vx'] = abs(e_obj['vx'])
            
        e.set_center((e_obj['x'], e.center[1]))

    # --- UPDATE RIGHT (HfO2) ---
    for e_obj in elecs_right:
        e = e_obj['patch']
        e_obj['x'] += e_obj['vx']
        
        # Interaction with Thick Wall (4.5 - 5.5)
        # If it hits the left side of the wall (4.5)
        if e_obj['x'] >= 4.5 and e_obj['vx'] > 0:
            e_obj['vx'] *= -1 # Bounce Back (The Solution)
            # Add a little jitter y to simulate scattering
            e.center = (e.center[0], e.center[1] + np.random.uniform(-0.1, 0.1))
            
        # Reset
        if e_obj['x'] < -2:
            e_obj['x'] = -1
            e_obj['vx'] = abs(e_obj['vx'])
            
        e.set_center((e_obj['x'], e.center[1]))
    
    # Shield Flash Effect
    if frame % 20 < 10:
        shield_text.set_alpha(0.8)
    else:
        shield_text.set_alpha(0.4)

    return []

ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=False)
plt.show()
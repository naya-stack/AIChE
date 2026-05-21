import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_facecolor('#0f172a') # Dark Blue Start
fig.patch.set_facecolor('#0f172a')

# --- ELEMENTS ---
# The Wall (Thin SiO2)
wall = patches.Rectangle((4.8, 0), 0.4, 6, color='gray', alpha=0.5, label='SiO2 Barrier')
ax.add_patch(wall)

# The Hot Zone (Red background behind wall - Initially Invisible)
hot_zone = patches.Rectangle((5.2, 0), 4.8, 6, color='red', alpha=0.0)
ax.add_patch(hot_zone)

# Text
leakage_text = ax.text(7.5, 3, "LEAKAGE", color='red', fontsize=20, fontweight='bold', alpha=0.0, ha='center')
status_text = ax.text(5, 5.5, "System Status: NORMAL", color='white', ha='center')

# Electrons (Cyan Dots)
num_electrons = 15
electrons = []
for _ in range(num_electrons):
    # Initialize electrons on the left
    e = plt.Circle((np.random.uniform(-2, 4), np.random.uniform(0.5, 5.5)), 0.1, color='cyan')
    ax.add_patch(e)
    electrons.append({'patch': e, 'x': e.center[0], 'y': e.center[1], 'vx': np.random.uniform(0.1, 0.2)})

def update(frame):
    global electrons
    current_leakage = 0
    
    # Update Electrons
    for e_obj in electrons:
        e = e_obj['patch']
        
        # Move Right
        e_obj['x'] += e_obj['vx']
        
        # Check Wall Collision (x > 4.8)
        if 4.8 < e_obj['x'] < 5.2:
            # Tunneling Logic: 70% chance to tunnel (The Glitch)
            if np.random.rand() > 0.3:
                pass # Tunnels through
            else:
                # Bounce back
                e_obj['vx'] *= -1
        
        # Check Boundary (Reset if off screen)
        if e_obj['x'] > 10 or e_obj['x'] < -2:
            e_obj['x'] = -1
            e_obj['vx'] = abs(e_obj['vx']) # Reset velocity to right
            
        e.set_center((e_obj['x'], e_obj['y']))
        
        # Count leakage
        if e_obj['x'] > 5.2:
            current_leakage += 1
            
    # Update Environment based on Leakage
    # The more electrons on the right, the redder it gets
    leakage_intensity = min(1.0, current_leakage / 5.0) # Max out at 5 electrons
    
    hot_zone.set_alpha(leakage_intensity * 0.6) # Max alpha 0.6
    leakage_text.set_alpha(leakage_intensity)
    
    # Pulse Text
    if frame % 10 < 5 and leakage_intensity > 0.5:
        leakage_text.set_fontsize(22)
    else:
        leakage_text.set_fontsize(20)

    # Update Status Text
    if leakage_intensity > 0.5:
        status_text.set_text("WARNING: QUANTUM LEAKAGE DETECTED")
        status_text.set_color('red')
    else:
        status_text.set_text("System Status: NORMAL")
        status_text.set_color('white')

    return [wall, hot_zone, leakage_text, status_text] + [e['patch'] for e in electrons]

ani = animation.FuncAnimation(fig, update, frames=600, interval=30, blit=False)
plt.title("Slide 6: The Leakage Crisis (SiO2 Failure)", color='white')
plt.show()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')

# Data
materials = ['SiO₂\n(Low K)', 'HfO₂\n(High K)']
d_vals = [1, 6] # Thickness (d)
k_vals = [3.9, 25] # Dielectric Constant (K)
# Assume C = K/d for visualization (ignoring constants)
c_vals = [3.9/1, 25/6] 

# Bar Chart Setup
bar_colors = ['#ef4444', '#10b981'] # Red for old, Green for new
bars = ax.bar(materials, d_vals, color=bar_colors, alpha=0.6, width=0.5)

# Text Labels
ax.set_ylabel("Thickness (d)", color='white', fontsize=12)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title("The Chemical Engineering Magic: C = κε₀A/d", color='cyan', fontsize=16)

# Capacitance Labels (Floating above bars)
cap_text_1 = ax.text(0, 1.2, f"C = {c_vals[0]:.2f}", color='white', ha='center', fontsize=12)
cap_text_2 = ax.text(1, 6.2, f"C = {c_vals[1]:.2f}", color='white', ha='center', fontsize=12, fontweight='bold')

# K-Value Labels (Below X axis)
k_text_1 = ax.text(0, -0.5, f"K = {k_vals[0]}", color='gray', ha='center')
k_text_2 = ax.text(1, -0.5, f"K = {k_vals[1]}", color='#10b981', ha='center', fontsize=14, fontweight='bold')

# Equation Display
eqn_text = ax.text(0.5, 5, "C ∝ K / d", color='white', fontsize=20, ha='center', alpha=0.0)

def animate(frame):
    # Animation Logic: Grow the bars
    if frame < 50:
        # Phase 1: Show SiO2
        bars[0].set_height(d_vals[0] * (frame/50))
    elif frame < 100:
        # Phase 2: Show HfO2 Growing
        progress = (frame - 50) / 50
        bars[1].set_height(d_vals[1] * progress)
        
        # Highlight the K value
        if progress > 0.8:
            k_text_2.set_fontsize(18)
            k_text_2.set_color('#06b6d4')
    
    # Phase 3: Show Equation Logic
    if frame > 120:
        eqn_text.set_alpha(1.0)
        if frame % 20 < 10: # Pulse effect
            eqn_text.set_color('#06b6d4')
        else:
            eqn_text.set_color('white')
            
    return bars

ani = FuncAnimation(fig, animate, frames=180, interval=30, blit=False)
plt.ylim(0, 8)
plt.show()
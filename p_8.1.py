import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0f172a') 
ax.set_facecolor('#0f172a')
ax.set_title("Slide 8: The High-K Solution (HfO₂)", color='white', fontsize=15)

# Physics Parameters for REFLECTION
L = 10.0
V0 = 5.0       # Very High Barrier
E = 1.0        # Same Electron Energy
barrier_w = 2.0 # Thicker Barrier
barrier_x = 4.0

k = np.sqrt(2 * E)
kappa = np.sqrt(2 * (V0 - E)) # Large decay constant

# Draw Barrier (Green for Safety)
ax.axvspan(barrier_x, barrier_x + barrier_w, color='#10b981', alpha=0.4, label='HfO₂ High-κ')
ax.axhline(y=E, color='white', linestyle='--', alpha=0.3)

# Wave Packet
x = np.linspace(0, L, 500)
line, = ax.plot([], [], color='#06b6d4', lw=3)
fill = ax.fill_between(x, 0, 0, color='#06b6d4', alpha=0.2)

# Success Text
success_text = ax.text(5, 0.5, "ZERO LEAKAGE", color='#10b981', fontsize=16, ha='center', fontweight='bold', alpha=0.0)

def psi_reflect(x, t):
    sigma = 1.0
    x0 = 2.0 + 0.1*t
    
    # Incident Wave
    psi_inc = np.exp(-0.5 * ((x - x0)/sigma)**2) * np.exp(1j * k * x - 1j * E * t)
    
    # Create Reflected Wave (Visual trick for animation)
    # Starts appearing when incident wave hits the wall
    dist_to_wall = x0 - barrier_x
    
    psi_final = np.zeros_like(x, dtype=complex)
    
    mask_before = x < barrier_x
    mask_barrier = (x >= barrier_x) & (x < barrier_x + barrier_w)
    mask_after = x >= barrier_x + barrier_w
    
    psi_final[mask_before] = psi_inc[mask_before]
    
    # Reflection Logic
    if dist_to_wall < sigma * 2:
        # Add a wave moving LEFT (-k*x)
        psi_ref = -0.9 * np.exp(-0.5 * ((x - (2*barrier_x - x0))/sigma)**2) * np.exp(-1j * k * x - 1j * E * t)
        psi_final[mask_before] += psi_ref[mask_before]
    
    # Inside Barrier (Heavy Decay)
    psi_final[mask_barrier] *= 0.1
    
    # After Barrier (ZERO Transmission)
    psi_final[mask_after] = 0.0
    
    return psi_final

def animate(frame):
    t = frame * 0.2
    y = psi_reflect(x, t)
    prob = np.abs(y)**2
    
    line.set_data(x, prob)
    global fill
    fill.remove()
    fill = ax.fill_between(x, prob, 0, color='#06b6d4', alpha=0.2)
    
    # Show Success Text when wave hits wall
    if frame > 40:
        success_text.set_alpha(1.0)
    
    return line, fill, success_text

ax.set_xlim(0, L)
ax.set_ylim(0, 0.8)
ax.tick_params(colors='white')
ax.legend(loc='upper right', facecolor='#0f172a', labelcolor='white')

ani = animation.FuncAnimation(fig, animate, frames=200, interval=30, blit=False)
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0f172a') # Dark Blue Background
ax.set_facecolor('#0f172a')
ax.set_title("Slide 6: Quantum Leakage (SiO₂ Failure)", color='white', fontsize=15)

# Physics Parameters for LEAKAGE
L = 10.0
V0 = 1.5       # Barrier Height (Low)
E = 1.0        # Electron Energy
barrier_w = 1.0 # Thin Barrier
barrier_x = 4.5

k = np.sqrt(2 * E)
kappa = np.sqrt(2 * (V0 - E))

# Draw Barrier
ax.axvspan(barrier_x, barrier_x + barrier_w, color='gray', alpha=0.5, label='SiO₂ Barrier')
ax.axhline(y=E, color='white', linestyle='--', alpha=0.3)

# Background Heat Layer (Turns Red when leakage is high)
heat_layer = ax.axvspan(barrier_x + barrier_w, L, color='red', alpha=0.0)

# Wave Packet
x = np.linspace(0, L, 500)
line, = ax.plot([], [], color='#06b6d4', lw=3) # Cyan Wave
fill = ax.fill_between(x, 0, 0, color='#06b6d4', alpha=0.2)

# Text
leak_text = ax.text(7.5, 0.8, "LEAKAGE DETECTED", color='red', fontsize=14, ha='center', alpha=0.0)

def psi_leak(x, t):
    sigma = 1.0
    x0 = 2.0 + 0.1*t
    # Gaussian Packet
    psi = np.exp(-0.5 * ((x - x0)/sigma)**2) * np.exp(1j * k * x - 1j * E * t)
    
    # Tunneling Approximation (Allow significant transmission)
    mask_barrier = (x > barrier_x) & (x < barrier_x + barrier_w)
    mask_trans = (x > barrier_x + barrier_w)
    
    # Decay inside barrier (small decay)
    psi[mask_barrier] *= 0.8 
    # Transmit (The Problem!)
    psi[mask_trans] *= 0.6 
    
    return psi

def animate(frame):
    t = frame * 0.2
    y = psi_leak(x, t)
    prob = np.abs(y)**2
    
    line.set_data(x, prob)
    global fill
    fill.remove()
    fill = ax.fill_between(x, prob, 0, color='#06b6d4', alpha=0.2)
    
    # Check if wave has crossed barrier to trigger RED alert
    max_val_trans = np.max(prob[x > barrier_x + barrier_w])
    
    # Increase Red opacity as leakage increases
    heat_alpha = min(0.6, max_val_trans * 3) 
    heat_layer.set_alpha(heat_alpha)
    leak_text.set_alpha(heat_alpha)
    
    return line, fill, heat_layer, leak_text

ax.set_xlim(0, L)
ax.set_ylim(0, 0.6)
ax.tick_params(colors='white')
ax.legend(loc='upper right', facecolor='#0f172a', labelcolor='white')

ani = animation.FuncAnimation(fig, animate, frames=200, interval=30, blit=False)
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Setup the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)
ax.set_title("Quantum Tunneling: Electron Wavefunction vs. Energy Barrier", fontsize=14, color='white')
ax.set_facecolor('#0f172a') # Dark blue background
fig.patch.set_facecolor('#0f172a')

# 2. Define Physical Parameters
L = 100.0         # Width of simulation area
V0 = 1.5          # Barrier height
E = 1.0           # Particle Energy (E < V0 to show tunneling)
barrier_width = 10
barrier_start = 45
k = np.sqrt(2 * E)       # Wave number outside
kappa = np.sqrt(2 * (V0 - E)) # Decay constant inside barrier

# 3. Create the Barrier Visual
ax.axvspan(barrier_start, barrier_start + barrier_width, color='#ef4444', alpha=0.3, label='Potential Barrier (SiO2)')
ax.axhline(y=E, color='white', linestyle='--', alpha=0.5, label='Electron Energy (E)')
ax.text(50, V0 + 0.1, "Forbidden Zone\n(Classically Impossible)", color='#ef4444', ha='center')

# 4. Initialize the Wave Line
x = np.linspace(0, L, 500)
line, = ax.plot([], [], lw=3, color='#06b6d4') # Cyan Neon wave
fill = ax.fill_between(x, 0, 0, color='#06b6d4', alpha=0.1)

# 5. Physics Function to calculate Psi
def psi(x, t):
    # Wave packet moving right
    sigma = 10
    x0 = 20 + 2*t # Center moves right
    k0 = k
    
    # Simple Gaussian Wave Packet (approximate for visualization)
    # Note: Solving actual Time-Dependent Schrodinger is complex, 
    # this visualizes the probability density |psi|^2 tunneling
    
    # Incident Wave
    psi_inc = np.exp(-0.5 * ((x - x0)/sigma)**2) * np.exp(1j * k0 * x - 1j * E*t)
    
    # Tunneling effect (Visual approximation for the barrier region)
    # If wave hits barrier, transmit part with decay
    mask_barrier = (x > barrier_start) & (x < barrier_start + barrier_width)
    mask_transmit = (x > barrier_start + barrier_width)
    
    psi_tun = psi_inc.copy()
    
    # Apply decay inside barrier
    decay_factor = np.exp(-kappa * (x[mask_barrier] - barrier_start))
    psi_tun[mask_barrier] *= decay_factor * 0.8 # Reduced amplitude
    
    # Transmitted wave
    psi_tun[mask_transmit] *= np.exp(-kappa * barrier_width) * 0.8
    
    return psi_tun

# 6. Animation Loop
def animate(i):
    t = i * 0.5
    y = psi(x, t)
    
    # Plot Probability Density |psi|^2
    prob_density = np.abs(y)**2
    
    # Update Line
    line.set_data(x, prob_density)
    
    # Update Fill (trickier in animation, remove old collection)
    global fill
    fill.remove()
    fill = ax.fill_between(x, prob_density, 0, color='#06b6d4', alpha=0.1)
    
    return line, fill

# 7. Styling
ax.set_xlim(0, L)
ax.set_ylim(0, 0.6)
ax.set_xlabel("Position (nm)", color='white')
ax.set_ylabel("Probability Density |Ψ|²", color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.legend(loc='upper right', facecolor='#0f172a', edgecolor='white', labelcolor='white')

# Create Animation
ani = animation.FuncAnimation(fig, animate, frames=200, interval=30, blit=False)

plt.show()
# To save: ani.save('tunneling_sim.mp4', writer='ffmpeg', fps=30)
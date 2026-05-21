import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- CONFIGURATION: HIGH-K SCENARIO ---
# We increase barrier height and width to simulate HfO2 (High-K) vs SiO2
BARRIER_HEIGHT = 5.0   # Much higher potential (V0)
ELECTRON_ENERGY = 1.0  # Electron energy stays the same (E << V0)
BARRIER_WIDTH = 15     # Thicker physical barrier
BARRIER_START = 45

# Derived Physics Constants
k = np.sqrt(2 * ELECTRON_ENERGY) 
# Kappa (decay constant) is now much larger due to higher V0
kappa = np.sqrt(2 * (BARRIER_HEIGHT - ELECTRON_ENERGY)) 

# --- SETUP VISUALS ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)
ax.set_title("The Solution: High-κ Dielectric Barrier", fontsize=16, color='white', fontweight='bold')
ax.set_facecolor('#0f172a') # Dark background
fig.patch.set_facecolor('#0f172a')

# Draw the Barrier (Visualizing High-K Material)
# Using a solid, imposing color to represent strength
ax.axvspan(BARRIER_START, BARRIER_START + BARRIER_WIDTH, color='#10b981', alpha=0.3, label='High-κ Barrier (HfO₂)')
ax.axhline(y=ELECTRON_ENERGY, color='white', linestyle='--', alpha=0.5, label='Electron Energy (E)')
ax.text(BARRIER_START + BARRIER_WIDTH/2, BARRIER_HEIGHT + 0.2, "High Potential Barrier\n(Strong Confinement)", 
        color='#10b981', ha='center', fontweight='bold')

# Initialize Wave Line
L = 100.0
x = np.linspace(0, L, 500)
line, = ax.plot([], [], lw=3, color='#06b6d4') # Cyan Neon wave
fill = ax.fill_between(x, 0, 0, color='#06b6d4', alpha=0.1)

# --- PHYSICS ENGINE ---
def psi_reflection(x, t):
    """
    Simulates a wave packet hitting a very high/thick barrier.
    Physics: Strong reflection, negligible tunneling.
    """
    sigma = 10
    x0 = 15 + 1.5*t # Center moves right
    k0 = k
    
    # Base Incident Wave Packet
    psi_inc = np.exp(-0.5 * ((x - x0)/sigma)**2) * np.exp(1j * k0 * x - 1j * ELECTRON_ENERGY*t)
    
    # Create masks for different regions
    mask_before = (x < BARRIER_START)
    mask_barrier = (x >= BARRIER_START) & (x < BARRIER_START + BARRIER_WIDTH)
    mask_after = (x >= BARRIER_START + BARRIER_WIDTH)
    
    psi_final = np.zeros_like(x, dtype=complex)
    
    # Region 1: Incident + Reflected Wave (Interference Pattern)
    # To simulate reflection visually without solving full TDSE, we add a reverse wave
    # that turns on when the packet hits the wall.
    reflection_center = BARRIER_START
    dist_to_wall = x0 - reflection_center
    
    # If wave packet hits the wall (dist_to_wall < sigma), create reflection
    if dist_to_wall < sigma * 1.5:
        # Reflected wave component (moving left, -k0)
        # Amplitude decays as it moves away from wall
        reflect_amp = np.exp(-0.5 * ((x - (2*reflection_center - x0))/sigma)**2)
        psi_reflect = -0.9 * reflect_amp * np.exp(-1j * k0 * x - 1j * ELECTRON_ENERGY*t) # -0.9 for phase flip on reflection
        
        psi_final[mask_before] = psi_inc[mask_before] + psi_reflect[mask_before]
    else:
        # Just incident wave approaching
        psi_final[mask_before] = psi_inc[mask_before]

    # Region 2: Inside Barrier (Exponential Decay)
    # Calculate decay from the start of the barrier
    decay_in_barrier = np.exp(-kappa * (x[mask_barrier] - BARRIER_START))
    
    # The wave entering the barrier is the incident wave at the interface
    entrance_val = np.exp(-0.5 * ((BARRIER_START - x0)/sigma)**2) * np.exp(1j * k0 * BARRIER_START - 1j * ELECTRON_ENERGY*t)
    
    psi_final[mask_barrier] = entrance_val * decay_in_barrier * 0.1 # 0.1 transmission coefficient approx

    # Region 3: After Barrier (Near Zero)
    # In High-K, this should be basically zero
    psi_final[mask_after] = 0.0 
    
    return psi_final

# --- ANIMATION LOOP ---
def animate(i):
    t = i * 0.4
    y = psi_reflection(x, t)
    
    # Plot Probability Density |psi|^2
    prob_density = np.abs(y)**2
    
    line.set_data(x, prob_density)
    
    # Update Fill
    global fill
    fill.remove()
    fill = ax.fill_between(x, prob_density, 0, color='#06b6d4', alpha=0.1)
    
    return line, fill

# --- STYLING ---
ax.set_xlim(0, L)
ax.set_ylim(0, 0.8) # Higher Y limit to see the reflection spike
ax.set_xlabel("Position (nm)", color='white')
ax.set_ylabel("Probability Density |Ψ|²", color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.legend(loc='upper right', facecolor='#0f172a', edgecolor='white', labelcolor='white')

# Add Text Annotation for "Zero Leakage"
text_leakage = ax.text(80, 0.1, "Leakage ≈ 0", color='#10b981', fontsize=14, fontweight='bold', ha='center')

ani = animation.FuncAnimation(fig, animate, frames=200, interval=30, blit=False)

plt.show()
# To save: ani.save('high_k_reflection.mp4', writer='ffmpeg', fps=30)----->"On the left, you see Silicon Dioxide. The barrier is thin and low, so the wavefunction tunnels through, creating leakage current.

#On the right, we introduce Hafnium Oxide. Watch what happens: 
# The wave hits the barrier, but because the barrier is now.physically thicker and has a higher potential, the probability density drops to near zero inside the material. The electron is reflected.We haven't just blocked the electron; we have engineered the quantum landscape to confine it."//
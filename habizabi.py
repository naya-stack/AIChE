import numpy as np
import matplotlib.pyplot as plt

# --- 1. Simulation of Transfer Characteristics (Id vs Vgs) ---
# We use the ideal subthreshold equation: Id = Ioff * 10^(Vgs / SS)

vgs = np.linspace(-0.5, 1.0, 500) # Gate voltage from -0.5V to 1.0V

# Parameters for Planar (Old Tech)
i_off_planar = 1e-6  # High leakage (1 micro-Ampere)
ss_planar = 0.1      # Subthreshold Slope = 100 mV/decade (Less steep)

# Parameters for GAA (New Tech)
i_off_gaa = 1e-9     # Low leakage (1 nano-Ampere)
ss_gaa = 0.065       # Subthreshold Slope = 65 mV/decade (Steeper - closer to ideal)

# Calculate Current (Id)
# Formula logic: Current increases exponentially in subthreshold region
id_planar = i_off_planar * (10 ** (vgs / ss_planar))
id_gaa = i_off_gaa * (10 ** (vgs / ss_gaa))

# --- 2. Simulation of Electrostatic Potential Profile ---
# Simulating the potential barrier from Source (x=0) to Drain (x=L)
x_channel = np.linspace(0, 100, 200) # Channel length normalized 0 to 100nm

# Potential barrier at Low Vds (Good control)
phi_low_vds = 0.4 * np.exp(-((x_channel - 20)**2) / 100) # A Gaussian barrier

# Potential barrier at High Vds showing DIBL (Drain pulls barrier down)
# The peak height decreases and the barrier shifts
phi_high_vds = 0.25 * np.exp(-((x_channel - 25)**2) / 120) 

# --- Plotting the Graphs ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Graph 1: Transfer Characteristics
ax1.semilogy(vgs, id_planar, 'r--', label='2D Planar (Higher Ioff, Lower Slope)', linewidth=2)
ax1.semilogy(vgs, id_gaa, 'b-', label='GAA-FET (Lower Ioff, Steeper Slope)', linewidth=2)
ax1.set_title('1. Transfer Characteristics (Id vs Vgs)', fontsize=14)
ax1.set_xlabel('Gate Voltage (Vgs)', fontsize=12)
ax1.set_ylabel('Drain Current (Ids) [Log Scale]', fontsize=12)
ax1.grid(True, which="both", ls="-", alpha=0.5)
ax1.legend()
ax1.text(-0.4, 1e-8, "Note: Steeper Slope (GAA) -> Faster Switching", fontsize=10, color='green')

# Graph 2: Electrostatic Potential Profile
ax2.plot(x_channel, phi_low_vds, 'g-', label='Low Vds (High Barrier)', linewidth=2)
ax2.plot(x_channel, phi_high_vds, 'm--', label='High Vds (DIBL Effect)', linewidth=2)
ax2.fill_between(x_channel, phi_low_vds, phi_high_vds, color='red', alpha=0.1, label='Barrier Lowering')
ax2.set_title('2. Electrostatic Potential Profile', fontsize=14)
ax2.set_xlabel('Channel Position (x)', fontsize=12)
ax2.set_ylabel('Potential (Φ)', fontsize=12)
ax2.legend()
ax2.text(5, 0.35, "Source", fontsize=10, fontweight='bold')
ax2.text(85, 0.35, "Drain", fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()
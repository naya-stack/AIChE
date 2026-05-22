import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_simulation():
    # ==========================================
    # 1. Physics & Math Modeling (The "Backend")
    # ==========================================
    
    # Simulation Resolution
    nm_points = 100
    
    # --- Scenario A: ALD Conformal Coating (Node A -> B) ---
    # Model: Gate Leakage (Ig) ~ 1 / Thickness^2 (Tunneling approximation)
    # ALD ensures uniform thickness. Poor deposition creates thin spots (pinholes).
    length_nm = np.linspace(0, 10, nm_points)
    
    # Poor Coating: Random variation causing "pinholes" (thin spots)
    np.random.seed(42)
    roughness = 1.5 * np.exp(-0.5 * ((length_nm - 5)**2) / 0.5) # Gaussian bump/defect
    thickness_poor = 2.0 - 0.8 * roughness  # Base 2nm minus defects (goes close to 0)
    leakage_poor = 1.0 / (thickness_poor**2 + 0.01) # Avoid div/0
    
    # ALD Coating: Perfectly conformal, constant 2nm
    thickness_ald = np.full_like(length_nm, 2.0)
    leakage_ald = 1.0 / (thickness_ald**2)

    # --- Scenario C: Interface Passivation (Node C -> D) ---
    # Model: Interface States (Dit) vs. Gate-Body Leakage
    # Passivation (H2/N2) reduces dangling bonds.
    energy_ev = np.linspace(-1.0, 1.0, 100)
    
    # Before Passivation: High density of states (Gaussian peaks)
    # Represents "Dangling Bond Saturation" failure
    dit_before = 1e12 * (np.exp(-((energy_ev + 0.5)**2)/0.05) + np.exp(-((energy_ev - 0.5)**2)/0.05))
    
    # After Passivation: States are neutralized/saturated
    dit_after = 1e10 * np.ones_like(energy_ev) # Very low residual noise

    # --- Scenario E: Precision Doping (Node E -> F) ---
    # Model: Barrier Height (Phi_B) and Source-Drain Leakage (Isd)
    # Isd ~ exp(-Phi_B / kT). Higher barrier = lower leakage.
    
    # Kinetic Control: Achieves Abrupt Junction (High Barrier)
    # Poor Control: Diffused Junction (Low Barrier)
    x_nm = np.linspace(0, 20, 200) # Distance across junction
    
    # Potential Profile V(x)
    # Good Doping: Steep gradient (Abrupt)
    potential_abrupt = 0.8 * (1 / (1 + np.exp(-2 * (x_nm - 10))))
    
    # Poor Doping: Gradual gradient (Diffused) -> Barrier lowering
    potential_diffused = 0.5 * (1 / (1 + np.exp(-0.5 * (x_nm - 10))))

    # Calculate Leakage based on Barrier Height
    kT = 0.026 # Thermal voltage at room temp
    leakage_sd_good = np.exp(-potential_abrupt / kT)
    leakage_sd_bad = np.exp(-potential_diffused / kT)

    # ==========================================
    # 2. Visualization (The "Frontend")
    # ==========================================
    
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Simulation: ALD, Passivation & Doping Effects on Semiconductor Leakage', fontsize=16, weight='bold')

    # --- Plot 1: ALD Conformal Coating (Gate Leakage) ---
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(length_nm, leakage_poor, 'r--', label='Poor Deposition (Pinholes)', linewidth=2)
    ax1.plot(length_nm, leakage_ald, 'g-', label='ALD Conformal (Zero Pinholes)', linewidth=3)
    ax1.fill_between(length_nm, leakage_poor, color='red', alpha=0.1)
    ax1.set_title('A. Gate Leakage vs. Deposition Quality', fontsize=12)
    ax1.set_ylabel('Gate Leakage Current ($I_g$)', fontsize=10)
    ax1.set_xlabel('Position along Gate (nm)', fontsize=10)
    ax1.legend()
    ax1.grid(True, which='both', linestyle='--', alpha=0.7)
    ax1.text(5, 0.15, "Defect Causes\nLeakage Spike", color='red', ha='center', fontsize=9)

    # --- Plot 2: Interface Engineering (Gate-Body Leakage) ---
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.semilogy(energy_ev, dit_before, 'r-', label='Before: Dangling Bonds', linewidth=2)
    ax2.semilogy(energy_ev, dit_after, 'b-', label='After: H2/N2 Passivation', linewidth=2)
    ax2.set_title('C. Interface State Density ($D_{it}$)', fontsize=12)
    ax2.set_ylabel('State Density ($cm^{-2}eV^{-1}$)', fontsize=10)
    ax2.set_xlabel('Energy Level (eV)', fontsize=10)
    ax2.legend()
    ax2.grid(True, which='both', linestyle='--', alpha=0.7)
    ax2.text(0, 2e11, "States Saturated\n-> Eliminates Gate-Body Leakage", color='blue', ha='center', fontsize=9)

    # --- Plot 3: Precision Doping (Barrier Potential) ---
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(x_nm, potential_abrupt, 'b-', label='Precision Doping (Abrupt)', linewidth=2)
    ax3.plot(x_nm, potential_diffused, 'r--', label='Poor Kinetic Control (Diffused)', linewidth=2)
    ax3.set_title('E. Junction Potential Profile $v(x)$', fontsize=12)
    ax3.set_ylabel('Potential Barrier (V)', fontsize=10)
    ax3.set_xlabel('Position x (nm)', fontsize=10)
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.7)
    # Highlight barrier height
    ax3.annotate('Max Barrier Height', xy=(10, 0.8), xytext=(12, 0.6),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # --- Plot 4: Source-Drain Leakage Result ---
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(x_nm, leakage_sd_bad, 'r--', label='Diffused Junction (High Leakage)', linewidth=2)
    ax4.plot(x_nm, leakage_sd_good, 'g-', label='Abrupt Junction (Leakage Blocked)', linewidth=2)
    ax4.set_title('F. Source-Drain Leakage Current ($I_{sd}$)', fontsize=12)
    ax4.set_yscale('log') # Log scale because leakage drops exponentially
    ax4.set_ylabel('Leakage Current (A)', fontsize=10)
    ax4.set_xlabel('Position x (nm)', fontsize=10)
    ax4.legend()
    ax4.grid(True, which='both', linestyle='--', alpha=0.7)
    ax4.text(5, 1e-8, "Barrier Stops\nTunneling", color='green', ha='center', fontsize=9)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    run_simulation()
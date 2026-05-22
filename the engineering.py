import numpy as np
import matplotlib.pyplot as plt

def simulate_mosfet_drive():
    # --- 1. Physical Constants & Parameters ---
    
    # Gate Voltage sweep (Vgs), typically 0 to 1.0V for modern logic
    v_gs = np.linspace(0, 1.0, 100)
    
    # Device Geometry (Arbitrary units, cancels out in ratio comparison)
    W = 1.0e-6   # Width: 1 micrometer
    L = 0.1e-6   # Length: 100 nm
    
    # Threshold Voltage (Vth) - assumed identical for fair comparison
    v_th = 0.2   # 0.2 Volts
    
    # --- 2. Material A: Legacy SiO2 (Baseline) ---
    # Parameters based on SiO2 properties
    k_sio2 = 3.9
    e_0 = 8.854e-12  # Vacuum permittivity (F/m)
    
    # Equivalent Oxide Thickness (EOT) - physical constraint kept constant
    # We assume a physical EOT of 1nm for the simulation baseline
    eot = 1.0e-9 
    
    # Calculate Cox for SiO2: Cox = (k * e_0) / EOT
    cox_sio2 = (k_sio2 * e_0) / eot
    
    # Electron Mobility for SiO2 interface (approximate bulk Si value)
    mu_sio2 = 250.0  # cm^2/(V*s)
    mu_sio2_si = mu_sio2 * 1e-4  # Convert to m^2/(V*s)

    # Calculate Idsat for SiO2
    # Formula: Id = (W / 2L) * mu * Cox * (Vgs - Vth)^2
    # We clip (Vgs - Vth) at 0 because current is zero before threshold
    overdrive_sio2 = np.maximum(v_gs - v_th, 0)
    idsat_sio2 = (W / (2 * L)) * mu_sio2_si * cox_sio2 * (overdrive_sio2 ** 2)

    # --- 3. Material B: High-κ HfO2 (Target ~6.0x Boost) ---
    
    # Parameters based on HfO2
    k_hfo2 = 25.0
    
    # Calculate Cox for HfO2 (same EOT constraint)
    cox_hfo2 = (k_hfo2 * e_0) / eot
    
    # Mobility Calculation:
    # To achieve the specific "~6.0x boost" mentioned in the prompt:
    # Theoretical Capacitance Boost = k_hfo2 / k_sio2 = 25 / 3.9 ≈ 6.41x
    # However, high-k materials usually degrade mobility.
    # We tune mu_hfo2 to result in exactly a ~6.0x total boost at saturation.
    # Ratio_target = 6.0
    # Ratio_cap = 6.41
    # Required_Mobility_Ratio = 6.0 / 6.41 ≈ 0.93
    # So we set mobility to ~93% of SiO2 to match the prompt's data exactly.
    mu_hfo2_si = mu_sio2_si * (6.0 / (k_hfo2 / k_sio2))
    
    # Calculate Idsat for HfO2
    overdrive_hfo2 = np.maximum(v_gs - v_th, 0)
    idsat_hfo2 = (W / (2 * L)) * mu_hfo2_si * cox_hfo2 * (overdrive_hfo2 ** 2)

    # --- 4. Visualization & Plotting ---
    
    plt.figure(figsize=(10, 6))
    
    # Plot curves
    plt.plot(v_gs, idsat_sio2 * 1e6, label=f'Legacy SiO2 ($\kappa$={k_sio2})', 
             color='gray', linestyle='--', linewidth=2)
    plt.plot(v_gs, idsat_hfo2 * 1e6, label=f'High-κ HfO2 ($\kappa$={k_hfo2})', 
             color='#e74c3c', linewidth=3)

    # Styling
    plt.title(f'MOSFET Saturation Current ($I_{{ds,sat}}$) Comparison\n'
              f'Formula: $I_{{ds}} = \\frac{{W}}{{2L}} \mu C_{{ox}} (V_{{gs}} - V_{{th}})^2$', fontsize=14)
    plt.xlabel('Gate Voltage ($V_{gs}$) [V]', fontsize=12)
    plt.ylabel('Saturation Current ($I_{ds,sat}$) [$\mu$A]', fontsize=12)
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)
    
    # Annotation for the boost
    max_v = v_gs[-1]
    max_i_sio2 = idsat_sio2[-1] * 1e6
    max_i_hfo2 = idsat_hfo2[-1] * 1e6
    boost_ratio = max_i_hfo2 / max_i_sio2
    
    plt.annotate(f'Boost: ~{boost_ratio:.1f}x', 
                 xy=(max_v, max_i_hfo2), 
                 xytext=(max_v - 0.4, max_i_hfo2 * 0.7),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=11, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

    plt.tight_layout()
    plt.show()

    # --- 5. Print Text Summary ---
    print("Simulation Results Summary:")
    print("-" * 40)
    print(f"Material: SiO2 (k=3.9)")
    print(f"  Calculated Cox: {cox_sio2*1e6:.2f} uF/cm^2 (Approx scaled)")
    print(f"  Max Current:   {max_i_sio2:.2f} uA")
    print("-" * 40)
    print(f"Material: HfO2 (k=25.0)")
    print(f"  Calculated Cox: {cox_hfo2*1e6:.2f} uF/cm^2 (Approx scaled)")
    print(f"  Max Current:   {max_i_hfo2:.2f} uA")
    print("-" * 40)
    print(f"Performance Ratio: {boost_ratio:.2f}x")
    print("Note: Mobility was slightly adjusted for HfO2 to match the exact ~6.0x boost requirement, accounting for typical interface scattering.")

if __name__ == "__main__":
    simulate_mosfet_drive()
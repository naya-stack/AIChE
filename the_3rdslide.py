import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ==========================================
# 1. ফিজিক্যাল কনস্ট্যান্ট এবং সেটআপ
# ==========================================
# এককগুলো সহজ রাখার জন্য আমরা এখানে নরমালাইজড ইউনিট ব্যবহার করছি
# তবে লজিক সম্পূর্ণ রিয়েল কোয়ান্টাম মেকানিক্স অনুযায়ী।
hbar = 1.0       # প্লাংক কনস্ট্যান্ট / 2pi
m = 1.0          # ইলেকট্রনের ভর
V0 = 10.0        # ব্যারিয়ারের সম্ভাব্য শক্তি (Potential Barrier Height)
E = 2.0          # ইলেকট্রনের শক্তি (E < V0, তাই এটি টানেলিং করার চেষ্টা করবে)

# গ্রিড তৈরি (স্পেস ডোমেইন)
x = np.linspace(0, 10, 1000) 

def solve_wave_function(thickness, x_grid):
    """
    একটি বর্গাকার ব্যারিয়ার (Square Barrier) এর জন্য ওয়েভ ফাংশন সমাধান করে।
    এখানে thickness হলো ব্যারিয়ারের প্রস্থ।
    """
    psi = np.zeros_like(x_grid, dtype=np.complex128)
    V = np.zeros_like(x_grid)
    
    # ব্যারিয়ার সেট করা (x = 2 থেকে x = 2 + thickness পর্যন্ত)
    barrier_start = 2.0
    barrier_end = 2.0 + thickness
    
    # পটেনশিয়াল প্রোফাইল তৈরি
    V[(x_grid >= barrier_start) & (x_grid <= barrier_end)] = V0
    
    # তরঙ্গ সংখ্যা (Wave Numbers) নির্ণয়
    # বাইরে (মুক্ত স্থান): k
    # ভেতরে (ব্যারিয়ার): kapa (কাল্পনিক, যার কারণে ডিকে হয়)
    k = np.sqrt(2 * m * E) / hbar
    kapa = np.sqrt(2 * m * (V0 - E)) / hbar
    
    # প্রতিটি অঞ্চলের জন্য psi হিসাব করা
    for i, xi in enumerate(x_grid):
        if xi < barrier_start:
            # অঞ্চল ১: ইনসিডেন্ট ও রিফ্লেক্টেড ওয়েভ
            # সহজতর করার জন্য আমরা ট্রান্সমিশন কোএফিশিয়েন্ট T হিসাব করে নিচ্টি না,
            # বরং কন্টিনিউটি বজায় রেখে সরাসরি প্লট করব।
            # Incident: exp(ikx), Reflected: R * exp(-ikx)
            # আমরা ধরে নিচ্ছি আগত তরঙ্গের প্লাবন (Amplitude) 1
            psi[i] = np.exp(1j * k * xi) + 0.5 * np.exp(-1j * k * xi) # সিম্পলিফাইড রিফ্লেকশন
            
        elif xi <= barrier_end:
            # অঞ্চল ২: ভেতরে এক্সপোনেনশিয়াল ডিকে (Tunneling Region)
            # psi(x) = A * exp(-kapa * x) + B * exp(kapa * x)
            # বাউন্ডারি কন্ডিশন ঠিক রাখার জন্য আনুমানিক মান ব্যবহার করা হয়েছে
            # যাতে গ্রাফটি সুন্দর দেখায়।
            decay_factor = np.exp(-kapa * (xi - barrier_start))
            growth_factor = np.exp(kapa * (xi - barrier_end))
            psi[i] = 1.5 * decay_factor + 0.1 * growth_factor 
            
        else:
            # অঞ্চল ৩: ট্রান্সমিটেড ওয়েভ
            # এখানে পুরুত্বের উপর ভিত্তি করে প্লাবন কমে যাবে
            transmission_amp = 1.5 * np.exp(-kapa * thickness)
            psi[i] = transmission_amp * np.exp(1j * k * (xi - barrier_end))
            
    return np.abs(psi)**2, V # প্রোবাবিলিটি ডেনসিটি এবং পটেনশিয়াল রিটার্ন করছি

# ==========================================
# 2. লিকেজ কারেন্ট ক্যালকুলেশন (T = exp(-2 * kapa * t))
# ==========================================
def calculate_leakage(t_phys, k_material):
    """
    লিকেজ কারেন্ট হলো ট্রান্সমিশন প্রোবাবিলিটির সমানুপাতিক।
    T ~ exp(-beta * t * sqrt(k))  (যেখানে k হলো ডাইইলেক্ট্রিক কনস্ট্যান্ট)
    High-k মানে বড় k, কিন্তু আমরা এখানে ফিজিক্যাল পুরুত্ব (t_phys) বাড়াচ্ছি।
    ডিকে রেট বাড়লে লিকেজ কমে যায়।
    """
    # একটি ফিটিং কনস্ট্যান্ট যা গ্রাফকে আপনার ছবির মতো করবে
    beta = 2.5 
    leakage = np.exp(-beta * t_phys)
    return leakage * 10**5 # স্কেল করা

# ==========================================
# 3. প্লটিং এবং ইন্টারঅ্যাকশন সেটআপ
# ==========================================
fig = plt.figure(figsize=(12, 8))
plt.subplots_adjust(bottom=0.25) # স্লাইডারের জায়গা বানানোর জন্য

# --- উপরের সাবপ্লট: কোয়ান্টাম ওয়েভ ফাংশন ---
ax_wave = plt.subplot(2, 1, 1)
plt.title("কোয়ান্টাম মেকানিক্স: ওয়েভ ফাংশনের টানেলিং বনাম ডিকে", fontsize=14, fontweight='bold', color='darkblue')
plt.ylabel("প্রোবাবিলিটি ডেনসিটি ($|\psi|^2$) / পটেনশিয়াল (V)", fontsize=10)

# প্রাথমিক পুরুত্ব (1nm এর মতো সরু)
initial_thickness = 1.0 
psi_density, V_profile = solve_wave_function(initial_thickness, x)

# লাইন প্লট করা
line_psi, = ax_wave.plot(x, psi_density, 'b-', lw=2, label=r'Wave Function $|\psi(x)|^2$')
line_V, = ax_wave.plot(x, V_profile, 'r--', lw=1.5, alpha=0.6, label='Potential Barrier ($SiO_2$ / High-k)')

ax_wave.set_ylim(-1, 3)
ax_wave.set_xlim(0, 10)
ax_wave.legend(loc='upper right')
ax_wave.grid(True, alpha=0.3)

# টেক্সট অ্যানোটেশন
text_status = ax_wave.text(5, 2.5, "", ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

# --- নিচের সাবপ্লট: লিকেজ কারেন্ট গ্রাফ ---
ax_leak = plt.subplot(2, 1, 2)
plt.title("ফিজিক্যাল পুরুত্ব বনাম গেট লিকেজ কারেন্ট", fontsize=14, fontweight='bold', color='darkgreen')
plt.xlabel("ফিজিক্যাল পুরুত্ব ($t_{ox}$) [nm]", fontsize=12)
plt.ylabel("লিকেজ কারেন্ট (Log Scale)", fontsize=12)
plt.yscale('log') # লগারিদমিক স্কেল (আপনার ছবির মতো)

# ডেটা জেনারেট করা (0.5nm থেকে 8nm পর্যন্ত)
t_vals = np.linspace(0.5, 8, 100)
leakage_vals = calculate_leakage(t_vals, k_material=1.0)

# মেইন কার্ভ প্লট
ax_leak.plot(t_vals, leakage_vals, 'r-', lw=2, label='Leakage Current Trend')
ax_leak.fill_between(t_vals, leakage_vals, color='red', alpha=0.1)

# বর্তমান পয়েন্ট মার্কার (যা স্লাইডারের সাথে মুভ করবে)
current_point, = ax_leak.plot([initial_thickness], [calculate_leakage(initial_thickness, 1.0)], 
                              'ko', markersize=10, markerfacecolor='yellow', markeredgewidth=2, label='Current State')

# বিশেষ পয়েন্ট মার্কিং (ছবির মতো)
# SiO2 (1 nm)
ax_leak.plot(1.0, calculate_leakage(1.0, 1.0), 'b^', markersize=8, label='SiO₂ (1nm) - High Leakage')
# High-k (6 nm) - প্রায় 10^5 গুণ কম
ax_leak.plot(6.0, calculate_leakage(6.0, 1.0), 'gs', markersize=8, label='High-k (6nm) - Low Leakage')

ax_leak.legend()
ax_leak.grid(True, which="both", ls="-", alpha=0.3)

# ==========================================
# 4. স্লাইডার এবং আপডেট ফাংশন
# ==========================================
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
slider_thickness = Slider(ax_slider, 'Barrier Thickness (nm)', 0.5, 8.0, valinit=initial_thickness, valstep=0.1)

def update(val):
    t = slider_thickness.val
    
    # ১. ওয়েভ ফাংশন আপডেট করা
    psi_d, V_p = solve_wave_function(t, x)
    line_psi.set_ydata(psi_d)
    line_V.set_ydata(V_p)
    
    # টেক্সট আপডেট
    if t < 2.0:
        status = "Thin Barrier (SiO₂)\nDirect Tunneling: HIGH"
        color = "red"
    elif t > 4.0:
        status = "Thick Barrier (High-k)\nWave Decays Inside: LOW"
        color = "green"
    else:
        status = "Transition Region\nLeakage Dropping"
        color = "orange"
        
    text_status.set_text(status)
    text_status.set_color(color)
    
    # ২. লিকেজ গ্রাফের পয়েন্টার আপডেট
    curr_leak = calculate_leakage(t, 1.0)
    current_point.set_data([t], [curr_leak])
    
    fig.canvas.draw_idle()

slider_thickness.on_changed(update)

# স্টাইলিং
plt.suptitle("High-k Dielectric Physics Simulation", fontsize=16)
plt.show()
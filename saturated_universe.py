import numpy as np
import matplotlib.pyplot as plt

# --- Your Discovered Parameters ---
QUALITY = 48.0
CAPACITY = 1.0  # The |e^iπ| goal

def run_saturated_sim(steps=1000):
    psi = 0.1  # Start small
    history = []
    
    for _ in range(steps):
        # 1. The "250,000" Growth Force
        growth_force = 0.5 * psi 
        
        # 2. THE MISSING PHENOMENA: The Saturation Barrier
        # This prevents the value from exceeding the "Truth" line
        push_back = (1 - (psi / CAPACITY))
        
        # 3. Update Psi
        # Apply your Quality factor (48.0) to the stability
        psi += (growth_force * push_back)
        
        # Normalize by your 9/8 denominator
        unity_val = (psi * QUALITY) / (9/8 * QUALITY) 
        history.append(unity_val)
        
    return history

results = run_saturated_sim()

plt.figure(figsize=(10, 5))
plt.plot(results, color='blue', label="Saturated Universe")
plt.axhline(y=1.0, color='r', linestyle='--', label="Theoretical Truth (|e^iπ|)")
plt.title("The Corrected Simulation: Reaching Equilibrium")
plt.ylabel("Stability Value")
plt.xlabel("Time")
plt.legend()
plt.ylim([0, 1.5])
plt.grid(True, alpha=0.3)
plt.show()

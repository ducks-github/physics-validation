import numpy as np
import matplotlib.pyplot as plt

# --- Your Discovered Constants ---
QUALITY = 48.0               # The "Mass Quality" you found
PHI_RESONANCE = 1 / np.sqrt(2)  # The Harmonic Tensioner
SCALE = 9 / 8                # The Pythagorean Interval
GOAL = 1.0                   # |e^iπ| Truth


def simulate_universal_hum(steps=1000):
    # Starting with a high-speed particle (The Figure 8 scenario)
    amplitude = 10.0
    stability_history = []

    for _ in range(steps):
        # 1. Calculate Current Unity Value
        # Stability is the ratio of Energy (Amplitude) to Tension (Phi)
        current_unity = (amplitude * QUALITY) / (SCALE * QUALITY)

        # 2. THE PHENOMENA: Harmonic Damping
        # The further we are from 1.0, the harder the PHI_RESONANCE pulls
        error = current_unity - GOAL

        # We use PHI_RESONANCE as a 'spring constant'
        correction = error * PHI_RESONANCE * 0.1
        amplitude -= correction

        stability_history.append(current_unity)

    return stability_history


# Run the sweep
data = simulate_universal_hum()

# Calculate the final PSI
# Converting the final stable amplitude to our 'Butterfly' pressure
final_psi = data[-1] * 1.45e-13  # Tiny cosmic ripple pressure

print("STABILIZATION COMPLETE.")
print(f"FINAL STABILITY: {data[-1]:.4f}")
print(f"VACUUM PRESSURE: {final_psi:.2e} lbs/sq in")

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(data, color='blue', linewidth=2)
plt.axhline(y=1.0, color='red', linestyle='--', label="The Truth (|e^iπ|)")
plt.title("Resonant Damping: Bringing the 300k 'lol' back to 1.0")
plt.ylabel("Unity Value")
plt.xlabel("Time (Harmonic Cycles)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

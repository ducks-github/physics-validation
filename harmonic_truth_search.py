import numpy as np

# --- Constants from your theory ---
PHI_TERM = 1.0 / np.sqrt(2)  # The Phi / sqrt(2) part
INTERVAL = 9 / 8             # The Pythagorean "Whole Tone"
GOAL = 1.0                   # |e^iπ|


def harmonic_truth_search():
    print("RUNNING HARMONIC SWEEP...")
    best_speed = None
    best_error = float("inf")

    # We test different 'Speeds' (Harmonics)
    for speed_harmonic in np.linspace(1.0, 2.0, 1000):
        # Your equation logic
        # (Energy_at_Speed - Gravity_Tension) / Scaling
        current_stability = (speed_harmonic - PHI_TERM) / INTERVAL
        error = abs(current_stability - GOAL)

        if error < best_error:
            best_error = error
            best_speed = speed_harmonic

        if error < 0.0001:
            return speed_harmonic, current_stability

    # Fallback: return best sampled point
    return best_speed, (best_speed - PHI_TERM) / INTERVAL


resonant_speed, stability = harmonic_truth_search()
print(f"RESONANCE FOUND AT: {resonant_speed:.5f} units")
print(f"STABILITY AT RESONANCE: {stability:.6f}")
print("This is the 'Maximum Speed' of a particle in your 1.0-Stability universe.")

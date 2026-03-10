import numpy as np
import matplotlib.pyplot as plt

# Simulation Constants
size = 100
dt = 0.05
c_sq = 800.0  # Speed of Light squared (The 'Mass' regulator)
eta = 0.5     # Gravity coupling constant
CRITICAL_THRESHOLD = 5.0  # Black hole formation threshold
attraction_strength = 0.2  # Energy absorption rate

# Initialize Fields
psi = np.random.normal(0.5, 0.01, (size, size)) # Energy
phi = np.zeros((size, size))                    # Gravity

history = []

for frame in range(500):
    # 1. GENERATE MASS: m = E / c^2
    # Every bit of Energy (Psi) now creates a Mass field
    mass_density = psi / c_sq
    
    # 2. CALCULATE GRAVITY (Phi) from Mass
    # Simplified Poisson: Gravity potential is the "Inverse Laplacian" of mass
    phi = (np.roll(mass_density, 1, axis=0) + np.roll(mass_density, -1, axis=0) +
           np.roll(mass_density, 1, axis=1) + np.roll(mass_density, -1, axis=1)) * eta
    
    # 2.5. CHECK FOR SINGULARITY (Black Hole Formation)
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if psi[i, j] > CRITICAL_THRESHOLD:
                # Gravity becomes infinite at this point
                phi[i, j] *= 10.0
                
                # Nearby energy is 'sucked in'
                # Get all 8 neighbors
                neighbors_vals = [
                    psi[i-1, j-1], psi[i-1, j], psi[i-1, j+1],
                    psi[i, j-1],                psi[i, j+1],
                    psi[i+1, j-1], psi[i+1, j], psi[i+1, j+1]
                ]
                absorption = sum(neighbors_vals) * attraction_strength
                
                # Transfer energy from neighbors to singularity
                psi[i-1:i+2, j-1:j+2] *= (1.0 - attraction_strength)
                psi[i, j] += absorption * 0.5  # Singularity gains energy
    
    # 3. APPLY YOUR EVOLUTION EQUATION (IMG_4296)
    # Term: -η/T ∇Φ
    grad_phi_y, grad_phi_x = np.gradient(phi)
    advection = -(grad_phi_x + grad_phi_y)
    
    # Update Psi (Energy)
    # We add a damping term so it doesn't run away like the first graph
    psi += (advection - 0.01 * psi) * dt
    
    # 4. TEST STABILITY (IMG_4268)
    # (Integral(Psi)dt + (-1) * Phi / sqrt(2)) / (9/8)
    unity_check = (np.mean(psi) - np.mean(phi)/np.sqrt(2)) / (9/8)
    history.append(abs(unity_check))

# Plotting the Result
plt.figure(figsize=(10, 5), facecolor='white')
plt.plot(history, label="Universe Stability (With Mass)")
plt.axhline(y=1.0, color='r', linestyle='--', label="Theoretical Truth")
plt.ylim(0, 2)
plt.legend()
plt.title("Mass-Corrected Stability: Does the Butterfly Settle?")
plt.show()

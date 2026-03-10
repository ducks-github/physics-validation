import numpy as np

# --- Simulation Constants ---
C = 3.0e8          # Speed of Light (m/s)
GRID_INCHES = 1e20 # Let's assume each grid cell is a massive cosmic distance
LBS_PER_KG = 2.204

def calculate_cosmic_pressure(psi_field):
    # 1. Total Energy (Sum of all Psi)
    total_energy = np.sum(np.abs(psi_field))
    
    # 2. Total Mass (m = E/c^2)
    total_mass_kg = total_energy / (C**2)
    total_mass_lbs = total_mass_kg * LBS_PER_KG
    
    # 3. Pressure (lbs / square inch)
    # Total area of the 'Universe' grid in square inches
    total_area_sq_in = (psi_field.shape[0] * psi_field.shape[1]) * GRID_INCHES
    
    psi_pressure = total_mass_lbs / total_area_sq_in
    
    return total_mass_lbs, psi_pressure

# Example Readout based on your 'Figure_1' data (Value ~50)
mock_psi = np.full((100, 100), 50.0)
mass_lbs, pressure_psi = calculate_cosmic_pressure(mock_psi)

print(f"TOTAL UNIVERSE WEIGHT: {mass_lbs:.2e} lbs")
print(f"COSMIC PRESSURE: {pressure_psi:.2e} lbs/sq in")

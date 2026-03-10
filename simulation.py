import numpy as np
import pygame

# --- Constants & Settings ---
WIDTH, HEIGHT = 1000, 700
GRID_W, GRID_H = 100, 50
UI_HEIGHT = 200  # Space at the bottom for the graph
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Courier", 16)
clock = pygame.time.Clock()

# Fields
psi = np.zeros((GRID_W, GRID_H))
source_pos = (5, GRID_H // 2)
slit_x = 40
CRITICAL_THRESHOLD = 8.0  # Black hole formation threshold
attraction_strength = 0.15  # Energy absorption rate


def apply_milky_way_physics(field, dt=0.1):
    # Diffusion (D∇²Ψ)
    laplacian = (np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
                 np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) - 4*field)
    
    # Harmonic Coupling + Growth (λχξΨ)
    # This creates the "Butterfly" feedback loop
    growth = 0.05 * field 
    
    return field + (0.2 * laplacian + growth) * dt


def check_singularities(field):
    # Detect and amplify black holes when Ψ exceeds critical threshold
    for i in range(1, field.shape[0] - 1):
        for j in range(1, field.shape[1] - 1):
            if field[i, j] > CRITICAL_THRESHOLD:
                # Extract energy from neighbors
                neighbors_energy = (
                    field[i-1, j-1] + field[i-1, j] + field[i-1, j+1] +
                    field[i, j-1] +                  field[i, j+1] +
                    field[i+1, j-1] + field[i+1, j] + field[i+1, j+1]
                )
                
                # Neighbors lose energy to the singularity
                field[i-1:i+2, j-1:j+2] *= (1.0 - attraction_strength)
                # Singularity gains half the absorbed energy
                field[i, j] += neighbors_energy * attraction_strength * 0.5
    
    return field


def draw_intensity_graph(screen, field_slice):
    # Draws a line graph of energy density at the detector screen
    graph_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)
    pygame.draw.rect(screen, (20, 20, 40), graph_rect)  # Graph background
    
    points = []
    max_val = np.max(field_slice) + 1e-5
    for x_coord, val in enumerate(field_slice):
        px = 50 + (x_coord * (graph_rect.width / len(field_slice)))
        # Normalize height to graph space
        py = (HEIGHT - 50) - (val / max_val * 80)
        points.append((px, py))
    
    if len(points) > 1:
        pygame.draw.lines(screen, (0, 255, 255), False, points, 2)
    
    label = font.render("DETECTOR SCREEN INTENSITY (Ψ INTERFERENCE)", True, (200, 200, 200))
    screen.blit(label, (50, HEIGHT - 175))


# --- Main Execution ---
running = True
frame = 0
while running:
    screen.fill((5, 5, 12))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. EMIT ENERGY (The Big Bang / Atom Source)
    psi[source_pos] = np.sin(frame * 0.4) * 10.0

    # 2. THE DOUBLE SLIT WALL (The Observer Barrier)
    psi[slit_x, :] = 0
    psi[slit_x, 20:23] = psi[slit_x - 1, 20:23]  # Upper Slit
    psi[slit_x, 27:30] = psi[slit_x - 1, 27:30]  # Lower Slit

    # 3. COMPUTE PHYSICS
    psi = apply_milky_way_physics(psi)
    psi *= 0.999  # Global energy decay

    # 3.5. CHECK FOR BLACK HOLE FORMATION
    psi = check_singularities(psi)

    # 4. DRAW THE FIELD (The Vitruvian Universe)
    scale_x = WIDTH // GRID_W
    scale_y = (HEIGHT - UI_HEIGHT) // GRID_H
    for i in range(GRID_W):
        for j in range(GRID_H):
            val = abs(psi[i, j])
            if val > 0.05:
                intensity = int(np.clip(val * 40, 0, 255))
                color = (intensity // 4, intensity // 2, intensity)
                pygame.draw.rect(
                    screen,
                    color,
                    (i * scale_x, j * scale_y, scale_x, scale_y),
                )

    # Draw the slit wall line for visual reference
    pygame.draw.line(
        screen,
        (60, 60, 80),
        (slit_x * scale_x, 0),
        (slit_x * scale_x, HEIGHT - UI_HEIGHT),
        2,
    )

    # 5. DRAW INTENSITY GRAPH (The Butterfly Pattern Revealed)
    # Sample the field at x=80 (detector screen position)
    detector_x = 80
    if detector_x < GRID_W:
        detector_slice = np.abs(psi[detector_x, :])
        draw_intensity_graph(screen, detector_slice)

    pygame.display.flip()
    clock.tick(60)
    frame += 1

pygame.quit()

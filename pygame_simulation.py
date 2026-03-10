import numpy as np
import pygame
import random

# --- 1. Setup ---
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 100 
SCALE = WIDTH // GRID_SIZE
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# The Galaxy Field (Psi)
psi = np.zeros((GRID_SIZE, GRID_SIZE))

# Physics Constants from your equation
D = 0.15          # Diffusion
growth = 0.02     # \u03bb\u03c7\u03be\u03a8
decay = 0.98      # Entropy (so it doesn't explode)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 2. RANDOM GENERATOR (The Butterfly Triggers)
    # Random "Star Births" (S) - small bursts of energy anywhere
    if random.random() > 0.9: 
        rx, ry = random.randint(30, 70), random.randint(30, 70)
        psi[rx, ry] += random.uniform(5, 15)

    # Random "Gravitational Shift" (The Twist)
    # This shifts the whole galaxy slightly, creating the spiral
    shift_x = random.randint(-1, 1)
    shift_y = random.randint(-1, 1)
    psi = np.roll(psi, shift_x, axis=0)
    psi = np.roll(psi, shift_y, axis=1)

    # 3. APPLY PHYSICS (The Equation)
    # Calculate Laplacian (Diffusion: \u2202\u00b2\u03a8)
    laplacian = (np.roll(psi, 1, axis=0) + np.roll(psi, -1, axis=0) +
                 np.roll(psi, 1, axis=1) + np.roll(psi, -1, axis=1) - 4*psi)
    
    # Update Psi: Change = Diffusion + Growth
    psi += (D * laplacian + growth * psi)
    psi *= decay # Keep the energy in check

    # 4. DRAWING
    screen.fill((5, 5, 15)) # Dark space background
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if psi[i, j] > 0.1:
                # Color mapping: High energy = White/Cyan, Low = Purple
                brightness = min(255, int(psi[i, j] * 50))
                color = (brightness // 2, brightness // 4, brightness)
                
                # Add a little "shimmer" with random flicker
                flicker = random.randint(-20, 20)
                color = tuple(max(0, min(255, c + flicker)) for c in color)
                
                pygame.draw.rect(screen, color, (i*SCALE, j*SCALE, SCALE, SCALE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

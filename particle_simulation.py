import pygame
import numpy as np
import random

# --- 1. Simulation Constants ---
WIDTH, HEIGHT = 800, 800
NUM_PARTICLES = 2000
G = 0.5  # Gravitational Constant for our "Universe"
c = 3.0  # Normalized speed of light for the sim

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Star:
    def __init__(self):
        # All stars start near the "Big Bang" center
        self.pos = np.array([WIDTH//2, HEIGHT//2], dtype=float)
        # Give them an initial random "Explosion" velocity
        angle = random.uniform(0, 2 * np.pi)
        speed = random.uniform(1, 5)
        self.vel = np.array([np.cos(angle), np.sin(angle)]) * speed
        self.color = (random.randint(150, 255), random.randint(100, 200), 255)

    def apply_gravity(self, centers):
        for c_pos, mass in centers:
            # Vector from star to gravity center
            diff = c_pos - self.pos
            dist_sq = np.sum(diff**2) + 100 # +100 prevents "division by zero"
            force_mag = G * mass / dist_sq
            
            # Update velocity based on the pull
            unit_vec = diff / np.sqrt(dist_sq)
            self.vel += unit_vec * force_mag

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99 # Friction/Drag so they don't fly away forever

# Initialize Particles
stars = [Star() for _ in range(NUM_PARTICLES)]

# Initial Gravity Hubs (The "S" and "Coupling" points)
hubs = [{"pos": np.array([WIDTH//2, HEIGHT//2], dtype=float), "energy": 500.0}]

running = True
while running:
    screen.fill((5, 0, 20)) # Deep Space Blue
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # RANDOM BUTTERFLY EFFECT: 
    # Occasionally spawn a new gravity hub to "pull" the spiral arms
    if random.random() > 0.98:
        hx = random.randint(200, 600)
        hy = random.randint(200, 600)
        hubs.append({"pos": np.array([hx, hy], dtype=float), "energy": float(random.randint(50, 200))})
        if len(hubs) > 5: hubs.pop(1) # Keep only a few active hubs

    # E = mc^2 -> m = E / c^2
    # Convert hub energy to dynamic gravitational mass each frame
    gravity_centers = []
    for hub in hubs:
        energy_intensity = hub["energy"]
        dynamic_mass = energy_intensity / (c**2)
        gravity_centers.append((hub["pos"], dynamic_mass))

    # Update and Draw Stars
    for s in stars:
        s.apply_gravity(gravity_centers)
        s.update()
        
        # Wrap-around logic (Simple Möbius-style edge)
        s.pos[0] %= WIDTH
        s.pos[1] %= HEIGHT
        
        pygame.draw.circle(screen, s.color, s.pos.astype(int), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

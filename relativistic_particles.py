import pygame
import numpy as np

# --- 1. Setup ---
WIDTH, HEIGHT = 800, 800
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- 2. Relativistic Constants ---
# Lower 'c' makes energy MUCH heavier (E/c^2 becomes a large mass)
c_light = 10.0
G = 1.2  # Gravitational constant

particles = []
# Create 1000 stars at the 'Big Bang' center
for _ in range(1000):
    particles.append({
        "pos": np.array([WIDTH // 2, HEIGHT // 2], dtype=float),
        "vel": np.random.normal(0, 2, 2),
        "energy": np.random.uniform(10, 50)  # The 'Psi' value for this star
    })

# --- Update the Initialization ---
# Instead of one central hub, we define two distinct 'Big Bang' sources
hubs = [
    [np.array([WIDTH // 3, HEIGHT // 2], dtype=float), 800],  # Source 1 (Massive)
    [np.array([2 * WIDTH // 3, HEIGHT // 2], dtype=float), 800],  # Source 2 (Massive)
]


# The apply_gravity loop automatically sums the pull from both
def apply_gravity(p, hubs):
    for c_pos, mass in hubs:
        diff = c_pos - p["pos"]
        dist_sq = np.sum(diff**2) + 500
        # The total force is the sum of vectors from both hubs
        force_mag = G * mass / dist_sq
        p["vel"] += (diff / np.sqrt(dist_sq)) * force_mag

running = True
while running:
    screen.fill((2, 5, 15))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Gravity from both hubs
    for p in particles:
        apply_gravity(p, hubs)

        # Update position
        p["pos"] += p["vel"]

        # Soft damping and wrap-around
        p["vel"] *= 0.999
        p["pos"][0] %= WIDTH
        p["pos"][1] %= HEIGHT

        # Draw particle with color based on energy
        e = p["energy"]
        brightness = int(np.clip((e - 10) / 40 * 255, 60, 255))
        color = (brightness // 3, brightness // 2, brightness)
        pygame.draw.circle(screen, color, p["pos"].astype(int), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

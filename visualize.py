import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ==========================================
# CTFC VISUALIZER: The Sediment Effect
# Purpose: Animate the "Gravitational Wake" (Dark Matter)
# created by mass moving through viscous spacetime.
# ==========================================

# 1. SETUP THE SPACETIME GRID
grid_size = 100
x = np.linspace(0, 10, grid_size)
y = np.linspace(0, 10, grid_size)
X, Y = np.meshgrid(x, y)

# 2. DEFINE THE MASS & SEDIMENT PROPERTIES
# Standard Gravity Field (Inverse Square)
def gravity_potential(x0, y0, mass=1.0):
    dist = np.sqrt((X - x0)**2 + (Y - y0)**2)
    dist[dist < 0.1] = 0.1 # Prevent singularity
    return mass / dist

# 3. INITIALIZE STATE
# Star starts at (2, 5) and moves to the right
star_pos = [2.0, 5.0]
velocity = [0.05, 0.0] 
sediment_grid = np.zeros_like(X) # Starts empty
decay_rate = 0.95 # How fast the wake fades (Lambda)
accumulation_rate = 0.5 # How much wake is deposited (Xi)

# Setup Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("CTFC Simulation: Gravitational Hysteresis (Dark Matter Wake)")
ax.set_xlabel("Space (X)")
ax.set_ylabel("Space (Y)")

# Visual Elements
# The "Wake" (Dark Matter) - Contour Map
contour = ax.contourf(X, Y, sediment_grid, cmap='Blues', alpha=0.6)
# The "Star" (Baryonic Mass) - Red Dot
star_dot, = ax.plot([], [], 'ro', markersize=10, label='Star (Mass)')
# The "Total Gravity" probe line
probe_text = ax.text(0.5, 9.5, '', fontsize=10, color='black')

def update(frame):
    global star_pos, sediment_grid, contour
    
    # A. MOVE THE STAR
    star_pos[0] += velocity[0]
    star_pos[1] += velocity[1]
    
    # Loop around screen
    if star_pos[0] > 10: star_pos[0] = 0
    
    # B. DEPOSIT SEDIMENT (The Golden Equation Application)
    # New sediment is added at current star position
    # This represents M_eff = M_bar + Integral(History)
    current_gravity = gravity_potential(star_pos[0], star_pos[1], mass=accumulation_rate)
    sediment_grid += current_gravity
    
    # C. APPLY DECAY (The Lambda Term)
    # The wake fades over time, but slowly.
    sediment_grid *= decay_rate
    
    # D. UPDATE VISUALS
    # Clear old contours to redraw
    for c in contour.collections:
        c.remove()
    
    # Draw new sediment (The Wake)
    # We use a threshold to show only significant "Dark Matter"
    contour = ax.contourf(X, Y, sediment_grid, levels=20, cmap='Purples', alpha=0.7)
    
    # Draw Star
    star_dot.set_data([star_pos[0]], [star_pos[1]])
    
    # Update Status Text
    # Calculate Ratio of Wake vs. Star Mass at current location
    wake_density = sediment_grid[int(star_pos[1]*10), int(star_pos[0]*10)]
    probe_text.set_text(f"Time Step: {frame}\nWake Intensity: {wake_density:.2f}")
    
    return star_dot, probe_text

# 4. RUN ANIMATION
ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=False)

# To save: ani.save('sediment_wake.gif', writer='imagemagick')
plt.show()

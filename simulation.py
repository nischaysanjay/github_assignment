import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ffmpeg

num_particles = 5
width = 10
height = 10
radius = 0.1
max_speed = 1.0
np.random.seed(0)
x, y, angle = np.random.uniform(radius, width-radius, num_particles), np.random.uniform(radius, height-radius, num_particles), np.random.uniform(0, 2*np.pi, num_particles)
vx, vy = max_speed*np.cos(angle), max_speed*np.sin(angle)

fig, ax = plt.subplots()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
circles = [plt.Circle((x[i], y[i]), radius, ec='none', fc='r') for i in range(num_particles)]
[ax.add_artist(circle) for circle in circles]

def update(frame):
    global x, y, vx, vy
    x, y = x+vx, y+vy
    for i in range(num_particles):
        if x[i]-radius < 0 or x[i]+radius > width:
            vx[i] *= -1
        if y[i]-radius < 0 or y[i]+radius > height:
            vy[i] *= -1
        for j in range(i+1, num_particles):
            dx, dy = x[i]-x[j], y[i]-y[j]
            dist = np.sqrt(dx**2+dy**2)
            if dist < 2*radius:
                ux, uy = dx/dist, dy/dist
                vix, viy = ux*vx[i]+uy*vy[i], -uy*vx[i]+ux*vy[i]
                vjx, vjy = ux*vx[j]+uy*vy[j], -uy*vx[j]+ux*vy[j]
                vx[i], vy[i] = ux*vjx-uy*vjy, uy*vjx+ux*vjy
                vx[j], vy[j] = ux*vix-uy*viy, uy*vix+ux*viy
        circles[i].set_center((x[i], y[i]))
    return circles

ani = FuncAnimation(fig, update, frames=range(100), blit=True)
ani.save('simulation.mpeg', writer='ffmpeg', fps=60)
plt.show()

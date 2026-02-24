import numpy as np
import matplotlib.pyplot as plt

print("Script started")

u = 20.0   # wind speed (m/s)

# Grid parameters
nx = 200
L = 1000.0
dx = L / nx
x = np.linspace(0, L, nx)

# Diffusion coefficient
D = 5.0

# Time parameters
dt = 0.1
nt = 200

# Initial condition (unit mass spike)
C = np.zeros(nx)
C[nx // 2] = 1.0 / dx
print("Initial mass:", np.sum(C) * dx)

plt.figure()

# Time integration loop
for n in range(nt):
    C_new = C.copy()

    for i in range(1, nx - 1):
        # Advection (wind transport) - upwind scheme
        advection = -u * (C[i] - C[i - 1]) / dx

        # Diffusion (spreading)
        second_derivative = (C[i + 1] - 2 * C[i] + C[i - 1]) / dx**2
        diffusion = D * second_derivative

        # Combined update
        C_new[i] = C[i] + dt * (advection + diffusion)

    # Simple open boundary conditions
    C_new[0] = C_new[1]
    C_new[-1] = C_new[-2]

    # Update state AFTER finishing all i
    C = C_new

    # Live plot every 10 steps
    if n % 10 == 0:
        plt.clf()
        plt.plot(x, C)
        plt.xlabel("Distance (m)")
        plt.ylabel("Concentration")
        plt.title(f"Aerosol advection-diffusion (t = {n*dt:.1f}s)")
        plt.ylim(0, 0.25)
        plt.pause(0.01)

print("Final mass:", np.sum(C) * dx)

plt.figure()
plt.plot(x, C)
plt.xlabel("Distance (m)")
plt.ylabel("Concentration")
plt.title("Final concentration")
print("About to show plot")
plt.show()
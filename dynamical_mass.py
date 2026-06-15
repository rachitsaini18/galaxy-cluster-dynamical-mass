"""
Estimating the Dynamical Mass of a Galaxy Cluster
==================================================

This script demonstrates a simplified workflow for estimating the dynamical
mass of a galaxy cluster using the virial theorem:

    M_dyn = (3 * sigma^2 * R) / G

where:
    sigma = velocity dispersion of galaxies in the cluster (km/s)
    R     = characteristic cluster radius (kpc)
    G     = gravitational constant, expressed in kpc * (km/s)^2 / M_sun

The script is structured in two parts:

1. (Optional) Load and inspect a FITS image of a galaxy cluster using Astropy,
   if a suitable file (e.g. an SDSS frame) is available.
2. Generate a simulated 2D Gaussian light profile representing a cluster,
   for visualization purposes, and compute the dynamical mass estimate
   using assumed/representative values for sigma and R.
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------------------------------------------------
# SECTION 1: Load and explore a FITS file (optional)
# -----------------------------------------------------------------------
# If you have an observational image (e.g. an SDSS or MaNGA FITS frame),
# point fits_path to it. If unavailable, the script proceeds with a
# simulated cluster image for demonstration purposes.

fits_path = "frame-r-005071-3-0347.fits"  # Replace with your file

try:
    hdul = fits.open(fits_path)
    print(hdul.info())

    data = hdul[0].data
    header = hdul[0].header

    print("FITS Header Object:", header.get("OBJECT", "N/A"))
    print("Image Shape:", data.shape)
    print("Mean Flux:", np.mean(data))
    print("Max Flux:", np.max(data))

    hdul.close()
except Exception as e:
    print("Error loading FITS file:", e)
    data = None  # Proceed with simulated cluster if unavailable


# -----------------------------------------------------------------------
# SECTION 2: Simulated 2D Gaussian cluster (for visualization)
# -----------------------------------------------------------------------

x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
x, y = np.meshgrid(x, y)
z = np.exp(-(x**2 + y**2))  # Gaussian light profile

plt.figure(figsize=(6, 5))
plt.imshow(z, origin="lower", extent=(-5, 5, -5, 5), cmap="inferno")
plt.colorbar(label="Relative Intensity")
plt.title("Simulated Galaxy Cluster (2D Gaussian Profile)")
plt.xlabel("X (arbitrary units)")
plt.ylabel("Y (arbitrary units)")
plt.tight_layout()
plt.savefig("figures/simulated_galaxy_cluster.png", dpi=300)
plt.show()


# -----------------------------------------------------------------------
# SECTION 3: Dynamical mass estimation using the virial theorem
# -----------------------------------------------------------------------
# Representative values, broadly consistent with massive SDSS-like
# galaxy clusters.

sigma = 1000  # km/s, velocity dispersion
R = 1000      # kpc, cluster radius (1 Mpc)
G = 4.3e-6    # gravitational constant in kpc * (km/s)^2 / M_sun

M_dyn = (3 * sigma**2 * R) / G  # in solar masses

print(f"\nEstimated Dynamical Mass: {M_dyn:.2e} M_sun")


# -----------------------------------------------------------------------
# SECTION 4: Save result
# -----------------------------------------------------------------------

with open("results/dynamical_mass_result.txt", "w") as f:
    f.write(f"Estimated Dynamical Mass: {M_dyn:.2e} M_sun\n")
    f.write(
        f"Using sigma = {sigma} km/s, R = {R} kpc, "
        f"G = {G} kpc*(km/s)^2/M_sun\n"
    )

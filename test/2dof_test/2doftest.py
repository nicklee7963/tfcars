import numpy as np

# Conversion factor from radians to degrees
conversion = 180 / np.pi

def move_to_pos(x, y, z):
    # Compute the angles in radians first
    b = np.arctan2(y, x) * conversion
    l = np.sqrt(x**2 + y**2)
    h = np.sqrt(l**2 + z**2)
    phi = np.arctan2(z, l) * conversion
    theta = np.arccos((h / 2) / 75) * conversion
    
    # Calculate angles a1 and a2
    a1 = phi + theta
    a2 = phi - theta
    
    return a1, a2

# Example usage
x, y, z = 10, 20, 30  # Example coordinates
a1, a2 = move_to_pos(x, y, z)
print(f"a1: {a1}, a2: {a2}")

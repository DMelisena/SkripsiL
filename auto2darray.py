import numpy as np

# Method 2: Using NumPy
rows = 3  # Number of rows in the array
cols = 4  # Number of columns in the array

# Create a 2D array initialized with zeros
array = np.zeros((rows, cols))

# Update specific elements in the array
array[0, 1] = 5
array[2, 3] = 10

# Print the array
print(array)
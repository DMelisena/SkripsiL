import matplotlib.pyplot as plt
import numpy as np

# Load the two images
image1 = plt.imread('RoomDoseDistribution.png')
image2 = plt.imread('DoseDistributionMap.png')

# Create a figure and axes
fig, ax = plt.subplots()

# Display the first image
ax.imshow(image1)

# Set the alpha value (transparency) for the second image
alpha = 0.5
image2_with_alpha = np.copy(image2)
image2_with_alpha[..., 3] = alpha  # Set the alpha channel

# Flip the second image
flipped_image2 = np.flipud(image2_with_alpha)

# Overlay the flipped second image with transparency on top of the first image
ax.imshow(flipped_image2, origin='lower')

# Hide the axis labels and ticks
ax.axis('off')

# Save the combined image
plt.savefig('combined_image.png', dpi=300)

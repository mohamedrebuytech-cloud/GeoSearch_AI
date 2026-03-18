import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import os

# 1. Load the processed satellite data
file_path = "sukkari_sample.nc"

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please run the download script first.")
else:
    ds = xr.open_dataset(file_path)
    data = ds.sukkari_data.values[0] 

    # Prepare RGB image for visualization
    rgb_img = np.stack([data[0], data[1], data[2]], axis=-1)
    p_low, p_high = np.percentile(rgb_img, (2, 98)) 
    rgb_img = np.clip((rgb_img - p_low) / (p_high - p_low) * 255, 0, 255).astype(np.uint8)

    def identify_mineral(signature):
        # Bands: 0:Red, 1:Green, 2:Blue, 3:NIR, 4:SWIR
        red, green, blue, nir, swir = signature[0]
        
        # Geological Band Ratios (Indices)
        iron_index = red / blue if blue != 0 else 0
        quartz_index = swir / nir if nir != 0 else 0
        
        # Classification Logic based on Reflectance Properties
        if quartz_index > 1.25:
            return "Quartz / High Silica"
        elif iron_index > 1.6:
            return "Iron Oxides (Hematite/Goethite)"
        elif swir > nir and swir > 0.35:
            return "Hydrothermal Alteration Zone"
        elif nir > red and nir > 0.4:
            return "Sparse Vegetation"
        else:
            return "General Rock / Surface Soil"

    print("System Ready. High Precision Spectral Matching (99.99%) enabled.")

    def on_click(event):
        if event.xdata is not None and event.ydata is not None:
            ix, iy = int(event.xdata), int(event.ydata)
            
            # Extract Spectral Signature
            target_signature = data[:, iy, ix].reshape(1, -1)
            
            # Predict Mineral Type
            mineral_name = identify_mineral(target_signature)
            
            # Perform Cosine Similarity Matching
            all_pixels = data.reshape(data.shape[0], -1).T
            similarity = cosine_similarity(all_pixels, target_signature).reshape(data.shape[1], data.shape[2])
            
            # High Sensitivity Threshold
            threshold = 0.9999 
            mask = similarity > threshold
            
            plt.clf()
            
            # Plot 1: Target Selection and Identification
            ax1 = plt.subplot(1, 2, 1)
            ax1.imshow(rgb_img)
            ax1.scatter([ix], [iy], c='#00ffff', s=100, marker='x')
            ax1.set_title(f"Target: {mineral_name}")
            
            # Plot 2: Spatial Distribution of Identified Mineral
            ax2 = plt.subplot(1, 2, 2)
            ax2.imshow(rgb_img, alpha=0.5) 
            overlay = np.zeros((*mask.shape, 4))
            overlay[mask] = [1, 0, 0, 1] # Red highlight for matches
            ax2.imshow(overlay)
            ax2.set_title(f"Matches for {mineral_name}")
            
            plt.draw()
            print(f"Target analyzed. Predicted Class: {mineral_name}")

    fig = plt.figure(figsize=(15, 7))
    plt.imshow(rgb_img)
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.title("Geosearch AI: Mineral Identification and Spectral Mapping")
    plt.show()
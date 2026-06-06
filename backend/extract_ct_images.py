import nibabel as nib
import matplotlib.pyplot as plt
import os

# Path to one CT file (change name if needed)
file_path = "coronacases_org_001.nii"


# Load CT scan
ct = nib.load(file_path)
data = ct.get_fdata()

# Create output folder
out_folder = "ct_slices"
os.makedirs(out_folder, exist_ok=True)

# Save few middle slices as PNG
total_slices = data.shape[2]

for i in range(10):   # save 10 images
    slice_index = total_slices//2 + i

    plt.imshow(data[:,:,slice_index], cmap="gray")
    plt.axis("off")
    
    plt.savefig(f"{out_folder}/slice_{i}.png", bbox_inches="tight", pad_inches=0)
    plt.close()

print("CT slices extracted successfully!")
 
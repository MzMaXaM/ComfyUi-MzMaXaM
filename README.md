# ComfyUi-MzMaXaM
A pack of nodes, to make my life and hopefully your a bit easier.

<img width="1472" alt="image" src="https://github.com/user-attachments/assets/b23b0c69-eda6-49d2-8186-dc842de268d6">

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/MzMaXaM/ComfyUi-MzMaXaM.git
    ```
2. ComfyUi Manager

    ComfyUi Manager/ Custom Nodes Manager/ Search for "mzmaxam"

# 1. Select Latent Size Node

![image](https://github.com/user-attachments/assets/bb81b4a3-06f1-4793-a663-5b70e600e5c7)


## Overview
A custom node for ComfyUI designed to generate an empty latent image at predefined resolutions. This node is useful for initializing images for further processing.

## Features
- **Predefined Resolutions**: Users can select from a list of common resolutions.
- **User-Friendly Interface**: Easy to use within the ComfyUI environment.

## Usage
1. Open ComfyUI.
2. Add the custom node from the node library.
3. Select the desired resolution from the provided list.
4. Generate the latent image.

## Curently resolutions
```
"Cinema landscape (1536x640) 21x9",
"Smartphone landscape (1472x704) 19x9",
"HD_Video landscape (1344x768) 16x9",
"Laptop landscape (1216x768) 8x5",
"Photo landscape (1216x832) 3x2",
"Widescreen landscape (1176x840) 7x5",
"TV landscape (1152x896) 4x3",
"Square (1024x1024) 1x1",
"TV portrait (896x1152) 4x3",
"Widescreen portrait (840x1176) 7x5",
"Photo portrait (832x1216) 3x2",
"Laptop portrait (768x1216) 8x5",
"HD_Video portrait (768x1344) 16x9",
"Smartphone portrait (704x1472) 19x9",
"Cinema portrait (640x1536) 21x9",
```

# 2. Text Encoder 3 in 1

![image](https://github.com/user-attachments/assets/95017521-0be3-4f0d-b162-0f592f3c77aa)

## Overview
A custom node for ComfyUI designed to use with pony models. It have 2 positive and one negative text encoders.
2 positives becouse in pony models I always want to keep the scores separate from the prompt.
2 positive text are concatenated and send over as one conditional.

## Features
- **2 positive text encoders**: Users can use one for scores while other to change the prompt as they want.
- **User-Friendly Interface**: Easy to use within the ComfyUI environment.

## Usage
1. Open ComfyUI.
2. Add the custom node from the node library.
3. Insert the prompts.
4. Select the clip-skip.
4. Conect outputs to the Sampler.

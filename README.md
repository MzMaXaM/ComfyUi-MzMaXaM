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

# 1. Select Latent Size Node 1Mp

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
"Hd Wide landscape (1344x712) 17x9", #New
"HD_Video landscape (1280x720) 16x9", #Updated
"Laptop landscape (1216x768) 8x5",
"Photo landscape (1216x832) 3x2",
"Widescreen landscape (1176x840) 7x5",
"TV landscape (1152x896) 4x3",
"Square (1024x1024) 1x1",
"TV portrait (896x1152) 4x3",
"Widescreen portrait (840x1176) 7x5",
"Photo portrait (832x1216) 3x2",
"Laptop portrait (768x1216) 8x5",
"HD_Video portrait (720x1280) 16x9", #Updated
"Hd Wide portrait (712x1344) 17x9", #New
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

# 3. Select Latent Size Node 2Mp   #Temporary for testing purposes

Added this version for testing I don't think anyone need it if I'll find were to use it Ill update it...

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
"Cinema landscape (2176x960) 21x9",#2.26
"Smartphone landscape (2080x992) 19x9",#2.09
"HD Wide landscape (1904x1008) 17x9",#1.89
"HD Video landscape (1920x1080) 16x9",#1.77
"Laptop landscape (1720x1088) 8x5",#1.58
"Photo landscape (1720x1184) 3x2",#1.45
"Widescreen landscape (1664x1184) 7x5",#1.4
"TV landscape (1632x1280) 4x3",#1.28
"Square (1448x1448) 1x1",#1
"TV portrait (1280x1632) 4x3",#0.78
"Widescreen portrait (1184x1664) 7x5",#0.71
"Photo portrait (1184x1720) 3x2",#0.68
"Laptop portrait (1088x1720) 8x5",#0.63
"HD Video portrait (1080x1920) 16x9",#0.56
"HD Wide portrait (1008x1904) 17x9",#0.53
"Smartphone portrait (992x2080) 19x9",#0.48
"Cinema portrait (960x2176) 21x9",#0.44
```

# 4. Upscale Latent/Image by 1.5

## Overview
I created this node for my workflows in which I'm using 16:9 resolution, and 
from (1280x720) 16x9, it's exactly 1.5 times smaller than (1080x1920) 16x9

That's why I made it :D

## Features
- upscale latent by 1.5 for the next Hi-Rez
- amount to duplicate IMG n times so you can choose the one you like 

## Usage
1. Open ComfyUI.
2. Add the custom node from the node library.
3. Insert the latent image.
4. Select the amount you want, default is 1.
4. Connect output to the Sampler.



# Image to Text Ollama
Worked on a node that would send the input image to the local Ollama Models.
You have to Install Ollama and add Visual Models for it to work.
As of today I can recommend minicpm Model
Bear in mind that the LLM model will eat resources...

# Text to Text Ollama
As the name suggests this node should generate a prompt for you from the prompt you'll give it :D
Don't forget that LLM models eat your resources.
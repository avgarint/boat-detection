# boat-detection

A python project developed during school that aims to detect boats from satellite imagery using PIL.Image.

Original picture           |  Output
:-------------------------:|:-------------------------:
<img src="https://user-images.githubusercontent.com/66020831/190869765-ae9ba35b-50d4-4985-89a8-ffbee5516fc0.png" width="550px" />  |  <img src="https://user-images.githubusercontent.com/66020831/190869769-fa9cea3d-6e69-46a5-abcd-a9b5a5e9342f.png" width="550px" />

## Libraries
- ``Pil Image``: [Website](https://pillow.readthedocs.io/en/stable/installation.html) or [Github repository](https://github.com/python-pillow/Pillow)

## Usage
```py
detect(img_path="Samples\Boat17.PNG", save_path="Output", remove_boats=False, export_as_mask=True)
```

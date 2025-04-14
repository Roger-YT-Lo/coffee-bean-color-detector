# Coffee Bean Color Detection using ESP32-CAM and OpenCV

This project uses an ESP32-CAM to capture real-time images of coffee beans, which are processed with OpenCV in Python to detect color (light, medium, dark) and edge imperfections (missing corners).

## Features

- **Real-time image capture** from ESP32-CAM via MJPEG stream.
- **HSV color analysis** to classify coffee beans as:
  - Light roast
  - Medium roast
  - Dark roast
- **Contour analysis** to detect physical imperfections (e.g., broken or chipped beans).
- Option to **save images** and **inspect HSV values** by keyboard input.

## Usage

1. Set the correct IP address for your ESP32-CAM stream:
   ```python
   url = "http://<your_esp32_ip>:81/stream"
   ```

2. Run the Python script:
   - Press `a` to save the current frame as an image.
   - Press `s` to display the HSV value at the center of the frame and classify bean color.
   - Press `q` to quit.

3. Saved images are stored in:
   ```
   C:/Users/Asus/Desktop/CoffeeBeans/
   ```

## Color Identity Ranges

These HSV ranges are used to classify bean colors. You may tweak them depending on your lighting condition.

| Roast Level | HSV Range (approx.) |
|-------------|---------------------|
| Light       | [10, 30, 90] to [30, 150, 200] |
| Medium      | [10, 50, 40] to [35, 200, 80]  |
| Dark        | [5, 50, 30] to [35, 255, 50]   |

> ⚠️ Color recognition may be affected by environmental lighting and camera quality. You can adjust HSV ranges as needed.

## ESP32-CAM Firmware

We use the standard MJPEG streaming example provided by Espressif. Due to licensing concerns, the source code is **not included** in this repository.  
You can find it by searching for the **ESP32-CAM MJPEG stream example** in Espressif’s GitHub repository or Arduino IDE examples.


## Contact

Roger YT.Lo--NTUST ECE  
Email: roger020739@gmail.com  
ECE, NTUST  


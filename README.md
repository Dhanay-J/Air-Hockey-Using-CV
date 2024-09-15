# Air-Hockey-Using-CV

This repository contains the code for a computer vision-based air hockey game developed using OpenCV and Python. The game is designed to be played using a webcam or other camera device, with the computer vision algorithm tracking the movement of the puck and paddles in real time. The goal is to provide a virtual air hockey experience by leveraging object detection techniques.

## Model Used

We have used a custom YOLOv8 model for **circle detection** to track the puck and paddles effectively during the game. The YOLOv8 model is chosen for its high speed and accuracy in detecting objects in real-time scenarios, making it ideal for a fast-paced game like air hockey.

## Dataset

A custom dataset was created for this project, specifically designed for detecting circular objects like pucks. The dataset was annotated using the **CVAT (Computer Vision Annotation Tool)** platform, which allows for efficient and precise labeling of objects. The dataset includes images of pucks and paddles from various angles and lighting conditions to ensure robust detection.

## Features

- **Real-Time Object Detection**: The game uses YOLOv8 to detect the puck and paddles in real-time, ensuring smooth gameplay.
- **Custom Dataset**: A dataset specifically built for detecting pucks and paddles, annotated using CVAT.
- **OpenCV Integration**: OpenCV is used for video capture, image processing, and displaying the game interface.
- **Camera-Based Control**: Players control their paddles using real-world objects tracked by the camera, adding an interactive layer to the game.
- **Collision Detection**: Implements basic physics for collision detection between the puck, paddles, and virtual table borders.

## Installation

### Our Work Environment

- **CPU**: Ryzen 5 5000 series
- **RAM**: 16 GB
- **GPU**: RTX 3050
- **OS**: Windows 11
- **Python**: 3.12.0

### Setup Guide

1. Clone the repository:

    ```bash
    git clone https://github.com/Dhanay-J/Air-Hockey-Using-CV.git
    cd Air-Hockey-Using-CV
    ```

2. (Optional but recommended) Set up a Python virtual environment:

    ```bash
    python -m venv env
    ```

3. Activate the environment:

    - For Windows:
    
        ```bash
        .\env\Scripts\activate
        ```

    - For Linux/MacOS:

        ```bash
        source env/bin/activate
        ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Alternatively, you can manually install the libraries:

```bash
pip install opencv-python
pip install ultralytics
pip install pygame
```

## Running the Game

To start the game, simply run:

```bash
python main.py
```

Make sure your webcam is connected and properly set up to detect the paddles and puck.

## Using Your Own Models

### Training and Testing Your Model

1. **Create your own dataset**:
    - You can collect and annotate your dataset using the [CVAT](https://app.cvat.ai/) or another annotation tool.
   
2. **Train the model**:
    - Use your custom dataset to train the YOLOv8 model. Adjust training parameters in `config.yaml` to match your dataset and hardware.

### Checking if the Detection Works

1. After training your model, use the provided script `yolo_test_run_model.py` to **check if the model detects the objects (puck and paddles)** correctly.
   - This script is used for a basic functionality test, ensuring the detection works as expected. It does **not** calculate any metrics like accuracy or precision.

2. To use the model in the game, pass the model's path as a parameter to the `Game` object:

    ```python
    game = Game(model_path="path/to/your/model.pt")
    ```

Replace `"path/to/your/model.pt"` with the actual path to your custom model.


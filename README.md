# Air-Hockey-Using-CV

This repository contains the code for a computer vision-based air hockey game developed using OpenCV and Python. The game is designed to be played using a webcam or other camera device, with the computer vision algorithm tracking the movement of the puck and paddles in real time. The goal is to provide a virtual air hockey experience by leveraging object detection techniques.

# Model Used

We have used a custom YOLOv8 model for circle detection to track the puck and paddles effectively during the game. The YOLOv8 model is chosen for its high speed and accuracy in detecting objects in real-time scenarios, making it ideal for a fast-paced game like air hockey.

# Dataset

A custom dataset was created for this project, specifically designed for detecting circular objects like pucks. The dataset was annotated using the CVAT (Computer Vision Annotation Tool) platform, which allows for efficient and precise labeling of objects. The dataset includes images of pucks and paddles from various angles and lighting conditions to ensure robust detection.

# Features

* Real-Time Object Detection: The game uses YOLOv8 to detect the puck and paddles in real-time, ensuring smooth gameplay.
* Custom Dataset: A dataset specifically built for detecting pucks and paddles, annotated using CVAT.
* OpenCV Integration: OpenCV is used for video capture, image processing, and displaying the game interface.
* Camera-Based Control: Players control their paddles using real-world objects that are tracked by the camera, adding an interactive layer to the game.
* Collision Detection: Implements basic physics for collision detection between the puck and paddles, as well as with the virtual borders of the table.


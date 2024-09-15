import cv2
import datetime
import os

# Function to capture video and write frames on 's' key press
def capture_and_write_frames(output_dir="./data/images/train"):
  # Set working directory (optional)
  os.chdir(output_dir)

  # Initialize video capture
  cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Change 0 to video file path if needed

  while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was not read, exit
    if not ret:
      print("Error: Failed to capture frame")
      break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Display the resulting frame (optional, can be commented out)
    cv2.imshow('frame', frame)

    # Wait for a key press with a short delay (1 millisecond)
    key = cv2.waitKey(1) & 0xFF

    # Exit if 'q' key is pressed
    if key == ord('q'):
      break

    # Write frame if 's' key is pressed
    if key == ord('s'):
        # Get current timestamp (optimize for filename construction)
        filename = f"frame_{datetime.datetime.now()}.jpg".replace(":", "-")
        # Write the frame to a file (consider compression)
        if cv2.imwrite(filename, frame, params=[cv2.IMWRITE_JPEG_QUALITY, 90]):
            print(f"Image saved: {filename}")
        else:
            print(f"Error: Failed to save image {filename}")
  # Release the capture and close all windows
  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  capture_and_write_frames()

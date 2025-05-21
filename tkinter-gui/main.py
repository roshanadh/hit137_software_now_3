"""
Question 1
You will develop a desktop application that demonstrates your understanding of Object-
Oriented Programming principles, GUI development using Tkinter, and image
processing using OpenCV.
You have the flexibility to design any user interface, provided it effectively supports all
required functionality.
Functional Requirements
1. Image Loading
    a. Select and load images, from the local device
    b. Display the loaded image in the application window
2. Image Cropping
    a. Draw a rectangle using mouse interaction for image cropping
    b. Provide real-time visual feedback of the selection area while drawing
    c. Display the cropped result alongside the original image
3. Image Resizing
    a. Slider control for resizing the cropped image
    b. Update the display in real-time as the user moves the slider
    4. Allow saving of the modified image
Optional
• Implement additional image processing features
• Add keyboard shortcuts
• Implement undo/redo functionality
"""

import tkinter as tk
from ImageEditor import ImageEditor

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()

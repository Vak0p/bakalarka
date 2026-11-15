# SurfaceSurfer

A GUI application for creating large-scale images (maps) of planar surfaces from video.

This project is a bachelor's thesis project. The current prototype focuses on loading a video and previewing its frames; image stitching and map creation are planned work and are not yet implemented.

## Run

On Windows, create the virtual environment, install dependencies, and launch the application:

```powershell
python -m venv venv
.\venv\Scripts\python -m pip install -r requirements.txt
.\run.bat
```

The application currently accepts MP4, MOV, AVI, MKV, and WebM videos.

## Thesis

**GUI application for creating huge photos (maps) from video of surface**  
Bachelor's thesis, Brno University of Technology, Faculty of Information Technology, 2026/2027  
Author: Vladimír Červenka · Supervisor: Ing. Pavol Dubovec

The thesis explores image stitching and GUI design, with the goal of designing and evaluating an application for creating large images of planar surfaces from video.

## Technologies

- **Python** is used for the application logic and to connect the user interface with video processing.
- **PySide6 (Qt for Python)** provides the desktop GUI. The window's visual design and layout were created in Qt Designer (`ui/main_window.ui`) and are compiled to Python when the application starts. Video preview frames are loaded in a background Qt worker so the interface remains responsive.
- **OpenCV** opens video files, reads their metadata and frames, and prepares sampled frames for the preview.
- **NumPy** stores and handles video frames as image arrays for conversion and display.
- **pyqtdarktheme-fork** supplies the dark Qt palette used by the application.
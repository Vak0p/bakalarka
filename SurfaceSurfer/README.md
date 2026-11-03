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
# Rubik's Cube photo solver

This first version reads six JPG photos and prints a solving sequence. It is reusable: each run can use a different cube.

## 1. Install Python packages

Open a terminal in this folder and run:

```powershell
py -m pip install -r requirements.txt
```

## 2. Take and save six photos

Use a standard 3×3 cube. Take one straight-on photo of each face, with the whole 3×3 grid visible, minimal glare, and the grid filling most of the image. Keep the cube's top edge at the top of the photo for the four side faces.

Save the photos in this exact order and orientation:

| File | Face | Photo orientation |
|---|---|---|
| `1.jpg` | U (top) | Look straight at the top face; the edge touching the cube's front face is at the bottom of the photo. |
| `2.jpg` | R (right) | Look straight at the right face; keep the cube's top edge at the top of the photo and front edge on the left. |
| `3.jpg` | F (front) | Look straight at the front face; top edge at top. |
| `4.jpg` | D (bottom) | Look straight at the bottom face; the edge touching the front face is at the top of the photo. |
| `5.jpg` | L (left) | Look straight at the left face; keep the cube's top edge at the top of the photo and front edge on the right. |
| `6.jpg` | B (back) | Look straight at the back face; top edge at top. |

The filename order is fixed, but the colors can be anything. The program uses each face's center sticker to learn that cube's color scheme.

## 3. Run

```powershell
py solve_cube.py --folder "C:\path\to\your\photos"
```

If the photos are in this folder, run:

```powershell
py solve_cube.py
```

## Move notation

`R`, `L`, `U`, `D`, `F`, `B` mean turn that face clockwise as you look directly at it. An apostrophe means counter-clockwise (`R'`); `2` means a half turn (`U2`). Keep the cube oriented consistently while following the sequence.

## Notes

This version assumes the photos are already straight, square-on views of individual faces and that the grid occupies most of each image. Strong shadows, glare, stickers with unusual colors, or incorrect face rotation can cause a scan error. If the solver reports an invalid cube, retake the photos in the listed order. It does not yet automatically find a 3×3 grid in arbitrary camera photos.

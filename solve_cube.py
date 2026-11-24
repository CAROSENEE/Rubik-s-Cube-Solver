from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import kociemba
import numpy as np

# The six photos must be in this order: U, R, F, D, L, B.
FACE_ORDER = "URFDLB"


def sample_grid(image: np.ndarray) -> list[tuple[int, int, int]]:
    """Sample a small central patch in each cell of a square 3x3 face photo."""
    h, w = image.shape[:2]
    if min(h, w) < 90:
        raise ValueError("image is too small")
    # Ignore outer borders/background and sample the middle area of each sticker.
    colors = []
    for row in range(3):
        for col in range(3):
            x0, x1 = int((col + 0.32) * w / 3), int((col + 0.68) * w / 3)
            y0, y1 = int((row + 0.32) * h / 3), int((row + 0.68) * h / 3)
            patch = image[y0:y1, x0:x1]
            # Median is less affected by glare and small marks than a single pixel.
            b, g, r = np.median(patch.reshape(-1, 3), axis=0)
            colors.append((int(r), int(g), int(b)))
    return colors


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    # Compare in HSV so brightness changes matter less than hue for colored stickers.
    aa = cv2.cvtColor(np.uint8([[a[::-1]]]), cv2.COLOR_BGR2HSV)[0, 0].astype(float)
    bb = cv2.cvtColor(np.uint8([[b[::-1]]]), cv2.COLOR_BGR2HSV)[0, 0].astype(float)
    dh = min(abs(aa[0] - bb[0]), 180 - abs(aa[0] - bb[0])) * 2
    return float(dh * dh + (aa[1] - bb[1]) ** 2 * 0.35 + (aa[2] - bb[2]) ** 2 * 0.15)


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve a Rubik's Cube from six face photos.")
    parser.add_argument("--folder", default=".", help="folder containing 1.jpg ... 6.jpg")
    args = parser.parse_args()
    folder = Path(args.folder)

    face_samples: dict[str, list[tuple[int, int, int]]] = {}
    for filename, face in zip(range(1, 7), FACE_ORDER):
        path = folder / f"{filename}.jpg"
        image = cv2.imread(str(path))
        if image is None:
            raise SystemExit(f"Could not open {path}. Use JPG files named 1.jpg through 6.jpg.")
        face_samples[face] = sample_grid(image)

    # The center sticker identifies the face color. This works with any color scheme.
    centers = {face: face_samples[face][4] for face in FACE_ORDER}
    center_list = list(centers.items())
    if len({face for face, _ in center_list}) != 6:
        raise SystemExit("Could not identify six different face centers.")

    facelets = []
    counts = {face: 0 for face in FACE_ORDER}
    for face in FACE_ORDER:
        for color in face_samples[face]:
            nearest = min(FACE_ORDER, key=lambda candidate: color_distance(color, centers[candidate]))
            facelets.append(nearest)
            counts[nearest] += 1

    if any(count != 9 for count in counts.values()):
        raise SystemExit(
            "The colors do not form six groups of nine. Check lighting, photo order, and image orientation. "
            f"Counts: {counts}"
        )

    state = "".join(facelets)
    try:
        solution = kociemba.solve(state)
    except Exception as exc:
        raise SystemExit(
            "The scanned colors do not describe a solvable cube. Check that each photo shows one complete face "
            "and that the photo order/orientation matches README.md.\nDetails: " + str(exc)
        )

    print("Solution (turn the face as viewed straight-on):")
    print(solution)
    print("\nMoves:")
    for number, move in enumerate(solution.split(), start=1):
        print(f"{number:2}. {move}")
    print("\nNotation: R/L/U/D/F/B = clockwise quarter-turn; ' = counter-clockwise; 2 = half-turn.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

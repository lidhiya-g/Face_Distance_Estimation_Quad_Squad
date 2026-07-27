# Face_Distance_Estimation_Quad_Squad
Monocular Face Distance Estimator — Real-time face depth ($Z$) and horizontal deviation angle ($\theta$) estimation using a single 2D camera feed and MediaPipe. Built on the pinhole camera model to calculate real-world spatial coordinates $(Z, \theta)$ with $\pm50\text{–}150\text{ cm}$ accuracy without requiring depth sensors.

# Monocular Face Distance & Angle Estimator

A real-time Python implementation for estimating face depth ($Z$) and horizontal deviation angle ($\theta$) from a single 2D camera feed using the pinhole camera model.

## 📌 Mathematical Model

This project uses the pinhole camera geometric model:

1. **Depth Estimation ($Z$)**:
   $$Z = \frac{f \times W}{w_{px}}$$
   - $f$: Camera focal length in pixels
   - $W$: Average real-world face width (~0.15 meters)
   - $w_{px}$: Detected face width in image pixels

2. **Horizontal Angle Deviation ($\theta$)**:
   $$\theta = \arctan\left(\frac{x - c_x}{f}\right)$$
   - $x$: X-coordinate of the face center in pixels
   - $c_x$: Image center X-coordinate ($W_{img} / 2$)

---

## 🛠️ Parameters & Assumptions

| Parameter | Meaning | Units / Form |
| :--- | :--- | :--- |
| `(x, y)` | Detected face center | pixels |
| `w_px` | Face width in image | pixels |
| `f` | Camera focal length | pixels |
| `(c_x, c_y)` | Image principal point (center) | pixels |
| `W` | Real face width | meters (~0.14 - 0.16 m) |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system.

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/YOUR_USERNAME/monocular-face-distance-estimator.git](https://github.com/YOUR_USERNAME/monocular-face-distance-estimator.git)
cd monocular-face-distance-estimator
pip install -r requirements.txt
```

### 3. Running the Estimator
Run the live webcam tracking script:

```bash
python main.py
```

Press **`q`** to terminate the stream.

---

## 📊 Expected Output Format

The system calculates and outputs a tuple for each detected face in real-time:

$$\text{Output} = (Z, \theta)$$

Example CLI output:
```text
(depth, theta) = (0.65 m, -8.32°)
(depth, theta) = (1.20 m, 12.15°)
```

import os
import json

def create_test_structure():
    """
    Crea una estructura de archivos de prueba para el analisis de metricas
    """
    base_path = "/data/Detect_Lines"
    os.makedirs(base_path, exist_ok=True)
    
    print(f"Creando estructura de prueba en: {base_path}")
    
    # Archivos Python de ejemplo
    python_files = [
        ("line_detector.py", '''import cv2
import numpy as np
import matplotlib.pyplot as plt

class LineDetector:
    def __init__(self):
        self.min_line_length = 50
        self.max_line_gap = 10
    
    def detect_lines(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                              minLineLength=self.min_line_length,
                              maxLineGap=self.max_line_gap)
        return lines
    
    def draw_lines(self, image, lines):
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image

def main():
    detector = LineDetector()
    print("Line detector initialized successfully")

if __name__ == "__main__":
    main()
'''),

        ("image_processor.py", '''import numpy as np
from PIL import Image
import json

class ImageProcessor:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"default_parameters": True}
    
    def preprocess_image(self, image_array):
        normalized = image_array / 255.0
        processed = self.apply_gaussian_filter(normalized)
        return processed
    
    def apply_gaussian_filter(self, image):
        kernel_size = 5
        return image

    def calculate_metrics(self, detection_results):
        total_lines = len(detection_results)
        avg_length = np.mean([r['length'] for r in detection_results]) if detection_results else 0
        return {
            "total_lines": total_lines,
            "average_length": avg_length,
            "detection_time": "0.5s"
        }
'''),

        ("utils.py", '''import os
import json
import datetime
from typing import List, Dict

def get_file_list(directory: str, extensions: List[str] = None) -> List[str]:
    if extensions is None:
        extensions = ['.py', '.json', '.yaml', '.txt']
    
    file_list = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in extensions):
            file_list.append(os.path.join(directory, file))
    
    return file_list

def save_results(results: Dict, filename: str):
    results['timestamp'] = datetime.datetime.now().isoformat()
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {filename}")

def load_config(config_file: str) -> Dict:
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_file} not found, using defaults")
        return {}

def validate_image_path(image_path: str) -> bool:
    return os.path.exists(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg'))
''')
    ]
    
    # Archivos de configuracion
    config_files = [
        ("config.json", '''{
    "model_parameters": {
        "detection_threshold": 0.8,
        "max_line_gap": 10,
        "min_line_length": 50,
        "hough_threshold": 80
    },
    "image_processing": {
        "resize_width": 800,
        "resize_height": 600,
        "blur_kernel": 5,
        "canny_threshold1": 50,
        "canny_threshold2": 150
    },
    "output_settings": {
        "save_detections": true,
        "output_format": "json",
        "visualize_results": true
    }
}
'''),

        ("parameters.yaml", '''training:
  model_name: "line_detection_cnn"
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
  optimizer: "adam"

data:
  input_shape: [600, 800, 3]
  augmentation: true
  train_test_split: 0.8

evaluation:
  metrics: ["precision", "recall", "f1_score"]
  validation_steps: 50
  early_stopping_patience: 10
''')
    ]
    
    # Archivos de datos y documentacion
    other_files = [
        ("requirements.txt", '''numpy==1.24.0
opencv-python==4.7.0
matplotlib==3.7.0
Pillow==9.5.0
scikit-image==0.20.0
'''),

        ("README.md", '''# Line Detection Project

Este proyecto implementa un sistema de deteccion de lineas en imagenes usando computer vision.

## Caracteristicas

- Deteccion de lineas usando transformada de Hough
- Procesamiento de imagenes con OpenCV
- Configuracion flexible via archivos JSON/YAML
- Metricas de evaluacion integradas

## Uso

```python
from line_detector import LineDetector

detector = LineDetector()
lines = detector.detect_lines('image.jpg')
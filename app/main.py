import os
import sys
import json
from datetime import datetime

# Agregar el directorio actual al path para los imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app.file_analyzer import FileAnalyzer
from app.metrics_calculator import MetricsCalculator

def create_test_data_if_needed(base_path):
    """Crea datos de prueba si el directorio esta vacio"""
    if not os.path.exists(base_path):
        print(f"Creando directorio: {base_path}")
        os.makedirs(base_path, exist_ok=True)
    
    if not os.listdir(base_path):
        print("Creando datos de prueba...")
        
        test_files = [
            ("line_detector.py", "# Line detection module\nimport cv2\nimport numpy as np\n\nclass LineDetector:\n    def detect_lines(self, image):\n        return []"),
            ("config.json", '{"model": "cnn", "epochs": 100}'),
            ("requirements.txt", "opencv-python\nnumpy\ntensorflow"),
            ("train_model.py", "# Training script\nprint('Training model...')"),
            ("utils.py", "# Utility functions\ndef load_image(path):\n    return None")
        ]
        
        for filename, content in test_files:
            filepath = os.path.join(base_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Creado: {filename}")
        
        print("Datos de prueba creados")

class ThesisMetricsApp:
    def __init__(self):
        # USAR TU PATH ESPECÍFICO DE WINDOWS
        self.base_path = r'C:\Users\omarg\OneDrive\Documentos\Proyect_Thesis\Detect_Lines'
        self.analyzer = FileAnalyzer()
        self.metrics_calc = MetricsCalculator()
    
    def run_analysis(self):
        print(f"Iniciando analisis en: {self.base_path}")
        
        # Crear directorio y datos de prueba si no existen
        create_test_data_if_needed(self.base_path)
        
        if not os.path.exists(self.base_path):
            print(f"Error: El directorio {self.base_path} no existe")
            print("Directorios disponibles en el directorio padre:")
            parent_dir = os.path.dirname(self.base_path)
            if os.path.exists(parent_dir):
                for item in os.listdir(parent_dir)[:10]:  # Mostrar primeros 10
                    print(f"  - {item}")
            return None
        
        file_metrics = self.analyzer.analyze_directory(self.base_path)
        
        if not file_metrics:
            print("No se encontraron archivos para analizar")
            return None
            
        summary = self.metrics_calc.calculate_summary(file_metrics)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_path": self.base_path,
            "file_metrics": file_metrics,
            "summary": summary
        }
        
        self.save_results(results)
        self.print_summary(summary)
        
        return results
    
    def save_results(self, results):
        output_dir = './output'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"metrics_{timestamp}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados guardados en: {output_file}")
    
    def print_summary(self, summary):
        print("\n" + "="*50)
        print("RESUMEN DE METRICAS")
        print("="*50)
        print(f"Total de archivos: {summary['total_files']}")
        print(f"Total de lineas de codigo: {summary['total_lines']}")
        print(f"Archivos por tipo:")
        for file_type, count in summary['files_by_type'].items():
            print(f"  {file_type}: {count}")
        if summary['total_files'] > 0:
            print(f"Tamaño total: {summary['total_size_mb']:.2f} MB")
            print(f"Archivo mas grande: {summary['largest_file']['path']}")
            print(f"Archivo con mas lineas: {summary['file_with_most_lines']['path']}")

if __name__ == "__main__":
    app = ThesisMetricsApp()
    app.run_analysis()
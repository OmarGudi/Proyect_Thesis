import os
import json
from datetime import datetime
from app.file_analyzer import FileAnalyzer
from app.metrics_calculator import MetricsCalculator

class ThesisMetricsApp:
    def __init__(self):
        # Usar variable de entorno o path por defecto
        self.base_path = os.getenv('ANALYSIS_PATH', '/data/Detect_Lines')
        self.analyzer = FileAnalyzer()
        self.metrics_calc = MetricsCalculator()
    
    def run_analysis(self):
        print(f"Iniciando analisis en: {self.base_path}")
        
        if not os.path.exists(self.base_path):
            print(f"Error: El directorio {self.base_path} no existe")
            print("Directorios disponibles:")
            for root, dirs, files in os.walk('/'):
                print(f"  {root}")
                if len(dirs) > 0:
                    for d in dirs[:5]:  # Mostrar solo primeros 5
                        print(f"    - {d}")
                break  # Solo mostrar root
            return None
        
        file_metrics = self.analyzer.analyze_directory(self.base_path)
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
        output_dir = os.getenv('OUTPUT_DIR', '/output')
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
        print(f"Tamaño total: {summary['total_size_mb']:.2f} MB")
        print(f"Archivo mas grande: {summary['largest_file']['path']}")
        print(f"Archivo con mas lineas: {summary['file_with_most_lines']['path']}")

if __name__ == "__main__":
    app = ThesisMetricsApp()
    app.run_analysis()
import os
import json

def create_test_structure():
    """
    Crea una estructura de archivos de prueba para el analisis de metricas
    """
    base_path = "/data/Detect_Lines"
    os.makedirs(base_path, exist_ok=True)
    
    print("Creando estructura de prueba en: " + base_path)
    
    # Archivos simples sin contenido complejo
    files_to_create = [
        ("line_detector.py", "print('Line detector module')"),
        ("image_processor.py", "print('Image processor module')"),
        ("utils.py", "print('Utils module')"),
        ("config.json", '{"model": "cnn", "epochs": 100}'),
        ("parameters.yaml", "model: cnn\nepochs: 100"),
        ("requirements.txt", "numpy\nopencv-python\nmatplotlib"),
        ("README.md", "# Project\nLine detection project"),
        ("data_analysis.py", "print('Data analysis module')")
    ]
    
    # Crear archivos principales
    for filename, content in files_to_create:
        filepath = os.path.join(base_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Creado: " + filepath)
    
    # Crear subdirectorio
    subdir_path = os.path.join(base_path, "models")
    os.makedirs(subdir_path, exist_ok=True)
    
    # Archivo en subdirectorio
    model_file = os.path.join(subdir_path, "model_architecture.py")
    with open(model_file, 'w') as f:
        f.write("print('Model architecture')")
    
    print("Creado: " + model_file)
    print("Estructura de prueba creada exitosamente")
    print("Total de archivos creados: " + str(len(files_to_create) + 1))

if __name__ == "__main__":
    create_test_structure()
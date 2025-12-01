import os
import fnmatch
from typing import List, Dict, Any

class FileAnalyzer:
    def __init__(self):
        self.python_patterns = ['*.py']
        self.config_patterns = ['*.json', '*.yaml', '*.yml', '*.xml', '*.config']
        self.document_patterns = ['*.md', '*.txt', '*.rst', '*.html', '*.css', '*.js']
        self.data_patterns = ['*.csv', '*.jsonl', '*.tsv', '*.dat']
    
    def analyze_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        file_metrics = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                metrics = self.analyze_file(file_path)
                if metrics:
                    file_metrics.append(metrics)
        
        return file_metrics
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        try:
            file_stats = os.stat(file_path)
            file_type = self.classify_file_type(file_path)
            line_count = self.count_lines(file_path)
            
            return {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_type': file_type,
                'size_bytes': file_stats.st_size,
                'line_count': line_count,
                'created_time': file_stats.st_ctime,
                'modified_time': file_stats.st_mtime
            }
        except (OSError, IOError) as e:
            print(f"Error analizando archivo {file_path}: {str(e)}")
            return None
    
    def classify_file_type(self, file_path: str) -> str:
        file_ext = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path).lower()
        
        if any(fnmatch.fnmatch(file_name, pattern) for pattern in self.python_patterns):
            return 'python'
        elif any(fnmatch.fnmatch(file_name, pattern) for pattern in self.config_patterns):
            return 'config'
        elif any(fnmatch.fnmatch(file_name, pattern) for pattern in self.document_patterns):
            return 'document'
        elif any(fnmatch.fnmatch(file_name, pattern) for pattern in self.data_patterns):
            return 'data'
        elif file_ext in ['.py']:
            return 'python'
        elif file_ext in ['.json', '.yaml', '.yml', '.xml']:
            return 'config'
        elif file_ext in ['.md', '.txt', '.rst']:
            return 'document'
        elif file_ext in ['.csv', '.jsonl', '.tsv']:
            return 'data'
        else:
            return 'other'
    
    def count_lines(self, file_path: str) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except (OSError, IOError, UnicodeDecodeError) as e:
            print(f"Error contando lineas en {file_path}: {str(e)}")
            return 0
from typing import List, Dict, Any

class MetricsCalculator:
    def calculate_summary(self, file_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not file_metrics:
            return self.empty_summary()
        
        total_files = len(file_metrics)
        total_lines = sum(fm['line_count'] for fm in file_metrics)
        total_size_bytes = sum(fm['size_bytes'] for fm in file_metrics)
        
        files_by_type = {}
        for fm in file_metrics:
            file_type = fm['file_type']
            files_by_type[file_type] = files_by_type.get(file_type, 0) + 1
        
        largest_file = max(file_metrics, key=lambda x: x['size_bytes'])
        file_with_most_lines = max(file_metrics, key=lambda x: x['line_count'])
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'total_size_bytes': total_size_bytes,
            'total_size_mb': total_size_bytes / (1024 * 1024),
            'files_by_type': files_by_type,
            'largest_file': {
                'path': largest_file['file_path'],
                'size_bytes': largest_file['size_bytes'],
                'size_mb': largest_file['size_bytes'] / (1024 * 1024)
            },
            'file_with_most_lines': {
                'path': file_with_most_lines['file_path'],
                'lines': file_with_most_lines['line_count']
            },
            'average_lines_per_file': total_lines / total_files if total_files > 0 else 0,
            'average_file_size_mb': (total_size_bytes / total_files) / (1024 * 1024) if total_files > 0 else 0
        }
    
    def empty_summary(self) -> Dict[str, Any]:
        return {
            'total_files': 0,
            'total_lines': 0,
            'total_size_bytes': 0,
            'total_size_mb': 0,
            'files_by_type': {},
            'largest_file': {'path': '', 'size_bytes': 0, 'size_mb': 0},
            'file_with_most_lines': {'path': '', 'lines': 0},
            'average_lines_per_file': 0,
            'average_file_size_mb': 0
        }
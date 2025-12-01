import unittest
import tempfile
import os
from app.file_analyzer import FileAnalyzer

class TestFileAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FileAnalyzer()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_classify_file_type(self):
        test_cases = [
            ('script.py', 'python'),
            ('config.json', 'config'),
            ('readme.md', 'document'),
            ('data.csv', 'data'),
            ('unknown.xyz', 'other')
        ]
        
        for filename, expected_type in test_cases:
            file_path = os.path.join(self.temp_dir, filename)
            with open(file_path, 'w') as f:
                f.write('test content')
            
            actual_type = self.analyzer.classify_file_type(file_path)
            self.assertEqual(actual_type, expected_type)
    
    def test_count_lines(self):
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')
        
        line_count = self.analyzer.count_lines(test_file)
        self.assertEqual(line_count, 3)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
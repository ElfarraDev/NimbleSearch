import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nimble_search import NimbleSearch

class TestNimbleSearch(unittest.TestCase):
    def setUp(self):
        self.docs = [
            {'title': 'Python Programming', 'content': 'Python is a versatile programming language.', 'category': 'Programming'},
            {'title': 'Data Science with Python', 'content': 'Python is widely used in data science.', 'category': 'Data Science'},
            {'title': 'Web Development', 'content': 'Web development involves creating websites and web applications.', 'category': 'Web'},
        ]
        self.index = NimbleSearch(text_fields=['title', 'content'], keyword_fields=['category'])
        self.index.fit(self.docs)

    def test_search(self):
        results = self.index.search('Python')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Python Programming')

    def test_filter(self):
        results = self.index.search('Python', filter_dict={'category': 'Data Science'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Data Science with Python')

    def test_add_document(self):
        new_doc = {'title': 'Machine Learning', 'content': 'Machine learning is a subset of AI.', 'category': 'AI'}
        self.index.add_document(new_doc)
        results = self.index.search('AI')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Machine Learning')

    def test_remove_document(self):
        self.index.remove_document(0)
        results = self.index.search('Python')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Data Science with Python')

if __name__ == '__main__':
    unittest.main()

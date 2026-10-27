"""
Test module to check if README.md exists and contains essential information.
"""

import unittest
import os

class TestReadme(unittest.TestCase):
    """
    Test case to check README.md.
    """
    
    def test_readme_exists(self):
        """
        Test if README.md exists.
        """
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')))
    
    def test_readme_contains_essential_info(self):
        """
        Test if README.md contains essential project information.
        """
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
        
        with open(readme_path, 'r') as f:
            content = f.read().lower()
            
            # Test all required sections (using case-insensitive checks)
            self.assertIn('adventure game', content)
            self.assertIn('installation', content)
            
            # Look for either "usage" or related terms like "running the game"
            usage_terms = ['usage', 'how to use', 'how to play', 'running the game', 'run the game', 'game controls']
            has_usage = any(term in content for term in usage_terms)
            self.assertTrue(has_usage, "README should contain usage instructions")
            
            # Look for game controls specifically
            self.assertIn('controls', content)

if __name__ == '__main__':
    unittest.main()
from django.forms import ValidationError
from apps.accounts.validators import validate_name
from django.test import TestCase

class NameValidatorTests(TestCase):
    def test_validate_name(self):
        # Test valid names
        valid_names = ['Alice', 'Bob', 'Charlie']
        for name in valid_names:
            try:
                result = validate_name(name)
                self.assertEqual(result, name)
            except ValidationError:
                self.fail(f"validate_name raised ValidationError unexpectedly for valid name: {name}")
                
        # Test names with spaces
        invalid_names = ['Alice Johnson', 'Bob Smith']
        for name in invalid_names:
            with self.assertRaises(ValidationError) as cm:
                validate_name(name)
            self.assertIn("No spaces between names", cm.exception)
            
        # Test names with non-alpha characters
        invalid_names = ['Alice123', 'Bob@Smith']
        for name in invalid_names:
            with self.assertRaises(ValidationError) as cm:
                validate_name(name)
            self.assertIn("Alphabetical characters only", cm.exception)
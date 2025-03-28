from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from industries.models import Industry
from django.utils import timezone


class IndustryModelTests(TestCase):
    """
    Comprehensive test suite for Industry model validation.
    Validates field constraints, uniqueness requirements, and model behavior.
    """
    def setUp(self):
        """
        Initialize test data for consistent model validation.
        """
        self.valid_industry_data = {
            'name': 'Technology',
            'description': 'Software and hardware development industries'
        }

    def test_industry_creation(self):
        """
        Verify basic industry creation with valid data.
        """
        industry = Industry.objects.create(**self.valid_industry_data)
        
        # Verify field values
        self.assertEqual(industry.name, self.valid_industry_data['name'])
        self.assertEqual(industry.description, self.valid_industry_data['description'])
        
        # Verify timestamps are set
        self.assertIsNotNone(industry.created_at)
        self.assertIsNotNone(industry.updated_at)
        
        # Verify timestamps are within expected timeframe (last minute)
        now = timezone.now()
        self.assertLess((now - industry.created_at).total_seconds(), 60)
        self.assertLess((now - industry.updated_at).total_seconds(), 60)
    
    def test_name_unique_constraint(self):
        """
        Verify unique constraint on industry name field.
        """
        # Create first industry
        Industry.objects.create(**self.valid_industry_data)
        
        # Attempt to create second industry with same name
        with self.assertRaises(IntegrityError):
            Industry.objects.create(
                name=self.valid_industry_data['name'],
                description='Different description'
            )
    
    def test_name_max_length(self):
        """
        Verify name field length constraint.
        """
        # Test with name at maximum length (50 chars)
        max_length_name = 'X' * 50
        industry = Industry(name=max_length_name)
        industry.full_clean()  # Should not raise exception
        
        # Test with name exceeding maximum length
        excessive_length_name = 'X' * 51
        industry = Industry(name=excessive_length_name)
        with self.assertRaises(ValidationError):
            industry.full_clean()
    
    def test_description_blank(self):
        """
        Verify description field can be blank.
        """
        industry_blank_desc = Industry.objects.create(
            name='Finance',
            description=''
        )
        self.assertEqual(industry_blank_desc.description, '')
        
        industry_no_desc = Industry.objects.create(
            name='Healthcare'
        )
        self.assertEqual(industry_no_desc.description, '')
    
    def test_string_representation(self):
        """
        Verify __str__ method returns the expected string.
        """
        industry = Industry.objects.create(**self.valid_industry_data)
        self.assertEqual(str(industry), self.valid_industry_data['name'])
    
    def test_verbose_name_plural(self):
        """
        Verify Meta class sets correct verbose_name_plural.
        """
        self.assertEqual(Industry._meta.verbose_name_plural, 'Industries')
    
    def test_update_timestamp(self):
        """
        Verify updated_at field updates automatically.
        """
        industry = Industry.objects.create(**self.valid_industry_data)
        original_updated_at = industry.updated_at
        
        # Force a delay to ensure timestamp difference
        import time
        time.sleep(1)
        
        # Update the industry
        industry.description = 'Updated description'
        industry.save()
        
        # Verify updated_at has changed
        self.assertNotEqual(industry.updated_at, original_updated_at)
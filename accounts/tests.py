from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class CustomUserModelTests(TestCase):
    """
    Test suite for verifying the functionality of the CustomUser model.
    Focuses on standard validation patterns and constraints.
    """
    
    def setUp(self):
        """
        Establish baseline test data for consistent validation across test methods.
        """
        self.User = get_user_model()
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'name': 'Test User'
        }
    
    def test_create_user(self):
        """
        Verify basic user creation with all required fields.
        """
        user = self.User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password'],
            name=self.test_user_data['name']
        )
        
        self.assertEqual(user.username, self.test_user_data['username'])
        self.assertEqual(user.email, self.test_user_data['email'])
        self.assertEqual(user.name, self.test_user_data['name'])
        self.assertTrue(user.check_password(self.test_user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """
        Verify superuser creation with appropriate permission flags.
        """
        admin_user = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123',
            name='Admin User'
        )
        
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)
    
    def test_username_unique_constraint(self):
        """
        Verify that username uniqueness constraint is enforced.
        """
        self.User.objects.create_user(
            username=self.test_user_data['username'],
            email='first@example.com',
            password='password123'
        )
        
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username=self.test_user_data['username'],
                email='second@example.com',
                password='password123'
            )
    
    def test_email_accepts_valid_formats(self):
        """
        Verify that properly formatted email addresses are accepted.
        """
        valid_emails = [
            'user@example.com',
            'first.last@domain.co.uk',
            'name+tag@example.org'
        ]
        
        for email in valid_emails:
            user = self.User(
                username=f"user_{email.split('@')[0]}",
                email=email,
                password='password123'
            )
            try:
                user.full_clean()  # Triggers validation
                self.assertTrue(True)  # Validation passed
            except ValidationError:
                self.fail(f"Validation failed for valid email: {email}")
    
    def test_name_field_optional(self):
        """
        Verify that name field can be null or blank as defined in the model.
        """
        user = self.User.objects.create_user(
            username='user_without_name',
            email='noname@example.com',
            password='password123'
        )
        
        self.assertIsNone(user.name)
        
        user = self.User.objects.create_user(
            username='user_empty_name',
            email='emptyname@example.com',
            password='password123',
            name=''
        )
        
        self.assertEqual(user.name, '')
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

class UserPermissionsTest(TestCase):

    def setUp(self):
        # Create admin user
        self.admin = User.objects.create_superuser(username='admin', password='1234')

        # Create regular users
        self.meirzhan = User.objects.create_user(username='meirzhan', password='1234')
        self.john = User.objects.create_user(username='john', password='1234')

        # Create APIClient instance for testing
        self.client = APIClient()

    def test_admin_access(self):
        """Test that only admin can access admin views."""
        # Log in as admin
        self.client.login(username='admin', password='1234')

        # Make request to the view that requires admin access
        response = self.client.get('/admin/')  # Change to a real admin view
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meirzhan_access(self):
        """Test that regular users cannot access admin views."""
        # Log in as Meirzhan
        self.client.login(username='meirzhan', password='1234')

        # Make request to the view that requires admin access
        response = self.client.get('/movies/12/')  # Change to a restricted view
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_john_access(self):
        """Test that another regular user cannot access admin views."""
        # Log in as John
        self.client.login(username='john', password='1234')

        # Make request to the view that requires admin access
        response = self.client.get('/movies/12/')  # Change to a restricted view
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access admin views."""
        # Make request without logging in
        response = self.client.get('/movies/12/')  # Change to a restricted view
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

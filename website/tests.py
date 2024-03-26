from django.test import TestCase
from django.urls import reverse
from .models import Record
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.record = Record.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            phone='1234567890',
            address='123 Main St',
            city='Anytown',
            state='Anystate',
            zipcode='12345'
        )

    def test_home_view_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        print("Home view test passed")

    def test_customer_record_view_GET(self):
        response = self.client.get(reverse('record', kwargs={'pk': self.record.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        print("Customer record view test passed")

    def test_add_record_view_GET(self):
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_record.html')
        print("Add record view test passed")

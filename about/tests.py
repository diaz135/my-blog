from django.test import TestCase
from django.urls import reverse
from website.models import Contact, Curriculum, Presentation, SiteInfo
from django.core.validators import validate_email
from django.http import JsonResponse

# --- Tests Unitaires ---

class ContactModelTest(TestCase):
    def test_create_contact(self):
        contact = Contact.objects.create(
            nom="John Doe",
            email="johndoe@example.com",
            subject="Inquiry",
            telephone="1234567890",
            message="This is a test message."
        )
        self.assertEqual(contact.nom, "John Doe")
        self.assertEqual(contact.email, "johndoe@example.com")
        self.assertEqual(contact.subject, "Inquiry")
        self.assertEqual(contact.telephone, "1234567890")
        self.assertEqual(contact.message, "This is a test message.")

# --- Tests d'Intégration ---

class AboutPageTest(TestCase):
    def setUp(self):
        SiteInfo.objects.create(name="Test Site", status=True)
        Presentation.objects.create(titre="About Us", description="<p>Test description</p>", status=True)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')
        self.assertContains(response, 'Test description')

class AuthorPageTest(TestCase):
    def setUp(self):
        SiteInfo.objects.create(name="Test Site", status=True)
        Curriculum.objects.create(nom="John Doe", description="<p>Curriculum description</p>", status=True)

    def test_author_page(self):
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Curriculum description')

# --- Tests Fonctionnels ---

class ContactFormFunctionalTest(TestCase):
    def test_valid_contact_submission(self):
        response = self.client.post(reverse('is_contact'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'l\'enregistrement a bien été effectué')

    def test_invalid_contact_submission(self):
        response = self.client.post(reverse('is_contact'), {
            'name': 'John Doe',
            'email': 'invalidemail',
            'subject': 'Test Subject',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email incorrect')

# --- Test de la méthode is_contact (formulaire de contact) ---

class ContactFormTest(TestCase):
    def test_is_contact_valid(self):
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'l\'enregistrement a bien été effectué')

    def test_is_contact_invalid_email(self):
        data = {
            'name': 'John Doe',
            'email': 'invalidemail',
            'subject': 'Test Subject',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email incorrect')

# --- Test de l'enregistrement du contact via la méthode is_contact ---

class IsContactTest(TestCase):
    def test_contact_submission_valid(self):
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Inquiry',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], "l'enregistrement a bien été effectué")

    def test_contact_submission_invalid_email(self):
        data = {
            'name': 'John Doe',
            'email': 'invalidemail',
            'subject': 'Inquiry',
            'tel': '1234567890',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], "email incorrect")

# --- Locust pour tests de performance (si nécessaire) ---

from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def test_about_page(self):
        self.client.get("/about")

    @task
    def test_contact_page(self):
        self.client.get("/contact")


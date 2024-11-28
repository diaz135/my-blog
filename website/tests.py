import pytest
from django.test import Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from website.models import SiteInfo, Publication, Newsletter
from elenizado.models import Publication as ElenizadoPublication  # Assurez-vous d'importer correctement les modèles nécessaires
from about.models import Gallerie


@pytest.mark.django_db
def test_index_view():
    """Test for the index view"""
    client = Client()

    # Create some dummy data for testing the index view
    site_info = SiteInfo.objects.create(
        email="test@example.com",
        nom="My Site",
        telephone=123456789,
        description="A description of the site",
        logo="path/to/logo.jpg"
    )

    # Create some publications for testing the view
    for i in range(10):
        ElenizadoPublication.objects.create(
            title=f"Publication {i}",
            content="Test content"
        )

    # Create dummy data for gallerie
    for i in range(5):
        Gallerie.objects.create(
            title=f"Gallerie {i}",
            content="Test gallery content",
            status=True
        )

    # Create a page for testing the view
    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert 'publication_r' in response.context
    assert 'events_r' in response.context
    assert 'gallerie' in response.context
    assert 'site_info' in response.context
    assert 'pub' in response.context

    # Check if pagination is working
    assert len(response.context['pub']) == 4  # Verify the number of publications displayed per page
    assert response.context['pub'][0].title == "Publication 9"  # Ensure the latest publication is displayed


@pytest.mark.django_db
def test_is_newsletter():
    """Test for subscribing to the newsletter"""
    client = Client()

    # Test valid email
    data = {'email': 'test@example.com'}
    response = client.post(reverse('is_newsletter'), data)

    # Verify that the email is saved in the newsletter
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['message'] == "l'enregistrement a bien été effectué"
    assert Newsletter.objects.filter(email='test@example.com').exists()

    # Test invalid email
    data = {'email': 'invalid-email'}
    response = client.post(reverse('is_newsletter'), data)

    assert response.status_code == 200
    assert response.json()['success'] is False
    assert response.json()['message'] == "email incorrect"

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.urls import reverse
from .views import signup
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your tests here.
class SignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolve_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

class SuccessfullSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username':' aseyed',
            'password1': 'qwerty123456',
            'password2': 'qwerty123456'
        }
        self.response = self.client.post(url, data)
        self.homepage_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.homepage_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.homepage_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated) 

class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
    
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


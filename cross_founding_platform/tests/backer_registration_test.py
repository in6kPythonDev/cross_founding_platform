from unittest import TestCase
from registration.models import RegistrationProfile

from django.contrib.auth.models import User
from django.core import mail
from django.test import Client

#print >> sys.stderr,
import sys

REGISTER_URI = "/accounts/register/"
LOGIN_URI = "/accounts/login/"
PASSWORD_RESET_URI = '/accounts/password/reset/'
ACCOUNTS_RESET_CONFIRM_URI = '/accounts/password/reset/confirm/'

class BackerRegistrationCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_should_validation_backer_form_sing_up_without_data(self):
        response = self.client.post(REGISTER_URI, self.get_empty_form())

        self.assertEqual(response.status_code, 200)
        for i in self.get_form_fields():
            errors = response.context['form'][i].errors
            self.assertTrue((len(errors) == 1 and len(errors[0]) > 0), "Should return an error for %s field" % i)

    def test_should_validation_backer_form_sing_up_with_data(self):
        data = {'username': 'joedoe',
                'email': 'joe@example.com',
                'password1': 'secret',
                'first_name': 'Joe',
                'last_name': 'Doe',
                'year_dob': '1900', 'month_dob': '01', 'day_dob': '01',
                'gender': '1'
        }

        response = self.client.post(REGISTER_URI, data)

        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
        self.user = User.objects.all()
        self.assertTrue(len(User.objects.all()))
        self.user = User.objects.get(username='joedoe')
        self.assertNotEqual(self.user.password, "secret")

    def test_should_validation_form_sign_in_without_data(self):
        data = {'username': '', 'password': ''}
        response = self.client.post(LOGIN_URI, data)

        self.assertEqual(response.status_code, 200)
        for i in data:
            errors = response.context['form'][i].errors
            self.assertTrue((len(errors) == 1 and len(errors[0]) > 0), "Should return an error for %s field" % i)

    def test_should_validation_form_sign_in_bad_data(self):
        data = {'username': 'johnsmith', 'password': 'password'}
        response = self.client.post(LOGIN_URI, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_should_validation_form_sign_in_with_data(self):
        user = User.objects.get(username='joedoe')
        user.is_active = True
        user.save()
        response = self.client.post(LOGIN_URI, {'username': 'joedoe', 'password': 'secret'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')

    def test_should_send_notification_email_after_backer_successful_registration_and_for_reset_password(self):
        data = {'username': 'joedoe',
                'email': 'joe@example.com',
                'password1': 'secret',
                'first_name': 'Joe',
                'last_name': 'Doe',
                'year_dob': '1900', 'month_dob': '01', 'day_dob': '01',
                'gender': '1',
                'twitter_user': '',
                'facebook_user': '',
                'access_token': '',
                'secret_token': '',
                'expire_token': '',
                'third_party_id': ''
        }

        self.assertEquals(len(mail.outbox), 0)
        self.client.post(REGISTER_URI, data)
        self.assertEquals(len(mail.outbox), 1)

        user = User.objects.get(username='joedoe')
        user.is_active = True
        user.save()

        response = self.client.post(PASSWORD_RESET_URI, {'email': 'joe@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(len(mail.outbox), 2)

    def get_form_fields(self):
        return ['username', 'email', 'password1', 'first_name', 'last_name', 'year_dob', 'month_dob', 'day_dob',
                'gender']

    def get_empty_form(self):
        return dict.fromkeys(self.get_form_fields(), '')
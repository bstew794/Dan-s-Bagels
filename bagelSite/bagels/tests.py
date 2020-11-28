from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile

# Create your tests here.


class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('tester', 'tester497@gmail.com')
        user.set_password('Pass123!')
        user.first_name = 'Anon'
        user.last_name = 'Joe'
        user.profile.phone_number = '9999999999'
        user.profile.member_number = user.profile.phone_number + str(int(round(user.date_joined.timestamp() * 1000)))
        user.save()

    def test_users_can_login(self):
        tester = User.objects.get(username='tester')
        client = Client()
        logged_in = client.login(username=tester.username, password='Pass123!')

        self.assertTrue(logged_in, "Tester could not login")
        self.assertEqual(tester.first_name, 'Anon', "First name is incorrect.")
        self.assertEqual(tester.last_name, 'Joe', "Last name is incorrect.")
        self.assertEqual(tester.profile.phone_number, '9999999999', "Phone number is incorrect.")
        self.assertEqual(tester.profile.member_number, tester.profile.phone_number +
                         str(int(round(tester.date_joined.timestamp() * 1000))), "Member number is incorrect")

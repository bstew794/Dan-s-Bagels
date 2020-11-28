from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile, InventoryItem

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

        # test_increment_inventory
        test_item = InventoryItem.objects.create(price=2.99, stock=10, name="test item",
                                                 description="hello, this is a test", allegry_info="none")
        test_item.save()

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

    def test_increment_inventory(self):
        test_item = InventoryItem.objects.get(name="test item")
        self.assertEqual(test_item.stock, 10)
        test_item.stock += 1
        self.assertEqual(test_item.stock, 11)

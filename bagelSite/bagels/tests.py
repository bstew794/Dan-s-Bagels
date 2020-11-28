from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Order, InventoryItem


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'tester497@gmail.com')
        self.user.set_password('Pass123!')
        self.user.first_name = 'Anon'
        self.user.last_name = 'Joe'
        self.user.profile.phone_number = '9999999999'
        self.user.profile.member_number = self.user.profile.phone_number + \
                                          str(int(round(self.user.date_joined.timestamp() * 1000)))
        self.user.save()

        self.client = Client()

        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.create(
            codename='can_view_current_orders',
            name='Can View Current Orders',
            content_type=content_type,
        )
        permission1 = Permission.objects.create(
            codename='can_prepare_order',
            name='Can Prepare Order',
            content_type=content_type,
        )
        permission2 = Permission.objects.create(
            codename='can_fulfill_order',
            name='Can Fulfill Order',
            content_type=content_type,
        )

        content_type1 = ContentType.objects.get_for_model(InventoryItem)
        permission3 = Permission.objects.create(
            codename='can_manage',
            name='Can Manage',
            content_type=content_type1,
        )

        self.group = Group.objects.create(name='managers')
        self.group1 = Group.objects.create(name='cashiers')
        self.group2 = Group.objects.create(name='chefs')

        self.group.permissions.add(permission, permission3)
        self.group.save()

        self.group1.permissions.add(permission, permission2)
        self.group1.save()

        self.group2.permissions.add(permission, permission1)
        self.group2.save()

    def test_users_can_login(self):
        tester = User.objects.get(username='tester')

        self.assertTrue(self.client.login(username=tester.username, password='Pass123!'),
                        "Tester could not login.")
        self.assertEqual(tester.email, self.user.email, "Email is incorrect")
        self.assertEqual(tester.first_name, self.user.first_name, "First name is incorrect.")
        self.assertEqual(tester.last_name, self.user.last_name, "Last name is incorrect.")
        self.assertEqual(tester.profile.phone_number, self.user.profile.phone_number, "Phone number is incorrect.")
        self.assertEqual(tester.profile.member_number, self.user.profile.member_number, "Member number is incorrect.")

    def test_users_can_log_out(self):
        self.assertFalse(self.client.logout(), "Tester could not logout.")

    def test_customer_permissions(self):
        self.assertFalse(self.user.has_perm('bagels.can_view_current_orders'), "The user is not just a customer")
        self.assertFalse(self.user.has_perm('bagels.can_prepare_order'), "The user is not just a customer")
        self.assertFalse(self.user.has_perm('bagels.can_fulfill_order'), "The user is not just a customer")
        self.assertFalse(self.user.has_perm('bagels.can_manage'), "The user is not just a customer")

    def test_chef_permissions(self):
        self.user.groups.add(Group.objects.get(name='chefs'))
        self.user.save()

        self.assertTrue(self.user.has_perm('bagels.can_view_current_orders'), "The user is not a chef")
        self.assertTrue(self.user.has_perm('bagels.can_prepare_order'), "The user is not a chef")
        self.assertFalse(self.user.has_perm('bagels.can_fulfill_order'), "The user is not a chef")
        self.assertFalse(self.user.has_perm('bagels.can_manage'), "The user is not a chef")

        self.user.groups.remove(Group.objects.get(name='chefs'))
        self.user.save()

    def test_cashier_permissions(self):
        self.user.groups.add(Group.objects.get(name='cashiers'))
        self.user.save()

        self.assertTrue(self.user.has_perm('bagels.can_view_current_orders'), "The user is not a cashier")
        self.assertFalse(self.user.has_perm('bagels.can_prepare_order'), "The user is not a cashier")
        self.assertTrue(self.user.has_perm('bagels.can_fulfill_order'), "The user is not a cashier")
        self.assertFalse(self.user.has_perm('bagels.can_manage'), "The user is not a cashier")

        self.user.groups.remove(Group.objects.get(name='cashiers'))
        self.user.save()

    def test_manager_permissions(self):
        self.user.groups.add(Group.objects.get(name='managers'))
        self.user.save()

        self.assertTrue(self.user.has_perm('bagels.can_view_current_orders'), "The user is not a manager")
        self.assertFalse(self.user.has_perm('bagels.can_prepare_order'), "The user is not a manager")
        self.assertFalse(self.user.has_perm('bagels.can_fulfill_order'), "The user is not a manager")
        self.assertTrue(self.user.has_perm('bagels.can_manage'), "The user is not a manager")

        self.user.groups.remove(Group.objects.get(name='managers'))
        self.user.save()

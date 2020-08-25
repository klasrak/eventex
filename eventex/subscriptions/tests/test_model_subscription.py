from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def test_create(self):
        obj = Subscription(
            name="Danilo Augusto", cpf="12345678901", email="daniloaugusto@mailinator.com", phone="18-91111-2222"
        )
        obj.save()

        self.assertTrue(Subscription.objects.exists())

from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Danilo Augusto", cpf="12345678901", email="danilo@testmail.com", phone="18-91111-2222")
        self.response = self.client.post("/inscricao/", data)

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = "Confirmação de Inscrição"
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = "contato@eventex.com.br"
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ["contato@eventex.com.br", "danilo@testmail.com"]
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn("Danilo Augusto", email.body)
        self.assertIn("12345678901", email.body)
        self.assertIn("danilo@testmail.com", email.body)
        self.assertIn("18-91111-2222", email.body)

from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Danilo Augusto", cpf="12345678901", email="danilo@testmail.com", phone="18-91111-2222")
        self.client.post("/inscricao/", data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = "Confirmação de Inscrição"
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = "contato@eventex.com.br"
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ["contato@eventex.com.br", "danilo@testmail.com"]
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ["Danilo Augusto", "12345678901", "danilo@testmail.com", "18-91111-2222"]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

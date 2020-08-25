from datetime import date

from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscriptions_form.html"""
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ("<form", 1),
            ("<input", 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context["form"]
        self.assertSequenceEqual(["name", "cpf", "email", "phone"], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name="Danilo Augusto", cpf="12345678901", email="danilo@testmail.com", phone="18-91111-2222")
        self.response = self.client.post("/inscricao/", data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

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


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post("/inscricao/", {})

    def test_post(self):
        """Ivalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_has_form(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context["form"]
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name="Danilo Augusto", cpf="12345678901", email="danilo@testmail.com", phone="18-91111-2222")
        response = self.client.post("/inscricao/", data, follow=True)
        self.assertContains(response, "Inscrição realizada com sucesso!")

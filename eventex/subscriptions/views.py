from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == "POST":
        return create(request)
    else:
        return new(request)


def create(request):

    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, "subscriptions/subscription_form.html", {"form": form})

    form.full_clean()

    # Send email
    _send_mail(
        "Confirmação de Inscrição",
        settings.DEFAULT_FROM_EMAIL,
        form.cleaned_data["email"],
        "subscriptions/subscription_email.txt",
        form.cleaned_data,
    )

    # Create
    Subscription.objects.create(**form.cleaned_data)

    # Success feedback
    messages.success(request, "Inscrição realizada com sucesso!")

    return HttpResponseRedirect("/inscricao/1/")


def new(request):
    return render(request, "subscriptions/subscription_form.html", {"form": SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

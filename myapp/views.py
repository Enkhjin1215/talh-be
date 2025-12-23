from rest_framework import viewsets
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from .models import Lottery
from .serializers import LotterySerializer


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer

    def perform_create(self, serializer):
        lottery = serializer.save()

        # Email байхгүй бол илгээхгүй
        if lottery.email:
            subject = "Таны сугалааны сертификат"
            
            message = render_to_string("emails/lottery_certificate.html", {
                "name": lottery.buten_ner,
                "phone": lottery.utas,
                "created_at": lottery.created_at,
            })

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[lottery.email],
            )
            email.content_subtype = "html"
            email.send()

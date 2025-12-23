from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Lottery
from .serializers import LotterySerializer


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        print("DEBUG: Incoming data:", request.data)
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 1. Save to Database first
        lottery = serializer.save()
        print(f"Record created with ID: {lottery.id}")

        # 2. Attempt Email (wrapped in try/except)
        if lottery.email:
            try:
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
                
                # Note: This is still synchronous. 
                # If it's slow, your Flutter app might timeout.
                email.send(fail_silently=False) 
                print("Email sent successfully")
            except Exception as e:
                print(f"EMAIL ERROR: {str(e)}")
                # We don't return 400 because the record WAS created successfully.
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
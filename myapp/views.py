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
        print("Incoming request data:", request.data)  # Debug: see what client sends
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            print("Serializer is valid")
            lottery = serializer.save()

            # Email only if provided
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
                print("Email sent successfully")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # << Important
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def dispatch(self, request, *args, **kwargs):
        # 1. Print the Content-Type header specifically
        print(f"DEBUG: Content-Type Header: {request.META.get('CONTENT_TYPE')}")
        
        # 2. Print the Raw Body length to see if data is actually arriving
        print(f"DEBUG: Request Method: {request.method}")
        
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # This will only print if the Parser succeeds
        print("DEBUG: Parser success! Data:", request.data)
        return super().create(request, *args, **kwargs)

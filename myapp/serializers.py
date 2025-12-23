# serializers.py
from rest_framework import serializers
from .models import Lottery

class LotterySerializer(serializers.ModelSerializer):

    def validate(self, data):
        print(f"DEBUG: Serializer received data: {data}")
        return data

    def create(self, validated_data):
        print(f"DEBUG: Serializer creating object with: {validated_data}")
        return super().create(validated_data)    
    class Meta:
        model = Lottery
        fields = '__all__'

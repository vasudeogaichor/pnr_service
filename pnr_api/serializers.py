from rest_framework import serializers
from .models import PNRStatusModel
class PNRStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PNRStatusModel
        fields = ["pnr_number", "pnr_status"]
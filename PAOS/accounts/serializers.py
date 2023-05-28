from rest_framework import serializers
from .models import PAOSUser

class PAOSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAOSUser 
        fields = ["username", "first_name", "last_name", "email", "last_login", "is_active", "id"]

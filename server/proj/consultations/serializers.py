from rest_framework import serializers
from .models import UserProfile, Consultation


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    # id = serializers.IntegerField(source='pk')
    class Meta:
        model = UserProfile
        fields = '__all__'  # __all__'


class UserProfileApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = UserProfile
        fields = ('peerid', 'username')


class ConsultationSerializer(serializers.ModelSerializer):
    insigator = UserProfileApplicationSerializer(read_only=True)
    class Meta:
        model = Consultation
        fields = '__all__'


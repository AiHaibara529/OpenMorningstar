from rest_framework.serializers import ModelSerializer
from forum.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['id', 'name', 'description', 'created_at']

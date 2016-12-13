from .models import Gig
from rest_framework import serializers

class GigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gig
        fields = '__all__'
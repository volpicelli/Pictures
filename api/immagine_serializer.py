from rest_framework import serializers

from home.models import Immagine


class ImmagineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Immagine

        fields = '__all__'
from rest_framework import serializers

from polls.models import Recipe


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('title', 'description')

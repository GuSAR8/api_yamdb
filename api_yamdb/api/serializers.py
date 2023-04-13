from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(read_only=True,
                                         slug_field='slug',)
    category = serializers.SlugRelatedField(read_only=True,
                                            slug_field='slug',)
    
    class Meta:
        model = Title
        fields = '__all__'

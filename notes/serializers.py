from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Note, Category

User = get_user_model()

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Note Serializer (Fix: Only include necessary fields)
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    category = CategorySerializer(read_only=True, required=False)   # Nested category details

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'category', 'is_archived']

# User Serializer (Fix: `model = CustomUser`, fix password issue)


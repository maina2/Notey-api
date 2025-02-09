from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Note, Category
from .serializers import NoteSerializer, CategorySerializer

class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed, created, updated, and deleted.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        """
        Save the note with the currently authenticated user.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Return notes that belong to the currently authenticated user.
        """
        return Note.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def archive(self, request, pk=None):
        """
        Custom action to archive a note.
        """
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.is_archived = True
        note.save()
        return Response({'status': 'Note archived'})

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

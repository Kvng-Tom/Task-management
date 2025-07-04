from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Board, Tasks
from .serializers import BoardSerializer, TaskSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(creator=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BoardDeleteView(generics.DestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(creator=user)
    
    
    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        board.delete()
        return Response({"message": "Board deleted successfully!"}, status=status.HTTP_200_OK)

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return Tasks.objects.filter(board__id=board_id, board__creator=self.request.user)

    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_id')
        board = Board.objects.get(id=board_id, creator=self.request.user)
        serializer.save(board=board)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return Tasks.objects.filter(board__id=board_id, board__creator=self.request.user)
    
    
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response({"message": "Task deleted successfully!"}, status=status.HTTP_200_OK)
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer
from .models import User
from rest_framework import status
from .permissions import CustomAuthenticationPermission
from django.db.models import Q


class ProtectedView(APIView):
    permission_classes = [CustomAuthenticationPermission]

    def get(self, request):
        content = {'message': 'HELLO! YOU have a good TOKEN'}
        return Response(content)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [CustomAuthenticationPermission]

    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, User):
            return User.objects.none()

        return User.objects.filter(Q(id=user.id) | Q(friends=user)).distinct()

class AddFriendView(APIView):
    permission_classes = [CustomAuthenticationPermission]

    def post(self, request, pk):
        try:
            friend = User.objects.get(pk=pk)
            print(friend, "FRIEND")
            user = request.user
            print(type(user), user,"___________________________________")
            user.add_friend(friend)
            return Response({'status': 'friend added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveFriendView(generics.UpdateAPIView):
    permission_classes = [CustomAuthenticationPermission]
    serializer_class = UserSerializer

    def post(self, request, pk):
        user = request.user
        try:
            friend = User.objects.get(pk=pk)
            user.remove_friend(friend)
            return Response({'status': 'friend removed'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime, timezone

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer, ContactSerializer

from .models import PasswordReset, Contact


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({'password': 'Invalid username or password.'})

        return Response(serializer.validated_data, status=200)


class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        if not user:
            return Response({'error': 'User not found'}, status=404)

        password_reset = PasswordReset.objects.create(user=user)
        token = password_reset.token
        send_password_reset_email(user, password_reset, token)

        return Response({'message': 'Password reset email sent successfully'}, status=200)


def send_password_reset_email(user, password_reset, token):
    subject = 'Password Reset'
    message = f'Hello {user.username},\n\nPlease click the following link to reset your password: http://localhost:8000/api/reset-password/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


class ResetPasswordView(APIView):
    def get(self, request, token):
        try:
            password_reset = PasswordReset.objects.get(token=token)
            now = datetime.now(timezone.utc)
            if password_reset.expires_at < now:
                return Response({'error': 'Token has expired'}, status=400)
            return Response({'token': token})
        except PasswordReset.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=404)

    def post(self, request, token):
        password_reset = PasswordReset.objects.get(token=token)
        new_password = request.data.get('new_password')
        user = password_reset.user
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=200)


class ContactListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except KeyError:
            return Response({'error': 'Username is required'}, status=400)


class ContactDetailView(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        contact = self.get_object(pk)
        contact.delete()
        return Response(status=204)

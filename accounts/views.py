from django.contrib.auth import login
from django.views import View
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from accounts.forms import LoginForm
from accounts.api.serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class LoginAndRegister(View):
    def get(self, request):
        return render(request, "login.html", {
            "login_form": LoginForm()
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, "login.html", {
                "response": ["OK"]
            })
        else:
            return render(request, "login.html", {
                "login_form": form,
                "response": form.errors
            })
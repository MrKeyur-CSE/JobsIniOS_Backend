from rest_framework import generics, status
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
# Create your views here.


class RegistrationView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("error -- ", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            data = {
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'address': user.address,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        data = request.data
        try:
            user = CustomUser.objects.get(id=pk)
            user.full_name = data['full_name']
            user.phone_number = data['phone_number']
            user.address = data['address']
            user.save()

            data = {
                'id': user.id,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'address': user.address,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

import re
from rest_framework import status, views
from rest_framework.response import Response
from authApp.serializers.userSerializer import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserCreateView(views.APIView):
  def post(self, request, *args, **kwargs):
    # Instanciar UserSerializer con la data enviada en la petición
    serializer = UserSerializer(data=request.data)
    # Validamos que la data venga en el formato esperado y retorna error en caso que no
    serializer.is_valid(raise_exception=True)
    # Luego de que la data es válida, llama el método "Create" para crear el usuario.
    serializer.save()
    # Imprime la información validada en el selializador
    print(serializer.validated_data)
    
    # Generar el objeto para hacer Login
    token_data = {
      'username': request.data['username'],
      'password': request.data['password'],
    }
    # Instanciar TokenObtainPairSerializer con token_data
    token_serializer = TokenObtainPairSerializer(data=token_data)
    # Validamos que la data venga en el formato esperado y retorna error en caso que no
    token_serializer.is_valid(raise_exception=True)

    # Retornar la información validada en el selializador del token
    return Response(token_serializer.validated_data, status=status.HTTP_200_OK)
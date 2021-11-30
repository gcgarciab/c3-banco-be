from authProject import settings

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend

from authApp.models.user import User
from authApp.serializers.userSerializer import UserSerializer
from authApp.serializers.userUpdateSerializer import UserUpdateSerializer

class UserDetailView(views.APIView):
  users = User.objects.all()
  # serializer = UserSerializer(users, many=True)
 
  # def get(self, request):
  #   return Response(self.serializer.data, status=status.HTTP_200_OK)

  def get(self, request, *args, **kwargs):
    token = request.META.get('HTTP_AUTHORIZATION')[7:]
    tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    valid_data = tokenBackend.decode(token, verify=False)
    
    if (valid_data['user_id'] != kwargs['pk']):
      error = { 'message': 'Unathorized user!' }
      return Response(error, status=status.HTTP_401_UNAUTHORIZED)
    
    user = self.users.get(id=kwargs['pk'])
    user_serializer = UserSerializer(user)

    return Response(user_serializer.data, status=status.HTTP_200_OK)


  def put(self, request, *args, **kwargs):
    user = self.users.filter(id=kwargs['pk']).first() # Similar a self.users.get(id=kwargs['pk']) pero evita errores en caso de que el usuario no ea encontrado

    if (user):
      # Si le pasan como primer parámetro la instancia al serializador, ya pueden llamar el método update, si no, les pedirá que creen un método 
      user_serializer = UserUpdateSerializer(user, data=request.data)

      if (user_serializer.is_valid(raise_exception=True)):
        user_serializer.save()
       
        return Response({ 'message': 'Usuario actualizado' }, status=status.HTTP_200_OK)

      return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({ 'message': 'Usuario no encontrado' }, status=status.HTTP_404_NOT_FOUND) 


  def delete(self, request, *args, **kwargs):
    user = self.users.filter(id=kwargs['pk']).first()
    
    if (user):
      user.delete()

      return Response({ 'message': 'Usuario eliminado' }, status=status.HTTP_200_OK)

    return Response({ 'message': 'Usuario no encontrado' }, status=status.HTTP_404_NOT_FOUND) 

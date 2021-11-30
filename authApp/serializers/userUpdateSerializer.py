from rest_framework import serializers
from authApp.models.user import User

class UserUpdateSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=40)
  password = serializers.CharField(max_length=40)

  class Meta:
    model = User

  def validate_name(self, value):
    if (value == ''):
      raise serializers.ValidationError('Error, El nombre no puede ser vacío.')
    return value

  def validate_password(self, value):    
    if (len(value) < 6):
      raise serializers.ValidationError('Error, El mínimo tamaño para una contraseña son 6 caracteres.')
    return value

  # def create(self, validated_data): 
  #   return User.objects.create(**validated_data)

  def update(self, instance, validated_data):
    # print(validated_data)
    instance.name = validated_data.get('name', instance.name)
    instance.password = validated_data.get('password', instance.password)
    instance.save()
    return instance
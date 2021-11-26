from rest_framework import serializers
from authApp.models.account import Account

from authApp.models.user import User
from authApp.serializers.accountSerializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
  account = AccountSerializer()

  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'name', 'email', 'account']

  def create(self, validated_data):
    # Separamos la información de la cuenta en la variable account_data
    account_data = validated_data.pop('account')
    # Creamos un usuario con la información restante y se asocia a la variable userInstance
    userInstance = User.objects.create(**validated_data)
    # Creamos una cuenta con la data filtrada y se la asociamos al usuario creado
    Account.objects.create(user=userInstance, **account_data)

    return userInstance

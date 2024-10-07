from rest_framework import serializers
from .models import User, Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['value', 'hidden_value']

    def to_representation(self, instance):
        request = self.context.get('request')
        representation = {
            'value': instance.value if instance.value is not None else 0,
        }

        # Проверяем, является ли текущий пользователь владельцем аккаунта
        if request and request.user == instance.user:
            representation['hidden_value'] = instance.hidden_value if instance.hidden_value is not None else 0
        else:
            # Для всех остальных не показываем hidden_value
            representation['hidden_value'] = None

        return representation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'account']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Проверяем, является ли текущий пользователь самим пользователем
        if request and request.user == instance:
            if not representation.get('account'):
                representation['account'] = {'value': 0, 'hidden_value': 0}
        else:
            # Для друзей, если нет аккаунта, оставить 'hidden_value' как None
            if not representation.get('account'):
                representation['account'] = {'value': 0, 'hidden_value': None}

        return representation


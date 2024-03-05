"""
Serializers for the user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )

from django.utils.translation import gettext as _
#_ common notation fro django

from rest_framework import serializers
#serializer convert object from json and validates - to python object or model

class UserSerializer(serializers.ModelSerializer):
    """Serailaizer for the user object - model serializer - validates"""

    class Meta:
    #this is this the model we pass to serializer
        model = get_user_model()
        # fields that are provided in request passed from user that they change
        fields = ['email', 'password', 'name']
        #tells django framework about some special values
        #- here password has to be more than 5
        extra_kwargs = {'password': {'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        """overrides behaviours -
        Create and return a user with encryped password
        called after validation if that is successful """
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type' : 'password'},
        trim_whitespace=False,
    )
    #using the style means password will be hidden and removes spaces
    #we don't want to trim spaces in password so set to False

    def valideate(self, attrs):
        """Validate and authentiate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        #authenticate is built in to django
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
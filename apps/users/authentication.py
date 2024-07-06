from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from apps.users.models import BlackListedTokenAccess

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = {h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES}


class WithAccessToken:
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(api_settings.AUTH_HEADER_NAME)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[1]

    def get_acces_token(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        token = self.get_raw_token(header)
        return token


class IsTokenValid(WithAccessToken, BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True

        token = self.get_acces_token(request)
        try:
            is_blackListed = BlackListedTokenAccess.objects.get(
                user=user_id, token=token
            )
            if is_blackListed:
                is_allowed_user = False
        except BlackListedTokenAccess.DoesNotExist:
            is_allowed_user = True
        if not is_allowed_user:
            raise AuthenticationFailed("Token invalido.")
        return is_allowed_user


class SoloPuedeModificarseElMismo(BasePermission):
    def has_object_permission(self, request, view, obj):
        usuario = request.user
        respuesta = usuario.id == obj.id
        return respuesta

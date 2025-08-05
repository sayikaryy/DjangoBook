# auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
 def authenticate(self, request):
    header_auth = super().authenticate(request)
    if header_auth:
        print("Authenticated via header")
        return header_auth

    raw_token = request.COOKIES.get('access_token')
    print("Token from cookie:", raw_token)
    if not raw_token:
        print("No token found in cookies")
        return None

    validated_token = self.get_validated_token(raw_token)
    user_auth_tuple = self.get_user(validated_token), validated_token
    print("Authenticated user:", user_auth_tuple[0])
    return user_auth_tuple



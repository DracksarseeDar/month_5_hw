import requests
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.serializers import OAuthCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code"
            }
        )   
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": f"Invalid access token: {token_data}"})

        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        print(f"USER_INFO: {user_info}")

        email = user_info.get("email")
        given_name = user_info.get("given_name", "")
        family_name = user_info.get("family_name", "")

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.registration_source = 'google'
            user.set_unusable_password()

      
        user.first_name = given_name
        user.last_name = family_name
        user.is_active = True        
        user.last_login = timezone.now() 
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "source": user.registration_source,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },status=status.HTTP_200_OK)
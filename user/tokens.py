from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model
User = get_user_model()

def get_tokens_for_user(user:User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }   

def get_user_from_token(token):
    try:
        access_token = AccessToken(str(token))
        user_id = access_token["user_id"]  # Adjust the key based on your payload
        # Now you have the user_id, you can retrieve the user from the database
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        # Handle exceptions, e.g., token decoding errors or user not found
        print(f"Error decoding token: {e}")
        return None
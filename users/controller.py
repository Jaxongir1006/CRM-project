from .schemas import (
    RegistereSchema,
    LoginSchema,
    CustomUserSchema,
    ErrorSchema,
)
from .models import CustomUser
from ninja_extra import api_controller, http_post, http_get
from ninja_jwt.tokens import RefreshToken
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAdmin


@api_controller("/user", tags=["Register and Login"])
class UserController:
    @http_post(
        "/register/",
        response={201: dict, 400: ErrorSchema},
        permissions=[IsAdmin],
        auth=JWTAuth(),
    )
    def register(self, request, data: RegistereSchema):
        """
        Register a new user
        """
        if data.password != data.confirm_password:
            return 400, {"error": "Passwords do not match"}
        data = data.model_dump(exclude_unset=True)
        data.pop("confirm_password")
        try:
            user = CustomUser.objects.create_user(**data)
        except Exception as e:
            return 400, {"error": str(e)}
        token = RefreshToken.for_user(user)

        return 201, {
            "message": "New user created",
            "user": CustomUserSchema.from_orm(user),
        }

    @http_post("/login/", response={200: dict, 400: ErrorSchema})
    def login(self, data: LoginSchema):
        data = data.model_dump(exclude_unset=True)
        user = CustomUser.objects.login_user(**data)
        if not user:
            return 400, {"error": "Invalid credentials"}

        token = RefreshToken.for_user(user)

        response_data = {
            "user": CustomUserSchema.from_orm(user),
            "tokens": {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            },
        }

        return 200, response_data

    @http_get(
        "/me/", response=CustomUserSchema, permissions=[IsAuthenticated], auth=JWTAuth()
    )
    def get_me(self, request):
        user = request.user
        return user

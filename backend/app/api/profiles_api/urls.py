from django.urls import path

from api.profiles_api.views import CreateUserView, ProfileRetrieveUpdateDestroy, CustomAuthToken, DeactivateAccountView, ChangePasswordView


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('details/', ProfileRetrieveUpdateDestroy.as_view(), name='retrieve-update-delete-api-view'),
    path('login/', CustomAuthToken.as_view()),
    path('deactivate/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

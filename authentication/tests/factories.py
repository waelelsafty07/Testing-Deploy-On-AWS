from django.contrib.auth.hashers import make_password
import factory
from users.models import Users


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password("password"))
    is_active = True

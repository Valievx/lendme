from django.contrib.auth.models import BaseUserManager


text = ("Ваш пароль: {password}.\n\n"
        "Никому не передавайте свой пароль в целях безопасности!")


class CustomUserManager(BaseUserManager):
    """Менеджер модели пользователя, для регистрации с ИНН."""

    use_in_migrations = True

    def create_user(
        self,
        username,
        name,
        email,
        phone,
        password,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(
            username=username,
            name=name,
            email=email,
            phone=phone,
            password=password,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, password, organization_inn=None, **extra_fields
    ):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен быть is_superuser=True."
            )

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_phone_verified = True
        user.is_verified = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

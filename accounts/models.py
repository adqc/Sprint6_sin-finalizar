from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['first_name'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "Nombre debe ser mínimo 2 caracteres"

        if (postData['last_name'].isalpha()) == False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Apellido debe ser mínimo 2 caracteres"

        if len(postData['email']) == 0:
            errors['email'] = "Debe introducir un correo electronico"

        if len(postData['password']) < 8:
            errors['password'] = "Contraseña muy corta"

        return errors

class User(models.Model):
    is_admin=models.BooleanField(default=False)
    is_profesor=models.BooleanField(default=False)
    is_estudiante=models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

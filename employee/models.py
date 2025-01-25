from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class Employee(AbstractUser):
    class Meta:
        db_table = 'employees'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['first_name', 'last_name']
        
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_set',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence. Um usuário receberá todas as permissões concedidas a cada um de seus grupos.',
        verbose_name='Grupos',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_set',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='Permissões do usuário',
    )

    def __str__(self):
        return self.get_full_name()
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
import uuid
from .utils import generate_file_path
from .validators import *

# Create your models here.
class Gender(models.Model):
    class Meta:
        db_table = 'genders'
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name
    
class DriversLicenseCategory(models.Model):
    class Meta:
        db_table = 'drivers_license_categories'
        verbose_name = 'Categoria da CNH'
        verbose_name_plural = 'Categorias da CNH'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    class Meta:
        db_table = 'candidates'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        ordering = ['first_name', 'last_name']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    first_name = models.CharField(
        max_length=255,
        validators=[lambda value: validate_name(value, _('First name'))],
        verbose_name='Nome'
    )
    last_name = models.CharField(
        max_length=255,
        validators=[lambda value: validate_name(value, _('Last name'))],
        verbose_name='Sobrenome'
    )
    date_of_birth = models.DateField(
        validators=[validate_date_of_birth],
        verbose_name='Data de nascimento'
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.PROTECT,
        verbose_name='Gênero'
    )
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_cpf],
        verbose_name='CPF'
    )
    rg = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_rg],
        verbose_name='RG'
    )
    has_disability = models.BooleanField(
        default=False,
        verbose_name='Possui deficiência?'
    )
    disability_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descrição da deficiência'
    )
    has_drivers_license = models.BooleanField(
        default=False,
        verbose_name='Possui CNH?'
    )
    drivers_license_category = models.ForeignKey(
        DriversLicenseCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Categoria da CNH'
    )
    is_first_job = models.BooleanField(
        default=False,
        verbose_name='É o primeiro emprego?'
    )
    is_currently_employed = models.BooleanField(
        default=False,
        verbose_name='Está trabalhando atualmente?'
    )
    photo = models.ImageField(
        upload_to=generate_file_path,
        null=True,
        blank=True,
        verbose_name='Foto'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)

        return full_name.strip()
    
    def clean(self):
        errors = {}

        # Aqui sao feitas as validacoes de campos que dependem de outros campos

        if errors:
            print(errors)
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Candidate.objects.get(pk=self.pk)

                if old_instance.photo != self.photo:
                    if old_instance.photo and os.path.isfile(old_instance.photo.path):
                        os.remove(old_instance.photo.path)
            except Candidate.DoesNotExist:
                old_instance = None

        self.full_clean()
        super(Candidate, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.exists(self.photo.path):
                try:
                    os.remove(self.photo.path)
                except Exception as e:
                    print(f'Error deleting photo: {e}')

        super(Candidate, self).delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()
    
class Contact(models.Model):
    class Meta:
        db_table = 'contacts'
        verbose_name = 'Informação de Contato'
        verbose_name_plural = 'Informações de Contato'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='Número de telefone'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='E-mail'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='Candidato'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.candidate.get_full_name()
    
class State(models.Model):
    class Meta:
        db_table = 'states'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome'
    )
    abbreviation = models.CharField(
        max_length=2,
        unique=True,
        verbose_name='Abreviação'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name
    
class City(models.Model):
    class Meta:
        db_table = 'cities'
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Nome'
    )
    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.name
    
class Address(models.Model):
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    street = models.CharField(
        max_length=255,
        verbose_name='Rua'
    )
    number = models.CharField(
        max_length=10,
        verbose_name='Número'
    )
    complement = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Complemento'
    )
    neighborhood = models.CharField(
        max_length=255,
        verbose_name='Bairro'
    )
    zip_code = models.CharField(
        max_length=8,
        verbose_name='CEP'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name='Cidade'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Candidato'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.candidate.get_full_name()
    
class SocialMedia(models.Model):
    class Meta:
        db_table = 'social_media'
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Nome'
    )
    url = models.URLField(
        verbose_name='URL'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='social_media',
        verbose_name='Candidato'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        return self.candidate.get_full_name()

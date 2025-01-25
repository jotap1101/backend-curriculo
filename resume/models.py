from django.db import models
from candidate.models import Candidate
from employee.models import Employee
import uuid

# Create your models here.
class AreaOfInterest(models.Model):
    class Meta:
        db_table = 'areas_of_interest'
        verbose_name = 'Área de Interesse'
        verbose_name_plural = 'Áreas de Interesse'
        ordering = ['name']

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
    
class SubareaOfInterest(models.Model):
    class Meta:
        db_table = 'subareas_of_interest'
        verbose_name = 'Subárea de Interesse'
        verbose_name_plural = 'Subáreas de Interesse'
        ordering = ['name']

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
    area_of_interest = models.ForeignKey(
        AreaOfInterest,
        on_delete=models.CASCADE,
        related_name='subareas_of_interest',
        verbose_name='Área de Interesse'
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
    
class Skill(models.Model):
    class Meta:
        db_table = 'skills'
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'
        ordering = ['name']

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

class StatusResume(models.Model):
    class Meta:
        db_table = 'status_resumes'
        verbose_name = 'Status do Currículo'
        verbose_name_plural = 'Status dos Currículos'
        ordering = ['name']

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

class Resume(models.Model):
    class Meta:
        db_table = 'resumes'
        verbose_name = 'Currículo'
        verbose_name_plural = 'Currículos'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='resumes',
        null=True,
        blank=True,
        verbose_name='Funcionário'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Candidato'
    )
    summary = models.TextField(
        null=True,
        blank=True,
        verbose_name='Resumo'
    )
    subareas_of_interest = models.ManyToManyField(
        SubareaOfInterest,
        verbose_name='Subáreas de Interesse'
    )
    skills = models.ManyToManyField(
        Skill,
        verbose_name='Habilidades'
    )
    status = models.ForeignKey(
        StatusResume,
        on_delete=models.PROTECT,
        related_name='resumes',
        verbose_name='Status'
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
    
class Institution(models.Model):
    class Meta:
        db_table = 'institutions'
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'
        ordering = ['name']

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

    def __str__(self):
        return self.name
    
class Course(models.Model):
    class Meta:
        db_table = 'courses'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']

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
    
    def __str__(self):
        return self.name
    
class Education(models.Model):
    class Meta:
        db_table = 'educations'
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações Acadêmicas'
        ordering = ['-end_date']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name='educations',
        verbose_name='Instituição'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='educations',
        verbose_name='Curso'
    )
    start_date = models.DateField(
        verbose_name='Data de Início'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='Está cursando atualmente?'
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name='Currículo'
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
        return self.resume.candidate.get_full_name()
    
class Company(models.Model):
    class Meta:
        db_table = 'companies'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

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

    def __str__(self):
        return self.name
    
class JobTitle(models.Model):
    class Meta:
        db_table = 'job_titles'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['name']

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

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    class Meta:
        db_table = 'experiences'
        verbose_name = 'Experiência Profissional'
        verbose_name_plural = 'Experiências Profissionais'
        ordering = ['-end_date']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='experiences',
        verbose_name='Empresa'
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        related_name='experiences',
        verbose_name='Cargo'
    )
    start_date = models.DateField(
        verbose_name='Data de Início'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='Está trabalhando atualmente?'
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='experiences',
        verbose_name='Currículo'
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
        return self.resume.candidate.get_full_name()
    
class Language(models.Model):
    class Meta:
        db_table = 'languages'
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'
        ordering = ['name']

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

    def __str__(self):
        return self.name
    
class LanguageLevel(models.Model):
    class Meta:
        db_table = 'language_levels'
        verbose_name = 'Nível de Idioma'
        verbose_name_plural = 'Níveis de Idioma'
        ordering = ['name']

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

    def __str__(self):
        return self.name
    
class ResumeLanguage(models.Model):
    class Meta:
        db_table = 'resumes_languages'
        verbose_name = 'Idioma do Currículo'
        verbose_name_plural = 'Idiomas dos Currículos'
        ordering = ['language']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name='resumes_languages',
        verbose_name='Idioma'
    )
    level = models.ForeignKey(
        LanguageLevel,
        on_delete=models.PROTECT,
        related_name='resumes_languages_levels',
        verbose_name='Nível'
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name='Currículo'
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
        return self.resume.candidate.get_full_name()
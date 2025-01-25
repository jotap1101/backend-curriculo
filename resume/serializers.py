from django.db import transaction
from rest_framework import serializers
from .models import *

class SubareaOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubareaOfInterest
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {
                'read_only': True,
                'required': False
            }
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {
                'read_only': True,
                'required': False
            }
        }

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'course', 'start_date', 'end_date', 'is_current']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False
            }
        }

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company', 'job_title', 'start_date', 'end_date', 'is_current']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False
            }
        }

class ResumeLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeLanguage
        fields = ['id', 'language', 'level']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False
            }
        }

class ResumeSerializer(serializers.ModelSerializer):
    subareas_of_interest = serializers.PrimaryKeyRelatedField(many=True, queryset=SubareaOfInterest.objects.all())
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    educations = EducationSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    languages = ResumeLanguageSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = ['id', 'employee', 'candidate', 'summary', 'subareas_of_interest', 'skills', 'educations', 'experiences', 'languages', 'status']
        extra_kwargs = {
            'id': {
                'read_only': True,
                'required': False
            },
            'employee': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        subareas_of_interest_data = validated_data.pop('subareas_of_interest', None)
        skills_data = validated_data.pop('skills', None)
        educations_data = validated_data.pop('educations', None)
        experiences_data = validated_data.pop('experiences', None)
        languages_data = validated_data.pop('languages', None)

        with transaction.atomic():
            resume = Resume.objects.create(**validated_data)

            if subareas_of_interest_data is not None:
                resume.subareas_of_interest.set(subareas_of_interest_data)

            if skills_data is not None:
                resume.skills.set(skills_data)

            for education_data in educations_data:
                Education.objects.create(resume=resume, **education_data)

            for experience_data in experiences_data:
                Experience.objects.create(resume=resume, **experience_data)

            for language_data in languages_data:
                ResumeLanguage.objects.create(resume=resume, **language_data)

        return resume

    def update(self, instance, validated_data):
        related_fields = ['subareas_of_interest', 'skills', 'educations', 'experiences', 'languages']

        with transaction.atomic():
            related_data = {field: validated_data.pop(field, None) for field in related_fields}

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if related_data['educations'] is not None:
                existing_ids = []

                for education_data in related_data['educations']:
                    education_id = education_data.pop('id', None)

                    if education_id:
                        education = Education.objects.get(id=education_id, resume=instance)

                        for field in ['institution', 'course', 'start_date']:
                            if field not in education_data:
                                education_data[field] = getattr(education, field)
                        
                        for key, value in education_data.items():
                            setattr(education, key, value)

                        education.save()
                        existing_ids.append(education_id)
                    else:
                        education = Education.objects.create(resume=instance, **education_data)

                        existing_ids.append(education.id)

                instance.educations.exclude(id__in=existing_ids).delete()

            if related_data['experiences'] is not None:
                existing_ids = []

                for experience_data in related_data['experiences']:
                    experience_id = experience_data.pop('id', None)

                    if experience_id:
                        experience = Experience.objects.get(id=experience_id, resume=instance)

                        for field in ['company', 'job_title', 'start_date']:
                            if field not in experience_data:
                                experience_data[field] = getattr(experience, field)

                        for key, value in experience_data.items():
                            setattr(experience, key, value)

                        experience.save()
                        existing_ids.append(experience_id)
                    else:
                        experience = Experience.objects.create(resume=instance, **experience_data)

                        existing_ids.append(experience.id)

                instance.experiences.exclude(id__in=existing_ids).delete()

            if related_data['languages'] is not None:
                existing_ids = []
                
                for language_data in related_data['languages']:
                    language_id = language_data.pop('id', None)

                    if language_id:
                        language = ResumeLanguage.objects.get(id=language_id, resume=instance)

                        for field in ['language', 'level']:
                            if field not in language_data:
                                language_data[field] = getattr(language, field)

                        for key, value in language_data.items():
                            setattr(language, key, value)

                        language.save()
                        existing_ids.append(language_id)
                    else:
                        language = ResumeLanguage.objects.create(resume=instance, **language_data)
                        
                        existing_ids.append(language.id)

                instance.languages.exclude(id__in=existing_ids).delete()

        return instance
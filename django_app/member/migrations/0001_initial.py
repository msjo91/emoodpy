# Generated by Django 2.0.6 on 2018-06-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('nickname', models.CharField(blank=True, max_length=30, null=True, verbose_name='nickname')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'N/A')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date_of_birth')),
                ('institution', models.CharField(blank=True, max_length=30, null=True, verbose_name='institution')),
                ('fitbit', models.CharField(blank=True, max_length=100, null=True, verbose_name='fitbit')),
                ('user_type', models.CharField(choices=[('P', 'Patient'), ('R', 'Researcher'), ('D', 'Developer')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
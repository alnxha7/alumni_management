# Generated by Django 4.2.3 on 2024-10-28 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumini', '0002_alter_events_description_alter_events_venue'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlumniJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=100)),
                ('date_joined', models.DateField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='alumni_job_images/')),
                ('approved', models.BooleanField(default=False)),
                ('alumni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='alumini.alumni')),
            ],
        ),
    ]

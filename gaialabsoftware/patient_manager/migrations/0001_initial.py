# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-01 02:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import patient_manager.models
import patient_manager.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_tools_stats', '0002_auto_20170805_0259'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientePostPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rif', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Patron')),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, validators=[patient_manager.validators.validate_positive_num])),
                ('nacionalidad', models.CharField(choices=[('V', 'V'), ('E', 'E'), ('G', 'G'), ('J', 'J')], max_length=10)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Clinicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rif', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, validators=[patient_manager.validators.validate_positive_num])),
            ],
            options={
                'verbose_name': 'Clinica(cliente)',
                'verbose_name_plural': 'Clinicas(cliente)',
            },
        ),
        migrations.CreateModel(
            name='Codigos',
            fields=[
                ('titulo', models.BooleanField(default=False)),
                ('numero', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('descripcion', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
            ],
            options={
                'verbose_name': 'Codigo',
                'verbose_name_plural': 'Codigos',
            },
        ),
        migrations.CreateModel(
            name='Detalles_Facturas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudio_realizado', models.CharField(max_length=250)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='Estudios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('last_modified_ts', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('impreso', models.BooleanField(default=False)),
                ('clinica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Clinicas')),
            ],
            options={
                'verbose_name': 'Estudios',
                'verbose_name_plural': 'Estudios',
            },
        ),
        migrations.CreateModel(
            name='Facturas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(choices=[('V', 'V'), ('E', 'E'), ('G', 'G'), ('J', 'J')], max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('last_modified_ts', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=50)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('rif', models.CharField(max_length=250)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, validators=[patient_manager.validators.validate_positive_num])),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rif', models.CharField(blank=True, max_length=50)),
                ('razon_social', models.CharField(blank=True, max_length=50)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('pais', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('ciudad', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=250)),
                ('codigo_postal', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Laboratorio',
                'verbose_name_plural': 'Laboratorios',
            },
        ),
        migrations.CreateModel(
            name='Medicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('numero_licencia', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('celular', models.CharField(blank=True, max_length=15, null=True, validators=[patient_manager.validators.validate_positive_num])),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Medico',
                'verbose_name_plural': 'Medicos',
            },
        ),
        migrations.CreateModel(
            name='Nomina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=50)),
                ('nombres', models.CharField(max_length=50)),
                ('acceso_a_sistema', models.BooleanField(default=False)),
                ('laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Laboratorio')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nomina',
                'verbose_name_plural': 'Nomina',
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=50, unique=True, validators=[patient_manager.validators.validate_positive_num])),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('sexo', models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=10)),
                ('nacionalidad', models.CharField(choices=[('V', 'V'), ('E', 'E')], max_length=10)),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.CharField(blank=True, max_length=15, null=True, validators=[patient_manager.validators.validate_positive_num])),
                ('observaciones', models.TextField(blank=True, max_length=500, null=True)),
                ('detalle', models.CharField(blank=True, max_length=50, null=True)),
                ('post_pago', models.BooleanField(default=False, verbose_name='Post Pago')),
                ('patron', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_manager.ClientePostPago')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Resultados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('last_modified_ts', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('adjunto', models.FileField(blank=True, null=True, upload_to=patient_manager.models.resultado_adjunto)),
                ('impreso', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Resultado',
                'verbose_name_plural': 'Resultados',
            },
        ),
        migrations.CreateModel(
            name='Resultados_Codigos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('codigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Codigos')),
                ('resultado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Resultados')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Tipos_Estudios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=50)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('last_modified_ts', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
            ],
            options={
                'verbose_name': 'Sub. Tipo de Estudio',
                'verbose_name_plural': 'Sub. Tipos de Estudios',
            },
        ),
        migrations.CreateModel(
            name='Tipos_Estudios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('citologia', 'citologia'), ('biopsia', 'biopsia')], max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tipo de Estudio',
                'verbose_name_plural': 'Tipos de Estudios',
            },
        ),
        migrations.CreateModel(
            name='MyDashboardStats',
            fields=[
            ],
            options={
                'verbose_name': 'Estadistica',
                'proxy': True,
                'verbose_name_plural': 'Estadisticas',
            },
            bases=('admin_tools_stats.dashboardstats',),
        ),
        migrations.CreateModel(
            name='MyDashboardStatsCriteria',
            fields=[
            ],
            options={
                'verbose_name': 'Criterios  de estadisticas',
                'proxy': True,
            },
            bases=('admin_tools_stats.dashboardstatscriteria',),
        ),
        migrations.AddField(
            model_name='sub_tipos_estudios',
            name='tipo_estudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_tipos_estudios', to='patient_manager.Tipos_Estudios'),
        ),
        migrations.AddField(
            model_name='resultados',
            name='codigos',
            field=models.ManyToManyField(through='patient_manager.Resultados_Codigos', to='patient_manager.Codigos'),
        ),
        migrations.AddField(
            model_name='resultados',
            name='estudio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Estudios'),
        ),
        migrations.AddField(
            model_name='pacientes',
            name='sub_tipos_estudios',
            field=models.ManyToManyField(help_text='Estudios relacionados', related_name='pacientes', through='patient_manager.Estudios', to='patient_manager.Sub_Tipos_Estudios'),
        ),
        migrations.AddField(
            model_name='pacientes',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estudios',
            name='estudio_realizado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Sub_Tipos_Estudios'),
        ),
        migrations.AddField(
            model_name='estudios',
            name='factura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='patient_manager.Facturas'),
        ),
        migrations.AddField(
            model_name='estudios',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Medicos'),
        ),
        migrations.AddField(
            model_name='estudios',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Pacientes'),
        ),
        migrations.AddField(
            model_name='estudios',
            name='patron',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_manager.ClientePostPago'),
        ),
        migrations.AddField(
            model_name='estudios',
            name='registrado_por',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Nomina'),
        ),
        migrations.AddField(
            model_name='detalles_facturas',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_manager.Facturas'),
        ),
        migrations.AddField(
            model_name='clinicas',
            name='medicos',
            field=models.ManyToManyField(help_text='Medicos relacionados', related_name='clinicas', to='patient_manager.Medicos'),
        ),
        migrations.AddField(
            model_name='clinicas',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

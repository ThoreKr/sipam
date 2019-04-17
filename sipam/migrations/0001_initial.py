# Generated by Django 2.2 on 2019-04-09 20:50

from django.db import migrations, models
import django.db.models.deletion
import netfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('prefix', netfields.fields.CidrAddressField(max_length=43)),
                ('subdomain', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='sipam.Prefix')),
                ('pool', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prefixes', to='sipam.Pool')),
            ],
            options={
                'ordering': ('prefix',),
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('ip', netfields.fields.InetAddressField(max_length=39)),
                ('fqdn', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ips', to='sipam.Prefix')),
            ],
            options={
                'ordering': ('ip',),
            },
        ),
    ]

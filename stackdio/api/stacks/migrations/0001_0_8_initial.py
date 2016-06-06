# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.files.storage
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields
from django.conf import settings
from django.db import migrations, models

import stackdio.api.stacks.models
import stackdio.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blueprints', '0001_0_8_initial'),
        ('cloud', '0001_0_8_initial'),
    ]

    replaces = [
        (b'stacks', '0001_initial'),
        (b'stacks', '0002_v0_7_migrations'),
        (b'stacks', '0003_v0_7b_migrations'),
        (b'stacks', '0004_v0_7c_migrations'),
        (b'stacks', '0005_v0_7d_migrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('status', model_utils.fields.StatusField(default=b'pending', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'pending', b'pending'), (b'ok', b'ok'), (b'deleting', b'deleting')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('status_detail', models.TextField(blank=True)),
                ('subnet_id', models.CharField(default=b'', max_length=32, verbose_name=b'Subnet ID', blank=True)),
                ('hostname', models.CharField(max_length=64, verbose_name=b'Hostname')),
                ('index', models.IntegerField(verbose_name=b'Index')),
                ('state', models.CharField(default=b'unknown', max_length=32, verbose_name=b'State')),
                ('state_reason', models.CharField(default=b'', max_length=255, verbose_name=b'State Reason', blank=True)),
                ('provider_dns', models.CharField(max_length=64, verbose_name=b'Provider DNS', blank=True)),
                ('provider_private_dns', models.CharField(max_length=64, verbose_name=b'Provider Private DNS', blank=True)),
                ('provider_private_ip', models.CharField(max_length=64, verbose_name=b'Provider Private IP Address', blank=True)),
                ('fqdn', models.CharField(max_length=255, verbose_name=b'FQDN', blank=True)),
                ('instance_id', models.CharField(max_length=32, verbose_name=b'Instance ID', blank=True)),
                ('sir_id', models.CharField(default=b'unknown', max_length=32, verbose_name=b'SIR ID')),
                ('sir_price', models.DecimalField(null=True, verbose_name=b'Spot Price', max_digits=5, decimal_places=2)),
                ('availability_zone', models.ForeignKey(related_name='hosts', to='cloud.CloudZone', null=True)),
                ('blueprint_host_definition', models.ForeignKey(related_name='hosts', to='blueprints.BlueprintHostDefinition')),
                ('cloud_image', models.ForeignKey(related_name='hosts', to='cloud.CloudImage')),
                ('instance_size', models.ForeignKey(related_name='hosts', to='cloud.CloudInstanceSize')),
                ('security_groups', models.ManyToManyField(related_name='hosts', to='cloud.SecurityGroup')),
            ],
            options={
                'ordering': ['blueprint_host_definition', '-index'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='title', verbose_name='slug', editable=False, blank=True)),
                ('status', model_utils.fields.StatusField(default=b'pending', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'pending', b'pending'), (b'launching', b'launching'), (b'configuring', b'configuring'), (b'syncing', b'syncing'), (b'provisioning', b'provisioning'), (b'orchestrating', b'orchestrating'), (b'finalizing', b'finalizing'), (b'destroying', b'destroying'), (b'finished', b'finished'), (b'starting', b'starting'), (b'stopping', b'stopping'), (b'terminating', b'terminating'), (b'executing_action', b'executing_action'), (b'error', b'error')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('namespace', models.CharField(max_length=64, verbose_name=b'Namespace')),
                ('create_users', models.BooleanField(verbose_name=b'Create SSH Users')),
                ('map_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_local_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('top_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=b'', storage=django.core.files.storage.FileSystemStorage(location=settings.STACKDIO_CONFIG.salt_core_states), max_length=255, blank=True, null=True)),
                ('orchestrate_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_orchestrate_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('global_orchestrate_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_orchestrate_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('pillar_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_local_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('global_pillar_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_local_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('props_file', stackdio.core.fields.DeletingFileField(default=None, upload_to=stackdio.api.stacks.models.get_local_file_path, storage=stackdio.api.stacks.models.stack_storage, max_length=255, blank=True, null=True)),
                ('blueprint', models.ForeignKey(related_name='stacks', to='blueprints.Blueprint')),
            ],
            options={
                'ordering': ('title',),
                'default_permissions': ('execute', 'delete', 'launch', 'admin', 'terminate', 'create', 'stop', 'update', 'start', 'ssh', 'orchestrate', 'provision', 'view'),
            },
        ),
        migrations.CreateModel(
            name='StackCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('status', model_utils.fields.StatusField(default=b'waiting', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'waiting', b'waiting'), (b'running', b'running'), (b'finished', b'finished'), (b'error', b'error')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Start Time', blank=True)),
                ('host_target', models.CharField(max_length=255, verbose_name=b'Host Target')),
                ('command', models.TextField(verbose_name=b'Command')),
                ('std_out_storage', models.TextField()),
                ('std_err_storage', models.TextField()),
                ('stack', models.ForeignKey(related_name='commands', to='stacks.Stack')),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'stack actions',
            },
        ),
        migrations.CreateModel(
            name='StackHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('status', model_utils.fields.StatusField(default=b'pending', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'pending', b'pending'), (b'launching', b'launching'), (b'configuring', b'configuring'), (b'syncing', b'syncing'), (b'provisioning', b'provisioning'), (b'orchestrating', b'orchestrating'), (b'finalizing', b'finalizing'), (b'destroying', b'destroying'), (b'finished', b'finished'), (b'starting', b'starting'), (b'stopping', b'stopping'), (b'terminating', b'terminating'), (b'executing_action', b'executing_action'), (b'error', b'error')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('status_detail', models.TextField(blank=True)),
                ('event', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=16, choices=[(b'DEBUG', b'DEBUG'), (b'INFO', b'INFO'), (b'WARNING', b'WARNING'), (b'ERROR', b'ERROR')])),
                ('stack', models.ForeignKey(related_name='history', to='stacks.Stack')),
            ],
            options={
                'ordering': ['-created', '-id'],
                'default_permissions': (),
                'verbose_name_plural': 'stack history',
            },
        ),
        migrations.AddField(
            model_name='host',
            name='stack',
            field=models.ForeignKey(related_name='hosts', to='stacks.Stack'),
        ),
        migrations.AlterUniqueTogether(
            name='stack',
            unique_together=set([('title',)]),
        ),
    ]

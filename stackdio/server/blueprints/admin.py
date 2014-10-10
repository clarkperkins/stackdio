# -*- coding: utf-8 -*-

# Copyright 2014,  Digital Reasoning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from django.contrib import admin

from . import models


class BlueprintAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'owner',
        'host_definition_count',
        'created',
        'modified',
    ]
admin.site.register(models.Blueprint, BlueprintAdmin)


class BlueprintHostDefinitionAdmin(admin.ModelAdmin):
    list_display = [
        'hostname_template',
        'blueprint',
        'cloud_profile',
        'count',
        'size',
        'zone',
        'subnet_id',
        'formula_components_count',
    ]
admin.site.register(models.BlueprintHostDefinition,
                    BlueprintHostDefinitionAdmin)


class BlueprintAccessRuleAdmin(admin.ModelAdmin):
    list_display = [
        'host',
        'protocol',
        'from_port',
        'to_port',
        'rule',
    ]
admin.site.register(models.BlueprintAccessRule, BlueprintAccessRuleAdmin)

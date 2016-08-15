# -*- coding: utf-8 -*-

# Copyright 2016,  Digital Reasoning
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

import logging

from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import serializers

from .fields import HyperlinkedParentField
from . import mixins, models, validators

logger = logging.getLogger(__name__)


class StackdioHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Override to use the appropriately namespaced url
    """

    def add_extra_kwargs(self, kwargs):
        """
        Hook to be able to add in extra kwargs
        (specifically for the StackdioParentHyperlinkedModelSerializer)
        """
        return kwargs

    def build_url_field(self, field_name, model_class):
        """
        Create a field representing the object's own URL.
        """
        field_class = self.serializer_url_field
        app_label = getattr(self.Meta, 'app_label', model_class._meta.app_label)
        model_name = getattr(self.Meta, 'model_name', model_class._meta.object_name.lower())
        lookup_field = getattr(self.Meta, 'lookup_field', 'pk')
        lookup_url_kwarg = getattr(self.Meta, 'lookup_url_kwarg', lookup_field)

        # Override user things
        if model_name in ('user', 'group', 'permission'):
            app_label = 'users'

        field_kwargs = {
            'view_name': 'api:%s:%s-detail' % (app_label, model_name),
            'lookup_field': lookup_field,
            'lookup_url_kwarg': lookup_url_kwarg,
        }

        field_kwargs = self.add_extra_kwargs(field_kwargs)

        return field_class, field_kwargs


class StackdioParentHyperlinkedModelSerializer(StackdioHyperlinkedModelSerializer):

    serializer_url_field = HyperlinkedParentField

    def add_extra_kwargs(self, kwargs):
        parent_attr = getattr(self.Meta, 'parent_attr', None)
        parent_lookup_field = getattr(self.Meta, 'parent_lookup_field', 'pk')
        default_parent_lookup_url_kwarg = 'parent_{}'.format(parent_lookup_field)
        parent_lookup_url_kwarg = getattr(self.Meta,
                                          'parent_lookup_url_kwarg',
                                          default_parent_lookup_url_kwarg)

        kwargs['parent_attr'] = parent_attr
        kwargs['parent_lookup_field'] = parent_lookup_field
        kwargs['parent_lookup_url_kwarg'] = parent_lookup_url_kwarg

        return kwargs


class StackdioLabelSerializer(mixins.CreateOnlyFieldsMixin,
                              StackdioParentHyperlinkedModelSerializer):
    """
    This is an abstract class meant to be extended for any type of object that needs to be labelled
    by setting the appropriate `app_label` and `model_name` attributes on the `Meta` class.

    ```
    class MyObjectLabelSerializer(StackdioLabelSerializer):

        # The Meta class needs to inherit from the super Meta class
        class Meta(StackdioLabelSerializer.Meta):
            app_label = 'my-app'
            model_name = 'my-object'
    ```
    """

    class Meta:
        model = models.Label
        parent_attr = 'content_object'
        lookup_field = 'key'
        lookup_url_kwarg = 'label_name'

        fields = (
            'url',
            'key',
            'value',
        )

        extra_kwargs = {
            'key': {'validators': [validators.LabelValidator()]},
            'value': {'validators': [validators.LabelValidator()]},
        }

        create_only_fields = (
            'key',
        )

    def validate(self, attrs):
        content_object = self.context.get('content_object')
        key = attrs.get('key')

        # Only need to validate if both a key was passed in and the content_object already exists
        if key and content_object:
            labels = content_object.labels.filter(key=key)

            if labels.count() > 0:
                raise serializers.ValidationError({
                    'key': ['Label keys must be unique.']
                })

        return attrs


class StackdioLiteralLabelsSerializer(StackdioLabelSerializer):

    class Meta(StackdioLabelSerializer.Meta):
        fields = (
            'key',
            'value',
        )


class StackdioModelPermissionsSerializer(serializers.Serializer):

    def validate(self, attrs):
        view = self.context['view']

        available_perms = view.get_model_permissions()
        bad_perms = []

        for perm in attrs['permissions']:
            if perm not in available_perms:
                bad_perms.append(perm)

        if bad_perms:
            raise serializers.ValidationError({
                'permissions': ['Invalid permissions: {0}'.format(', '.join(bad_perms))]
            })

        return attrs

    def create(self, validated_data):
        # Determine if this is a user or group
        view = self.context['view']
        user_or_group = view.get_user_or_group()

        # Grab our data
        auth_obj = validated_data[user_or_group]

        # Grab model class
        model_cls = validated_data['model_cls']
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.model_name

        for perm in validated_data['permissions']:
            assign_perm('%s.%s_%s' % (app_label, perm, model_name), auth_obj)

        return self.to_internal_value(validated_data)

    def update(self, instance, validated_data):
        # Determine if this is a user or group
        view = self.context['view']
        user_or_group = view.get_user_or_group()

        # The funkiness below is to prevent a client from submitting a PUT or PATCH request to
        # /api/<resource>/permissions/users/user_id1 with user="user_id2".  If this were
        # allowed, you could change the permissions of any user from the endpoint of any other user

        # Pull the user from the instance to update rather than from the incoming request
        auth_obj = instance[user_or_group]
        # Then add it to the validated_data so the create request uses the correct user
        validated_data[user_or_group] = auth_obj

        # Grab the object
        model_cls = validated_data['model_cls']
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.model_name

        if not self.partial:
            # PUT request - delete all the permissions, then recreate them later
            for perm in instance['permissions']:
                remove_perm('%s.%s_%s' % (app_label, perm, model_name), auth_obj)

        # We now want to do the same thing as create
        return self.create(validated_data)


class StackdioObjectPermissionsSerializer(serializers.Serializer):

    def validate(self, attrs):
        view = self.context['view']

        available_perms = view.get_object_permissions()
        bad_perms = []

        for perm in attrs['permissions']:
            if perm not in available_perms:
                bad_perms.append(perm)

        if bad_perms:
            raise serializers.ValidationError({
                'permissions': ['Invalid permissions: {0}'.format(', '.join(bad_perms))]
            })

        return attrs

    def create(self, validated_data):
        # Determine if this is a user or group
        view = self.context['view']
        user_or_group = view.get_user_or_group()

        # Grab our data
        auth_obj = validated_data[user_or_group]
        # Grab the object
        obj = validated_data['object']
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        for perm in validated_data['permissions']:
            assign_perm('%s.%s_%s' % (app_label, perm, model_name), auth_obj, obj)

        return self.to_internal_value(validated_data)

    def update(self, instance, validated_data):
        # Determine if this is a user or group
        view = self.context['view']
        user_or_group = view.get_user_or_group()

        # The funkiness below is to prevent a client from submitting a PUT or PATCH request to
        # /api/<resource>/<pk>/permissions/users/user_id1 with user="user_id2".  If this were
        # allowed, you could change the permissions of any user from the endpoint of any other user

        # Pull the user from the instance to update rather than from the incoming request
        auth_obj = instance[user_or_group]
        # Then add it to the validated_data so the create request uses the correct user
        validated_data[user_or_group] = auth_obj

        # Grab the object
        obj = validated_data['object']
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        if not self.partial:
            # PUT request - delete all the permissions, then recreate them later
            for perm in instance['permissions']:
                remove_perm('%s.%s_%s' % (app_label, perm, model_name), auth_obj, obj)

        # We now want to do the same thing as create
        return self.create(validated_data)

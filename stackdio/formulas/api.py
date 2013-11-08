import logging

from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from core.exceptions import BadRequest, ResourceConflict

from . import tasks
from . import serializers
from . import models

logger = logging.getLogger(__name__)


class FormulaListAPIView(generics.ListCreateAPIView):

    model = models.Formula
    serializer_class = serializers.FormulaSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self):
        return self.request.user.formulas.all()

    def pre_save(self, obj):
        obj.owner = self.request.user

    def create(self, request, *args, **kwargs):
        uri = request.DATA.get('uri', '')
        public = request.DATA.get('public', False)

        if not uri:
            raise BadRequest('uri field is required')

        # check for duplicate uri
        try:
            formula = self.model.objects.get(uri=uri, owner=request.user)
            raise ResourceConflict('A formula already exists with this '
                                   'uri: {0}'.format(uri))
        except self.model.DoesNotExist:
            pass

        formula = self.model.objects.create(owner=request.user,
                                         public=public,
                                         uri=uri,
                                         status=self.model.IMPORTING,
                                         status_detail='Importing formula...this could take a while.')

        # Import using asynchronous task
        tasks.import_formula.si(formula.id)()

        return Response(self.get_serializer(formula).data)


class FormulaPublicAPIView(generics.ListAPIView):
    model = models.Formula
    serializer_class = serializers.FormulaSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self):
        return self.model.objects \
            .filter(public=True) \
            .exclude(owner=self.request.user)


class FormulaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    model = models.Formula
    serializer_class = serializers.FormulaSerializer
    parser_classes = (JSONParser,)

    def get_object(self):
        '''
        Return the formula if it's owned by the request user or
        if it's public...else we'll raise a 404
        '''
        return get_object_or_404(self.model,
                                 Q(owner=self.request.user) | Q(public=True),
                                 pk=self.kwargs.get('pk'))

    def update(self, request, *args, **kwargs):
        '''
        Override PUT requests to only allow the public field to be changed.
        '''
        formula = self.get_object()

        # Only the owner can submit PUT/PATCH requests
        if formula.owner != request.user:
            raise BadRequest('Only the owner of a formula may modify it.')

        public = request.DATA.get('public', None)
        if public is None or len(request.DATA) > 1:
            raise BadRequest("Only 'public' field of a formula may be modified.")

        if not isinstance(public, bool):
            raise BadRequest("'public' field must be a boolean value.")


        # Update formula's public field
        formula.public = public
        formula.save()

        return Response(self.get_serializer(formula).data)

    def delete(self, request, *args, **kwargs):
        '''
        Override the delete method to check for ownership.
        '''
        formula = self.get_object()
        if formula.owner != request.user:
            raise BadRequest('Only the owner of a formula may delete it.')
        return super(FormulaDetailAPIView, self).delete(request, *args, **kwargs)


class FormulaPropertiesAPIView(generics.RetrieveAPIView):

    model = models.Formula
    serializer_class = serializers.FormulaPropertiesSerializer

    def get_object(self):
        '''
        Return the formula if it's owned by the request user or
        if it's public...else we'll raise a 404
        '''
        return get_object_or_404(self.model,
                                 Q(owner=self.request.user) | Q(public=True),
                                 pk=self.kwargs.get('pk'))


class FormulaComponentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    model = models.FormulaComponent
    serializer_class = serializers.FormulaComponentSerializer
    parser_classes = (JSONParser,)

    def get_object(self):
        return get_object_or_404(self.model,
                                 pk=self.kwargs.get('pk'),
                                 formula__owner=self.request.user)


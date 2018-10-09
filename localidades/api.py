# -*- coding: utf-8 -*-

# Importaciones Django

# Importaciones Terceros
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from tastypie import fields

# Importaciones Propias
from freesbid.core.query import normalize_query, get_query
from .models import Localidad, Provincia, Departamento


class ProvinciaResource(ModelResource):

	class Meta:
		queryset = Provincia.objects.all()
		resource_name = 'provincia'
		serializer = Serializer(formats=['json'])
		filtering = {
			'nombre' : ALL,
			'id': ALL,
		}
		always_return_data = True


class DepartamentoResource(ModelResource):

	class Meta:
		queryset = Departamento.objects.all()
		resource_name = 'departamento'
		serializer = Serializer(formats=['json'])
		filtering = {
			'nombre' : ALL,
		}
		always_return_data = True
		list_allowed_methods = ['get']



class LocalidadResource(ModelResource):

	provincia = fields.ForeignKey(ProvinciaResource, 'provincia', full=True)
	departamento = fields.ForeignKey(DepartamentoResource, 'departamento')

	class Meta:
		queryset = Localidad.objects.all().select_related('provincia', 'departamento')
		resource_name = 'localidad'
		serializer = Serializer(formats=['json'])
		filtering = {
			'provincia' : ALL_WITH_RELATIONS,
			'nombre' : ALL_WITH_RELATIONS,
		}
		always_return_data = True
		limit = 0
		max_limit = 0
		list_allowed_methods = ['get']


	def apply_filters(self, request, applicable_filters):
		base_object_list = super(LocalidadResource, self).apply_filters(request, applicable_filters)
		query = request.GET.get('q', None)
		if query:
			entry_query = get_query(query, ['nombre'])
			base_object_list = base_object_list.filter(entry_query).distinct()
		return base_object_list
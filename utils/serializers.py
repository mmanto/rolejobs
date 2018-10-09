# encoding=utf-8

from __future__ import unicode_literals

from rest_framework import serializers


class ChoicesSerializer(serializers.Serializer):
    """This is read only serializer for list choices"""

    name = serializers.CharField(max_length=250, required=True)
    value = serializers.CharField(max_length=100, required=True)

    def create(self):
        raise Exception("Read only serializer")

    def update(self):
        self.create()

    @classmethod
    def parse_data(cls, choices):
        return [{"name": n, "value": v} for v, n in choices]

    @classmethod
    def from_choice(cls, choice):
        return ChoicesSerializer({
            "name": str(choice[1]),
            "value": str(choice[0])
        })


class SimpleItemSerializer(serializers.Serializer):
    """Simple item serializer, for SimpleItemModel"""

    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=100, required=True)


class SimpleItemDescSerializer(SimpleItemSerializer):
    """Simple item desc serializer"""

    description = serializers.CharField(max_length=300, required=False)


class SlugedItemSerializer(SimpleItemDescSerializer):
    """Sluged item serializer"""

    slug = serializers.CharField(
        max_length=40,
        read_only=True)


class PkListSerializer(serializers.Serializer):
    """Pk list serializer"""

    pks = serializers.ListField(
        child=serializers.IntegerField(min_value=1)
    )


class PkListField(serializers.RelatedField):
    """Pk list field for serializers"""

    def __init__(self, *args, **kwargs):
        self._model = kwargs.pop('model', None)
        super(PkListField, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        super(PkListField, self).get_queryset(*args, **kwargs)

    def to_representation(self, value):
        return [int(item.pk) for item in value.all()]

    def to_internal_value(self, value):
        if self._model is not None:
            return [self._model.objects.get(pk=int(pk)) for pk in value]
        else:
            return [int[pk] for pk in value]

    def run_validation(self, data=""):
        if data == "":
            data = None

        return data


class SubModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self._pass_id = kwargs.pop("pass_id", False)
        super(SubModelSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        id = data.get("id", None)

        data = super(SubModelSerializer, self).to_internal_value(data)

        if self._pass_id:
            data.update({"id": id})

        return data


class ModelWithSubModelsSerializer(serializers.ModelSerializer):

    def update_sub_element(self, instance, data, model):
        return data

    def create_parts(self, instance, model, items, **kwargs):
        update_data = kwargs.get("update", None)

        if update_data is not None:
            for i in items:
                i.update(update_data)
        else:
            items = [self.update_sub_element(instance, data, model)
                     for data in items]

        models = [model(**data) for data in items]

        return model.objects.bulk_create(models)

    def save_parts(self, instance, rel_name, model, items, **kwargs):
        local_qs = getattr(instance, rel_name)

        new_items = [i for i in items
                     if i.get("id", None) is None]

        to_update = {i["id"]: i for i in items
                     if i.get("id", None) is not None}

        actuals = {i.id: i for i in local_qs.all()}

        self.create_parts(instance, model, new_items, **kwargs)

        for id, actual in actuals.items():
            if id in to_update:
                data = to_update.get(id)
                for key in data.keys():
                    setattr(actual, key, data.get(key, getattr(actual, key)))

                actual.save(force_update=True)
            else:
                actual.delete()

from rest_framework import serializers
from rest_framework.utils import model_meta


class ExtraFieldModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


def data_is_many(data):
    if isinstance(data, (list, tuple)):
        return True
    return False


def wrapping_flat_data(instance, validated_data):
    data = {}
    for model_field in model_meta.get_field_info(instance).fields:
        model_field_data = validated_data.get(model_field, None)
        if model_field_data is not None:
            data[model_field] = model_field_data
    return data


def get_extra_model_flat_data(instance, field, validated_data):
    v_data = validated_data.get(field, None)
    if v_data is None:
        v_data = validated_data
        for model_field in model_meta.get_field_info(instance).fields:
            if model_field in validated_data.keys():
                validated_data.pop(model_field)
    else:
        validated_data.pop(field)

    if data_is_many(v_data):
        return [wrapping_flat_data(instance, item) for item in v_data], validated_data
    return wrapping_flat_data(instance, v_data), validated_data


class ExtraRelationModelSerializer(ExtraFieldModelSerializer):

    def create(self, validated_data):
        if getattr(self.Meta, 'extra_models', None):
            for model, field in self.Meta.extra_models:
                extra_model_data, validated_data = get_extra_model_flat_data(model, field, validated_data)
                if data_is_many(extra_model_data) and self.extra_model_can_many(field):
                    validated_data[field] = []
                    for the_data in extra_model_data:
                        m_data, _ = model.objects.get_or_create(**the_data)
                        validated_data[field].append(m_data)
                else:
                    m_data, _ = model.objects.get_or_create(**extra_model_data)
                    validated_data[field] = m_data
        return super(ExtraRelationModelSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if getattr(self.Meta, 'extra_models', None):
            for model, field in self.Meta.extra_models:
                extra_model_data, validated_data = get_extra_model_flat_data(model, field, validated_data)
                if data_is_many(extra_model_data) and self.extra_model_can_many(field):
                    validated_data[field] = []
                    for the_data in extra_model_data:
                        m_data, _ = model.objects.update_or_create(**the_data)
                        validated_data[field].append(m_data)
                else:
                    m_data, _ = model.objects.update_or_create(**extra_model_data)
                    validated_data[field] = model.objects.update(m_data)
        return super(ExtraRelationModelSerializer, self).update(instance, validated_data)

    def save(self, **kwargs):
        assert not hasattr(self, 'save_object'), (
                'Serializer `%s.%s` has old-style version 2 `.save_object()` '
                'that is no longer compatible with REST framework 3. '
                'Use the new-style `.create()` and `.update()` methods instead.' %
                (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def is_valid(self, raise_exception=False):
        target_valid = super(ExtraRelationModelSerializer, self).is_valid()
        if getattr(self.Meta, 'extra_models', None) and target_valid:
            for _, field in self.Meta.extra_models:
                if field in self.fields:
                    extra_serializer_class = self.fields.get(field).__class__

                    if data_is_many(self.initial_data[field]):

                        if self.extra_model_can_many(field) is False:
                            self._errors = {field: "field can't many."}
                            return False
                        for initial_data in self.initial_data[field]:
                            extra_serializer = extra_serializer_class(data=initial_data)
                            if extra_serializer.is_valid() is False:
                                self._errors = extra_serializer.errors
                                return False

                    else:
                        extra_serializer = extra_serializer_class(data=self.initial_data[field])
                        if extra_serializer.is_valid() is False:
                            self._errors = extra_serializer.errors
                            return False
        return target_valid

    def extra_model_can_many(self, field):
        if getattr(self.Meta, 'model', None):
            model = getattr(self.Meta, 'model')
            model_fields = model_meta.get_field_info(model).fields
            if model_fields.get(field).one_to_one:
                return False
            return True
        return False


class ExtraListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):

        extra_serializer_class = self.get_extra_serializer_class()
        instances = []
        for item in validated_data:
            data = extra_serializer_class().update(item)
            instances.append(data)
        return instances

    def create(self, validated_data):
        extra_serializer_class = self.get_extra_serializer_class()
        instances = []
        for item in validated_data:
            data = extra_serializer_class().create(item)
            instances.append(data)
        return instances

    def is_valid(self, raise_exception=False):
        extra_serializer_class = self.get_extra_serializer_class()
        if extra_serializer_class is None:
            raise ValueError(
                'Cannot get Meta extra_serializer_class.'
            )
        v_data = []
        for item in self.initial_data:
            extra_serializer = extra_serializer_class(data=item)
            if extra_serializer.is_valid() is False:
                self._errors = extra_serializer.errors
                return False
            v_data.append(extra_serializer.validated_data)
        self._validated_data = v_data
        return True

    def get_extra_serializer_class(self):
        if hasattr(self.Meta, 'extra_serializer_class'):
            return getattr(self.Meta, 'extra_serializer_class')
        return None

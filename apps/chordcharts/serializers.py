from rest_framework import serializers
from .models import Section, Line, Measure, Chord


class SectionSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `chart_id` field.
            attrs['chart_id'] = self.context['chart_id']

        return super(SectionSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = Section
        fields = (
            'id',
            'key_distance_from_chart',
            'number',
            'alt_name',
            'time_signature'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `chart_id` field.
            attrs['section_id'] = self.context['section_id']

        return super(SubsectionSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = Section
        fields = ('id', 'number')


class LineSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `section_id` field.
            attrs['subsection_id'] = self.context['subsection_id']

        return super(LineSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = Line
        fields = ('id', 'number')


class MeasureSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `line_id` field.
            attrs['line_id'] = self.context['line_id']

        return super(MeasureSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = Measure
        fields = ('id', 'number', 'beat_schema')


class ChordSerializer(serializers.ModelSerializer):

    chord_type_id = serializers.PrimaryKeyRelatedField(source='chord_type')

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `line_id` field.
            attrs['measure_id'] = self.context['measure_id']

        return super(ChordSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = Chord
        fields = (
            'id',
            'order',
            'beats',
            'chord_type_id',
            'chord_pitch',
            'alt_bass',
            'alt_bass_pitch'
        )
import json

from django.shortcuts import render, redirect
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponsePermanentRedirect
)
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from songs.models import Song
from core.helpers.fields_maxlength import fields_maxlength

from .models import Chart, Key, ChordType
from .settings import BOXED_CHART
from .helpers.new_chart import ProcessNewChartPost, FormErrors
from .helpers.keys_json import keys_json


def song_index(request):

    context = {
        'songs': Song.objects.all()
    }

    return render(request, 'chordcharts/song_index.html', context)


def chart(request, song_slug, chart_id, key_tonic=None, edit=False):
    """
    Renders the view for the chart.

    Could be the normal chart or view edit version. In case of the edit
    version, `edit` should be `True`.
    """

    def get_key(chart, key_tonic):
        """
        Returns the key for the given `key_tonic` or `None` if
        `key_tonic` was invalid.
        """
        if key_tonic:
            try:
                return Key.objects.get(
                    tonic=key_tonic,
                    tonality=chart.key.tonality
                )
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def get_chart_data(edit, key):

        kwargs = {
            'edit': edit
        }

        if key:
            kwargs['transpose_to_tonic'] = key.tonic

        return chart.client_data(**kwargs)

    def get_chord_types_sets(chord_types):
        """
        Returns two sets of chord types lists.
        """
        return (chord_types[:12], chord_types[12:])

    def get_chord_types_json(chord_types):
        """
        Returns the JSON representation of the given `chord_types`.
        """
        return json.dumps(
            [chord_type.client_data() for chord_type in chord_types]
        )

    def get_redirect_wrong_slugs(chart, key, song_slug, key_tonic):
        """
        Returns a redirect response in case the given `song_slug` isn't
        equal to the chart's song's slug, and/or if the given
        `key_tonic` is invalid. Otherwise returns `None`.
        """

        redirect = False
        reverse_kwargs = {}

        if song_slug != chart.song.slug:
            redirect = True

        if key_tonic:
            if key:
                reverse_kwargs['key_tonic'] = key_tonic
            else:
                # If `key` is `None`, it means that the `key_tonic` was
                # invalid. In this case we want to redirect, so it will
                # go to the default key.
                redirect = True

        if redirect:

            reverse_kwargs['chart_id'] = chart.id
            reverse_kwargs['song_slug'] = chart.song.slug

            if edit:
                view = 'chordcharts:edit_chart'
            else:
                view = 'chordcharts:chart'

            return HttpResponsePermanentRedirect(
                reverse(view, kwargs=reverse_kwargs)
            )

    chart = get_object_or_404(Chart, id=chart_id)
    key = get_key(chart, key_tonic)
    redirect_wrong_slugs = get_redirect_wrong_slugs(
        chart, key, song_slug, key_tonic
    )

    if redirect_wrong_slugs:
        return redirect_wrong_slugs
    else:

        if edit:
            # Only clean up the chart in edit mode, because if we always
            # do it it might become a bit too much. Besides that,
            # "unclean" charts should work nevertheless.
            chart.cleanup()

        chart_data = get_chart_data(edit, key)
        all_keys = Key.objects.all()
        chart_keys = all_keys.filter(tonality=chart.key.tonality)
        chord_types = ChordType.objects.all()

        context = {
            'settings': BOXED_CHART,
            'settings_json': json.dumps(BOXED_CHART),
            'chart': chart_data,
            'chart_json': json.dumps(chart_data),
            'chart_keys': chart_keys,
            'all_keys_json': keys_json(all_keys),
            'chord_types_sets': get_chord_types_sets(chord_types),
            'chord_types_json': get_chord_types_json(chord_types),
            'edit': edit,
            'key_select_tonics': Key.TONIC_CHOICES
        }

        return render(request, 'chordcharts/chart/base.html', context)


def new_chart(request):
    """
    Returns a view where you can create new charts.
    """

    def get_keys():
        """
        Returns a dict with a list of keys for each tonality.
        """

        keys = {}

        for key in Key.objects.all():

            if key.tonality not in keys:
                keys[key.tonality] = []

            keys[key.tonality].append(key)

        return keys

    def get_maxlength():
        """
        Returns the maximum lengths for the fields used in the form.

        Will be a dict with the fieldname in the key and the maximum
        lenght in the value.
        """

        maxlength = fields_maxlength(Song, ['name'])
        maxlength['song_name'] = maxlength.pop('name')
        maxlength.update(
            fields_maxlength(
                Chart, ['short_description', 'video_url', 'lyrics_url']
            )
        )

        return maxlength

    response = None
    errors = []

    if request.method == 'POST':

        try:
            chart = ProcessNewChartPost(request).process()
        except FormErrors as formErrors:
            errors = formErrors.errors
        else:
            response = redirect(
                'chordcharts:edit_chart',
                song_slug=chart.song.slug,
                chart_id=chart.id
            )

    if not response:

        keys = get_keys()

        context = {
            'all_keys_json': keys_json(Key.objects.all()),
            'key_select_tonics': Key.TONIC_CHOICES,
            'keys_major': keys[Key.TONALITY_MAJOR],
            'keys_minor': keys[Key.TONALITY_MINOR],
            'maxlength': get_maxlength(),
            'errors': errors
        }

        response = render(request, 'chordcharts/new_chart.html', context)

    return response


def delete_chart(request, song_slug, chart_id):
    """
    On a POST, will delete the chart with id `chart_id`.
    """

    if request.method == 'POST':

        try:
            chart = Chart.objects.get(id=chart_id)
        except ObjectDoesNotExist:
            response = HttpResponseBadRequest('Song not found')
        else:

            song = chart.song
            chart.delete()

            if song.charts.count() == 0:
                song.delete()

            context = {
                'song_name': request.POST.get('song_name')
            }

            response = render(
                request,
                'chordcharts/chart_deleted.html',
                context
            )

    else:
        response = HttpResponse(status=405)

    return response


def how_to_read(request):
    return render(request, 'chordcharts/how_to_read.html')


def chord_symbols(request):

    context = {
        'chord_types': ChordType.objects.all()
    }

    return render(request, 'chordcharts/chord_symbols.html', context)

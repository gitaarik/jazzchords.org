# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Chord.measure'
        db.alter_column(u'chordcharts_chord', 'measure_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chordcharts.Measure']))

    def backwards(self, orm):

        # Changing field 'Chord.measure'
        db.alter_column(u'chordcharts_chord', 'measure_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chordcharts.Line']))

    models = {
        u'chordcharts.chart': {
            'Meta': {'object_name': 'Chart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Key']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['songs.Song']"})
        },
        u'chordcharts.chord': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('measure', 'order'),)", 'object_name': 'Chord'},
            'alternative_bass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'alternative_bass_pitch': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'beats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'chord_pitch': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'chord_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.ChordType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Measure']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'chordcharts.chordtype': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ChordType'},
            'chord_output': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'chordcharts.key': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('tonality', 'order'),)", 'object_name': 'Key'},
            'distance_from_c': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '25'}),
            'tonality': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'tone': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'chordcharts.line': {
            'Meta': {'object_name': 'Line'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Section']"})
        },
        u'chordcharts.measure': {
            'Meta': {'object_name': 'Measure'},
            'beat_schema': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Line']"}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'chordcharts.note': {
            'Meta': {'ordering': "('distance_from_root',)", 'object_name': 'Note'},
            'distance_from_root': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Key']"}),
            'key_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'chordcharts.section': {
            'Meta': {'ordering': "('number',)", 'unique_together': "(('chart', 'number'),)", 'object_name': 'Section'},
            'alt_title': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'chart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chordcharts.Chart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_distance_from_chart': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'songs.song': {
            'Meta': {'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['chordcharts']
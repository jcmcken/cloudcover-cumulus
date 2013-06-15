# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Host'
        db.create_table(u'cumulus_host', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'cumulus', ['Host'])

        # Adding unique constraint on 'Host', fields ['name', 'ip']
        db.create_unique(u'cumulus_host', ['name', 'ip'])

        # Adding model 'Key'
        db.create_table(u'cumulus_key', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cumulus', ['Key'])

        # Adding model 'Datum'
        db.create_table(u'cumulus_datum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cumulus.Key'])),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cumulus.Host'])),
        ))
        db.send_create_signal(u'cumulus', ['Datum'])

        # Adding unique constraint on 'Datum', fields ['host', 'key']
        db.create_unique(u'cumulus_datum', ['host_id', 'key_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Datum', fields ['host', 'key']
        db.delete_unique(u'cumulus_datum', ['host_id', 'key_id'])

        # Removing unique constraint on 'Host', fields ['name', 'ip']
        db.delete_unique(u'cumulus_host', ['name', 'ip'])

        # Deleting model 'Host'
        db.delete_table(u'cumulus_host')

        # Deleting model 'Key'
        db.delete_table(u'cumulus_key')

        # Deleting model 'Datum'
        db.delete_table(u'cumulus_datum')


    models = {
        u'cumulus.datum': {
            'Meta': {'unique_together': "(('host', 'key'),)", 'object_name': 'Datum'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cumulus.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cumulus.Key']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'cumulus.host': {
            'Meta': {'unique_together': "(('name', 'ip'),)", 'object_name': 'Host'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cumulus.key': {
            'Meta': {'object_name': 'Key'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cumulus']
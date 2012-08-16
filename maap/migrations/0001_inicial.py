# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MaapModel'
        db.create_table('maap_maapmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created', null=True, to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('maap', ['MaapModel'])

        # Adding model 'MaapPoint'
        db.create_table('maap_maappoint', (
            ('maapmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapModel'], unique=True, primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.Icon'], null=True, blank=True)),
        ))
        db.send_create_signal('maap', ['MaapPoint'])

        # Adding model 'MaapArea'
        db.create_table('maap_maaparea', (
            ('maapmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapModel'], unique=True, primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal('maap', ['MaapArea'])

        # Adding model 'Icon'
        db.create_table('maap_icon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('maap', ['Icon'])


    def backwards(self, orm):
        # Deleting model 'MaapModel'
        db.delete_table('maap_maapmodel')

        # Deleting model 'MaapPoint'
        db.delete_table('maap_maappoint')

        # Deleting model 'MaapArea'
        db.delete_table('maap_maaparea')

        # Deleting model 'Icon'
        db.delete_table('maap_icon')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.icon': {
            'Meta': {'object_name': 'Icon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.maaparea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapArea', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.maapmodel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapModel'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        'maap.maappoint': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapPoint', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.Icon']", 'null': 'True', 'blank': 'True'}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['maap']
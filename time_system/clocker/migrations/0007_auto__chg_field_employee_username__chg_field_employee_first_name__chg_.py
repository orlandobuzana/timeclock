# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Employee.username'
        db.alter_column(u'clocker_employee', 'username', self.gf('django.db.models.fields.TextField')(unique=True))

        # Changing field 'Employee.first_name'
        db.alter_column(u'clocker_employee', 'first_name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Employee.last_name'
        db.alter_column(u'clocker_employee', 'last_name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Job.name'
        db.alter_column('Job', 'name', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Employee.username'
        db.alter_column(u'clocker_employee', 'username', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True))

        # Changing field 'Employee.first_name'
        db.alter_column(u'clocker_employee', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'Employee.last_name'
        db.alter_column(u'clocker_employee', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'Job.name'
        db.alter_column('Job', 'name', self.gf('django.db.models.fields.CharField')(max_length=25))

    models = {
        u'clocker.employee': {
            'Meta': {'ordering': "['username']", 'object_name': 'Employee'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 8, 0, 0)'}),
            'first_name': ('django.db.models.fields.TextField', [], {}),
            'has_salary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hire_date': ('django.db.models.fields.DateField', [], {}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'salary': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        u'clocker.job': {
            'Meta': {'ordering': "['-is_active']", 'object_name': 'Job', 'db_table': "'Job'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'clocker.shift': {
            'Meta': {'ordering': "['-time_in', 'employee']", 'object_name': 'Shift', 'db_table': "'Shift'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'clocker.shiftsummary': {
            'Meta': {'ordering': "['shift', 'employee', 'job']", 'unique_together': "(('job', 'shift'),)", 'object_name': 'ShiftSummary', 'db_table': "'Shift Summary'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Job']"}),
            'miles': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Shift']"})
        }
    }

    complete_apps = ['clocker']
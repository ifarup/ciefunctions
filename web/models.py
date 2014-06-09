from django.db import models

# Create your models here.

class Result(models.Model):
	field_size = models.FloatField()
	age = models.IntegerField()
	lambda_min = models.FloatField()
	lambda_max = models.FloatField()
	lambda_step = models.FloatField()
	data = models.TextField() 
	
	def __unicode__(self):
		return u'%s %s' % (self.age, self.field_size)
		
	def get_data(self):
		return self.data

class Plot(models.Model):
	field_size = models.FloatField()
	age = models.IntegerField()
	lambda_min = models.FloatField()
	lambda_max = models.FloatField()
	lambda_step = models.FloatField()
	data = models.TextField() 
	
	def __unicode__(self):
		return u'%s %s' % (self.age, self.field_size)
		
	def get_data(self):
		return self.data


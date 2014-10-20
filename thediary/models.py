from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class EventCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField("Event name", max_length=256, null=True, blank=True)
    category = models.ForeignKey(EventCategory)
    description = models.TextField("Event description", null=True, blank=True)
    date = models.DateField("Day of activity")
    duration_s = models.PositiveIntegerField("Duration in seconds")
    user = models.ForeignKey(User, null=True, blank=True)

    def save_model(self, request, instance, form, change):
        if form:
            instance = form.save(commit=False)
            if not change or not instance.created_by:
                instance.user = request.user
            form.save_m2m()
            instance.save()
        return instance

    def __str__(self):
        return self.__unique__()

    def __unique__(self):
        if self.name:
            return '%s(%s) at %s for %.2f hours' % (self.name, self.category.name, self.date, float(self.duration_s)/3600.0)
        else:
            return '%s at %s for %.2f hours' % (self.category.name, self.date, float(self.duration_s)/3600.0)


class EventForm(ModelForm):
    class Meta:
        labels = {
            'duration_s': 'Duration in minutes',
        }
        model = Event
        fields = ['category','duration_s','date', 'name', 'description' ]

    def clean_duration_s(self):
        return self.cleaned_data['duration_s']*60

    def clean_date(self):
        print self.cleaned_data['date']
        print type(self.cleaned_data['date'])
        return self.cleaned_data['date']


class EventCategoryForm(ModelForm):
    class Meta:
        model = EventCategory
        fields = [ 'name' ]

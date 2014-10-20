import datetime

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext

from thediary.models import EventForm, EventCategoryForm, EventCategory
@staff_member_required
def index(request):
    extra_message = None
    form_category = EventCategoryForm()
    form = EventForm({'date': datetime.date.today(), 'category': EventCategory.objects.all()[0], 'duration_s': 60 })
    if request.method == 'POST':
        if 'submit_category' in request.POST:
            form_category = EventCategoryForm(request.POST, request.FILES)
            if form_category.is_valid():
                category = form_category.save(commit=False)
                category.save()
                form.data['category'] = category
                extra_message = 'Category saved successfully'
                # do something.
            else:
                extra_message = 'entry not valid'
        elif 'submit_event' in request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                extra_message = 'Event saved successfully'
                # do something.
            else:
                extra_message = 'entry not valid'

    return render(request, "index.html", RequestContext(request, {
        "form": form,
        "form_category": form_category,
        "extra_message": extra_message,
    }))

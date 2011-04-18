# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource
from forms import DataSourceForm
from mongoengine.django.auth import User

def index(request):
    
    form = DataSourceForm()

    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES)
        import ipdb; ipdb.set_trace()
        if form.is_valid():
            form.save()

        return redirect("/")


    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects.order_by('created'),
            'form': form,
        }
    )


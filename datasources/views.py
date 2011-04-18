# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource
from forms import DataSourceForm
from mongoengine.django.auth import User

def index(request):
    
    form = DataSourceForm()

    if request.method == 'POST':
       form = DataSourceForm(request.POST, request.FILES)

       if form.is_valid():
            data = form.cleaned_data
            attach = data['attach']
            datasource = DataSource()
            datasource.name = data['name']
            datasource.attach.put(
                attach.read(), 
                content_type=attach.content_type, 
                filename=attach.name,
            )
            import ipdb; ipdb.set_trace()
            datasource.author = User.objects.get(username=data['author'])
            datasource.save()

       return redirect("/")


    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects.order_by('created'),
            'form': form,
        }
    )


# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource, Column
from forms import DataSourceForm, ColumnFormSet, ColumnForm

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from mongoengine import connect
from bson.objectid import ObjectId

def index(request):
 
    form = DataSourceForm()
    column_form = ColumnFormSet()
    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES)
        column_form = ColumnFormSet(request.POST)
        if form.is_valid():
            datasource = form.save()
        else:
            pass
        return redirect("/")


    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects.order_by('created'),
            'form': form,
            'column_form': column_form
        }
    )

def detail(request, id):
    column_form = ColumnForm()
    datasource = DataSource.objects.get(id=id)
    return render(
        request,
        'detail.html',
        {
            'datasource': datasource,
            'columns': datasource.column_set.all(),
            'column_form':column_form,
            
        }
    )
    
    
def column(request, id):
    instance = Column.objects.get(pk=id)
    db = connect('sitseg')
    dataset = db.data.group(
        key={instance.label:1},
        condition={'datasource_id':3},
        initial={'count':0},
        reduce="function(obj,prev){prev.count ++;}"
    )
    dataindex = dict([(d[instance.label],d['count']) for d in dataset]) 
    if id and request.method == "POST":
        instance.has_geodata = request.POST.get('has_geodata')
        instance.is_available = request.POST.get('is_available')
        instance.save()
        
        return redirect('detail', instance.datasource_id)
    return render(
        request,
        'column.html',
        {
            'column':instance,
            'dataset': dataindex,
            'label':instance.label,
            
        }
    )

def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response


def autogenerate_columns(request, id):
    datasource = DataSource.objects.get(id=id)
    datasource.import_columns()
    return redirect('detail', datasource.pk)

def import_data(request, id):
    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
    datasource = DataSource.objects.get(id=id)
    datasource.generate_documents()
    return redirect("/")


def data_formatted(data, doclist):
    """ takes a plain data and columns info and generate a list of labeled values"""
    for document in data:
        doc_formatted = []
        for column in doclist:
            doc_formatted.append(dict(
                label = column.name,
                key = column.label,
                value = document[column.label],
                field_type = column.data_type
            ))
            
        yield doc_formatted

def show_data(request, id):
    datasource = DataSource.objects.get(id=id)    
    data = datasource.find()[:1]

    return render(
        request,
        'data.html',
        {
            'datasource': datasource,
            'columns':datasource.column_set.all(),            
            'data': data_formatted(data, datasource),
        }
    )

def document_edit(request):
    pass

def document_detail(request):
    pass
    
def document_add(request):
    pass

#def document_list(request, datasource_id):
#    datasource = DataSource.objects.get(id=datasource_id)    
#    data = datasource.find()[:100]
#    columns = datasource.column_set.all()[:3]

def show_data(request, id):
    datasource = DataSource.objects.get(id=id)
    data = datasource.find()[:1]
    columns = datasource.column_set.all()
    return render(
        request,
        'document_list.html',
        {
            'datasource': datasource,
            'columns': columns,            
            'data': data_formatted(data, columns),
        }
    )

def geometry_append(request, datasource_id, id):
    db = connect('sitseg')
    # This create the collection if not exists previously
    data_collection = db['data']
    
    column_id = request.get("column_id", "")
    maapmodel_id = request.get("maapmodel_id", "")
    
    oid = ObjectId(id)
    document_args = dict()
    document_args[column_id+"_geom_id"] = maapmodel_id
    
    data_collection.find_one({"_id": oid}).update(document_args)
    
    return redirect('detail', id)


def scatter_plot(request, datasource_id):
    datasource = DataSource.objects.get(pk=datasource_id)

    columns = datasource.column_set.all()
    context = {
        'datasource': datasource,
        'columns': columns,            
    }

    if request.method == 'POST':
        db = connect('sitseg')
        column1 = request.POST.get('column1', None)
        column2 = request.POST.get('column2', None)
        
        data = db.data.find({'datasource_id': int(datasource_id)}, {column1:1,column2:1})
        datalist = [{
                column1:item[column1],
                column2:item[column2],                
            } for item in data]
        
        context['scatterdata'] = datalist
        context['labels'] = [column1, column2]
    return render(
        request,
        'scatter_form.html',
        context,
    )    


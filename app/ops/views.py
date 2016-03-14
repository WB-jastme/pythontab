from django.shortcuts import render
from django.contrib import auth
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.template import Context,RequestContext
#from django.template import loader, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ops.models import server,passets

# test enviroment clean nginx cache
import commands
def nginx(request,string):
    try:
        m=commands.getoutput(''' ansible %s -m shell -a "sh /opt/script/clean_cache.sh"  ''' %string)
        return render_to_response('interface/nginx_interface.html',{'result':m})
    except Exception as e:
        return render_to_response('interface/nginx_interface.html',{'result':e})
        

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main')
            else:
                login_error = 'login error.'
                return render_to_response('index.html', {'login_error' : login_error, 'is_display' : 'display:block'})
        else:
            login_error = 'login error.'
            return render_to_response('index.html', {'login_error' : login_error, 'is_display' : 'display:block'})
    return render_to_response('index.html', {'is_display' : 'display:none'})

@login_required
def mylogout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

#index
def main(request):
    return render_to_response('main/main.html')

@login_required
def assets(request):
    asset=server.objects.all()
    return render_to_response('assets/assets.html',{'user':request.user,'asset':asset},context_instance=RequestContext(request))


@login_required
def addserver(request):
    if request.method == 'POST':
        vhostname = request.POST['hostname']
        vband = request.POST['band']
        vraid = request.POST['raid']
        vdisk = request.POST['disk']
        vmemory = request.POST['memory']
        vcpu = request.POST['cpu']
        vinterface_out = request.POST['interface_out']
        vinterface_in = request.POST['interface_in']
        vos = request.POST['os']
        vsn = request.POST['sn']
        vfan = request.POST['fan']
        vowner = request.POST['owner']
        vtime = request.POST['time']
        ps=server(hostname=vhostname,band=vband,raid=vraid,disk=vdisk,memory=vmemory,cpu=vcpu,interface_out=vinterface_out,interface_in=vinterface_in,os=vos,sn=vsn,fixed_assets_encoding=vfan,owner=vowner,time=vtime)
        ps.save()
        return HttpResponseRedirect('/assets')
    else:
        return render_to_response('assets/addserver.html')

#passets
@login_required
def personal(request):
    passet=passets.objects.all()
    return render_to_response('assets/passets.html',{'user':request.user,'passet':passet},context_instance=RequestContext(request))

#interface
@login_required
def clean_cache(request):
    try:
        m=commands.getoutput(''' ansible nginx_group -m shell -a "sh /opt/script/clean_cache.sh"  ''')
        m=m.split('\n')
        return render_to_response('interface/clean_cache.html',{'result':m})
    except Exception as m:
        return render_to_response('interface/clean_cache.html',{'result':m})

#check_log
#@login_required
from pykafka import KafkaClient
def check_log(request):
    
    try:
        m=['start comsume from zookeeper\r\n if only this information,no log comsume']
        client = KafkaClient(hosts="172.31.9.125:2181,172.31.9.125:2182,172.31.9.125:2183")
        topic = client.topics['t_nginx']
        balanced_consumer= topic.get_balanced_consumer(
            consumer_group='group1',
            auto_commit_enable=True,
            consumer_timeout_ms=5000,
            zookeeper_connect='172.31.9.125:2181,172.31.9.125:2182,172.31.9.125:2183'
        )
        for message in balanced_consumer:
            if message is not None:
                 m.append(message.value)
                 
                 print m
            else:
                 m='no logs'
                 print m
        return render_to_response('interface/log.html',{'result':m})
    except Exception as m:
        print m
        return render_to_response('interface/log.html',{'result':m})

#ops
@login_required
def ops(request):
    return render_to_response('ops/ops.html')

#douments pages

#@login_required
#def documents(request):
#    project=d_category.objects.all()
#    doc=docs.objects.all()
#    return render_to_response('Documents/Documents.html',{'project':project,'doc':doc,'user':request.user},context_instance=RequestContext(request))
#
#@login_required
#def adddocuments(request):
#    item=d_category.objects.all()
#    if request.method == 'POST':
#        vtitle=request.POST['title']
#        vca=request.POST['ca']
#        vauthor=request.POST['author']
#        vdate=request.POST['date']
#        vdocument=request.POST['document']
#        ps=docs(title=vtitle,category=vca,author=vauthor,date=vdate,text=vdocument)
#        ps.save()
#        return HttpResponseRedirect('/Documents')
#    else:
#        return render_to_response('Documents/adddocuments.html',{'item':item})
#
#@login_required
#def doc_filter(request,by):
#    project=d_category.objects.all()
#    doc=docs.objects.filter(category=by)
#    return render_to_response('Documents/Documents.html',{'project':project,'doc':doc},context_instance=RequestContext(request))
#
#@login_required
#def doc_modify(request,i_id):
#    items=d_category.objects.all()
#    item=docs.objects.get(id=i_id)
#    if request.method == 'POST':
#        vtitle=request.POST['title']
#        vca=request.POST['ca']
#        vauthor=request.POST['author']
#        vdate=request.POST['date']
#        vtext=request.POST['text']
#        docs.objects.filter(id=i_id).update(title=vtitle,category=vca,author=vauthor,date=vdate,text=vtext)
#    return render_to_response('Documents/doc_modify.html',{'item':item,'items':items})
#
#@login_required
#def doc_delete(request,i_id):
#    docs.objects.filter(id=int(i_id)).delete()
#    return HttpResponseRedirect('/Documents')
#
#@login_required
#def d_cancel(request):
#    return HttpResponseRedirect('/Documents')
#
#import commands    
#@login_required
#def logs(request):
#    if request.method == 'POST':
#        server = request.POST['server']
#        logname = request.POST['logname']
#        starttime = request.POST['starttime']
#        endtime = request.POST['endtime']
#        keyword = request.POST['keyword']
#        content = commands.getoutput('''awk -F:"[|]|,| " '$2 > "%s" && $2 < "%s"' /opt/%s | grep "%s"''' %(starttime,endtime,logname,keyword))
#        for i in content.split('\n'):
#            print i
#        return render_to_response('Logs/Logs.html',{'user':request.user,'content':content.split('\n')})
#    return render_to_response('Logs/Logs.html',{'user':request.user})
#
#import numpy as np
#import pandas as pd
#from pandas import Series,DataFrame
##import matplotlib.pyplot as plt
##@login_required
#def an_log(request):
#    f=open('/opt/reslut.txt').readlines()
#    f=eval(f[0])
#    d={}
#    for k,v in f.iteritems():
#        if v > 5000:
#            d[k]=v
##    plt.figure(figsize=(20,6), dpi=80)
##    ts = Series(d)
##    ts.plot(kind='barh')
##    plt.savefig('/var/www/jastme/static/images/log.png')
##    plt.figure(figsize=(20,8), dpi=80)
##    ts.plot(kind='pie')
##    plt.savefig('/var/www/jastme/static/images/pie.png')
#    categories = d.keys()
#    data = d.values()
##    print categories,data
#    return render_to_response('An_Log/an_log.html',{'user':request.user,'categories':categories,'data':data})
#
#import nmap
#@login_required
#def autodevops(request):
#    nm = nmap.PortScanner()
#    if request.method == 'POST':
#        hosts = request.POST['hosts']
#        hosts = hosts.split(',')
#        d={}
#        for i in hosts:
#            k=nm.scan(i,'22')
#            try:
#                d[i]=k.get('scan').get(i).get('status').get('state')
#            except:
#                d[i]='None'
#        return render_to_response('assets/Autoassets.html',{'user':request.user,'d':d.iteritems()})
#    return render_to_response('assets/Autoassets.html',{'user':request.user})

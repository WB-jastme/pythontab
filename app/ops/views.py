# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib import auth
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.template import Context,RequestContext
from app.settings import MEDIA_ROOT
#from django.template import loader, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ops.models import server,inventory
import commands,re
import simplejson as json
# test enviroment clean nginx cache
def nginx(request,string):
    try:
        m=commands.getoutput(''' ansible %s -m shell -a "sh /opt/script/test.sh"  ''' %string)
        m=m.split('\n')
        return render_to_response('mysite/api/test.html',{'result':m})
    except Exception as m:
        m=m.split('\n')
        return render_to_response('mysite/api/test.html',{'result':m})
        

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
@login_required
def main(request):
    return render_to_response('mysite/root/index.html',{'user':request.user},context_instance=RequestContext(request))

@login_required
def IDC_SC(request):
    servers=server.objects.filter(idc="sc")
    return render_to_response('mysite/servers/idc_sc.html',{'user':request.user,'servers':servers},context_instance=RequestContext(request))

@login_required
def IDC_BJ(request):
    servers=server.objects.filter(idc="bj")
    return render_to_response('mysite/servers/idc_bj.html',{'user':request.user,'servers':servers},context_instance=RequestContext(request))

@login_required
def IDC_SH(request):
    servers=server.objects.filter(idc="sh")
    return render_to_response('mysite/servers/idc_sh.html',{'user':request.user,'servers':servers},context_instance=RequestContext(request))

@login_required
def add_server(request):
    if request.method == 'POST':
        hostname = request.POST['hostname']
        band = request.POST['band']
        raid = request.POST['raid']
        disk = request.POST['disk']
        memory = request.POST['memory']
        cpu = request.POST['cpu']
        interface_out = request.POST['in_out']
        interface_in = request.POST['in_in']
        os = request.POST['os']
        sn = request.POST['sn']
        idc = request.POST['idc']
        ps=server(hostname=hostname,
                  band=band,
                  raid=raid,
                  disk=disk,
                  memory=memory,
                  cpu=cpu,
                  interface_out=in_out,
                  interface_in=in_in,
                  os=os,
                  sn=sn,
                  idc=idc)
        ps.save()
        if idc == "sc":
            return HttpResponseRedirect('/IDC_SC')
        elif idc == "bj":
            return HttpResponseRedirect('/IDC_BJ')
        elif idc == "SH":
            return HttpResponseRedirect('/IDC_SH')
        else:
            pass
    else:
        return render_to_response('mysite/servers/add_server.html')

import commands
@login_required
def ansible_adhoc(request):
    group=inventory.objects.all()
    if request.method == 'POST':
        hosts = request.POST['hosts']
        module = request.POST['module']
        script = request.POST['script']
        print hosts,module,script
        try:
            if module == 'setup':
                m=commands.getoutput(''' ansible %s -m %s ''' %(hosts,module))
                m=m.split('\n')
                command = ''' ansible %s -m %s ''' %(hosts,module)
                return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group,'reslut':m,'command':command},context_instance=RequestContext(request))
            elif module == 'command':    
                m=commands.getoutput(''' ansible %s -m %s -a "%s" ''' %(hosts,module,script))
                m=m.split('\n')
                command = ''' ansible %s -m %s -a "%s" ''' %(hosts,module,script)
                return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group,'reslut':m,'command':command},context_instance=RequestContext(request))
            else:
                m=commands.getoutput(''' ansible %s -m %s -a "sh %s" ''' %(hosts,module,script))
                m=m.split('\n')
                command = ''' ansible %s -m %s -a "sh %s" ''' %(hosts,module,script)
                return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group,'reslut':m,'command':command},context_instance=RequestContext(request))
        except Exception as m:
            m=m.split('\n')
            return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group,'reslut':m},context_instance=RequestContext(request))
    return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group},context_instance=RequestContext(request))   

@login_required
def ansible_playbook(request):
    '''
    查看playbook然后执行,确认
    '''
    group=inventory.objects.all()
    if request.method == 'POST':
        playbook = request.POST['playbook']
        try:
            m=commands.getoutput(''' ansible-playbook /etc/ansible/playbooks/%s ''' %(playbook))
            m=m.split('\n')
            command = ''' ansible-playbook /etc/ansible/playbooks/%s ''' %(playbook)
            return render_to_response('mysite/ansible/ansible_playbook.html',{'groups':group,'command':command,'reslut':m},context_instance=RequestContext(request))
        except Exception as m:
            m=m.split('\n')
            return render_to_response('mysite/ansible/ansible_ad_hoc.html',{'groups':group,'reslut':m},context_instance=RequestContext(request))
    return render_to_response('mysite/ansible/ansible_playbook.html',{'groups':group},context_instance=RequestContext(request)) 
        
#interface
@login_required
def clean_cache(request):
    try:
        m=commands.getoutput(''' ansible nginx_group -m shell -a "sh /opt/script/clean_cache.sh"  ''')
        m=m.split('\n')
        return render_to_response('interface/clean_cache.html',{'result':m})
    except Exception as m:
        return render_to_response('interface/clean_cache.html',{'result':m})

#@login_required
from pykafka import KafkaClient
def comsumer_log(request):
    if request.method == 'POST':
        t=request.POST['topic']
        try:
            m=['start comsume from zookeeper\r\n if only this information,no logs in kafka']
            client = KafkaClient(hosts="192.168.1.1:2181")
            type(t)
            t=t.encode('utf8')
            topic = client.topics[t]
            balanced_consumer= topic.get_balanced_consumer(
                consumer_group='group1',
                auto_commit_enable=True,
                consumer_timeout_ms=1000,
                zookeeper_connect='192.168.1.1:2181'
            )
            for message in balanced_consumer:
                if message is not None:
                     m.append(message.value)
                else:
                     m='no logs'
            return render_to_response('mysite/logs/comsumer_log.html',{'result':m})
        except Exception as m:
            return render_to_response('mysite/logs/comsumer_log.html',{'result':m})
    else:
        return render_to_response('mysite/logs/comsumer_log.html',context_instance=RequestContext(request))

@login_required
def tail_log(request):
    alllog = commands.getoutput(''' find /tmp -name "*.log" ''').split('\n')
    if request.method == 'POST':
        lines = request.POST['lines']
        logs = request.POST['logs']
        try:
            m = commands.getoutput(''' tail -n %s %s  ''' %(lines,logs)).split('\n')
            return render_to_response('mysite/logs/tail_log.html',
                                      {'alllog':alllog,'lines':lines,'logs':logs,'result':m},
                                      context_instance=RequestContext(request))
        except Exception as m:
            return render_to_response('mysite/logs/tail_log.html',{'result':m})
    else:
        return render_to_response('mysite/logs/tail_log.html',
                                      {'alllog':alllog},
                                      context_instance=RequestContext(request))      

@login_required
def an_log(request):
    '''目前只处理nginx的access.log'''
    logs = "/var/log/nginx/access.log".split()
#    logs = "/tmp/access.log".split()
    if request.method == 'POST':
        log = request.POST['logs']
        httplist=[]
        f=open(log)
        ff=f.readlines()
        d={}
        for code in ff:
            httpcode = re.findall(r'HTTP/1.1"(.*)"http',code)
            if len(httpcode) > 0:
                httpcode = httpcode[0].split()[0]
                httplist.append(httpcode)
        codes = list(set(httplist))
        for i in codes:
            if i in httplist:
                d[i]=httplist.count(i)
        state = d.keys()
        times = d.values()
        piedata = json.dumps(map(list,zip(state,times)))
        return render_to_response('mysite/logs/an_log.html',{'state':state,'times':times,'logs':logs,'piedata':piedata},context_instance=RequestContext(request))
    return render_to_response('mysite/logs/an_log.html',{'logs':logs},context_instance=RequestContext(request))

def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            files = request.FILES['file']
            fd = open('%s%s' % (MEDIA_ROOT,files), 'wb')
            print type(files)
            for content in files.chunks():
                fd.write(content)  
                fd.close() 
            return render_to_response('mysite/files/upload_files.html',{'message':'upload Done'},context_instance=RequestContext(request))
        return render_to_response('mysite/files/upload_files.html',{'message':'no file select'},context_instance=RequestContext(request))
    return render_to_response('mysite/files/upload_files.html')
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

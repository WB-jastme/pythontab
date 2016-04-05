from django.conf.urls import patterns, include, url
from django.contrib import admin
from ops import views 
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jastme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#    url(r'^assets/$',views.assets,name='assets'),
#    url(r'^personal/$',views.personal,name='personal'),
    (r'^$',views.index),
    url(r'^main/$',views.main,name='main'),
    url(r'^servers/sc$',views.IDC_SC,name='servers_sc'),
    url(r'^servers/bj$',views.IDC_BJ,name='servers_bj'),
    url(r'^servers/sh$',views.IDC_SH,name='servers_sh'),
    url(r'^servers/add$',views.add_server,name='add_server'),
    url(r'^ansible/ad-hoc$',views.ansible_adhoc,name='ansible_adhoc'),
    url(r'^ansible/playbook$',views.ansible_playbook,name='ansible_playbook'),
    url(r'^logs/comsumer_log$',views.comsumer_log,name='comsumer_log'),
#    url(r'^logs/tail_log$',views.tail_log,name='tail_log'),
    url(r'^interface/(?P<string>\S+)/$',views.nginx,name='nginx'),
    url(r'^api/clean_cache$',views.clean_cache,name='clean_cache'),
#    url(r'^api/check_log$',views.check_log,name='check_log'),
    url(r'^ops/$',views.ops,name='ops'),
#    url(r'^DevOps/list_modify/(?P<i_id>\d+)/$',views.list_modify,name='list_modify'),
#    url(r'^DevOps/list_delete/(?P<i_id>\d+)/$',views.list_delete,name='list_delete'),
#    url(r'^Documents/$',views.documents,name='documents'),
#    url(r'^Documents/(?P<by>\w+)/$',views.doc_filter,name='doc_filter'),
#    url(r'^Documents/adddocuments$',views.adddocuments,name='adddocuments'),
#    url(r'Documents/doc_modify/(?P<i_id>\d+)/$',views.doc_modify,name='doc_modify'),
#    url(r'Documents/doc_delete/(?P<i_id>\d+)/$',views.doc_delete,name='doc_delete'),
#    url(r'^Documents/d_cancel/$',views.d_cancel,name='d_cancel'),
#    url(r'^Logs/$',views.logs,name='logs'),
#    url(r'^log_analysis/$',views.an_log,name='an_log'),
    url(r'^logout/$',views.mylogout,name='mylogout'),
#    url(r'^AutoDevOps/$',views.autodevops,name='autodevops'),
)

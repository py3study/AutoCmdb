from django.conf.urls import url,include
from web.views import index,host,ansible
app_name = 'web'

urlpatterns = [
    url(r'^$', index.index,name="index"),
    url(r'^index/', index.index,name="index"),
    url(r'^default/', index.default,name="default"),
    url(r'^host/list/', host.list,name="list"),
    url(r'^host/info/(?P<pk>\d+)/$', host.info,name="info"),
    # url(r'^host/add/', host.add,name="add"),

    url(r'^host/cpu/monitor/(?P<pk>\d+)/$', host.cpu,name="cpu"),
    url(r'^host/memory/monitor/(?P<pk>\d+)/$', host.memory,name="memory"),

    url(r'^ansible/list/', ansible.list,name="ansible_list"),
    url(r'^ansible/add/', ansible.add,name="ansible_add"),
    url(r'^ansible/add_host/(?P<pk>\d+)/$', ansible.add_host,name="ansible_add_host"),

]
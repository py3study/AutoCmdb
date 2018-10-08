from django.conf.urls import url,include
from api.views import host,hostinfo,disk,network,ansible
from api.views.monit import cpu,memory
app_name = 'api'

urlpatterns = [
   url(r'host/(?P<pk>\d+)/$',host.HostView.as_view({'get':'get_msg'}),name='host'),
   url(r'host/list/$',host.HostView.as_view({'post':'list'}),name='list'),

   url(r'host/hostinfo/(?P<pk>\d+)/$',hostinfo.HostInfoView.as_view({'get':'get_msg'}),name='info'),
   url(r'host/disk/(?P<pk>\d+)/$',disk.DiskView.as_view({'get':'get_msg'}),name='disk'),
   url(r'host/network/(?P<pk>\d+)/$',network.NetworkView.as_view({'get':'get_msg'}),name='network'),
   url(r'host/add/$',host.HostView.as_view({'post':'add'}),name='add'),
   url(r'host/delete/(?P<pk>\d+)/$',host.HostView.as_view({'delete':'delete'}),name='delete'),

   url(r'cpu/add/$',cpu.CpuView.as_view({'post':'add'}),name='cpu'),
   url(r'memory/add/$',memory.MemoryView.as_view({'post':'add'}),name='memory'),

   url(r'cpu/chart_json/(?P<pk>\d+)/$',cpu.CpuView.as_view({'get':'chart_json'}),name='chart_cpu'),
   url(r'memory/chart_json/(?P<pk>\d+)/$',memory.MemoryView.as_view({'get':'chart_json'}),name='chart_memory'),

   url(r'ansible/add/$',ansible.AnsibleView.as_view({'post':'add'}),name='ansible_add'),
   url(r'ansible/list/$',ansible.AnsibleView.as_view({'post':'list'}),name='ansible_list'),
   url(r'ansible/add_host/$',ansible.AnsibleView.as_view({'post':'add_host'}),name='ansible_add_host'),
   url(r'ansible/delete/(?P<pk>\d+)/$',ansible.AnsibleView.as_view({'delete':'delete'}),name='ansible_delete'),
]
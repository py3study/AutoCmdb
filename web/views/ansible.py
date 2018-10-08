from django.shortcuts import render


# Create your views here.
def list(request):
    return render(request,"ansible_list.html")

def add(request):
    return render(request,"ansible_add.html")

def add_host(request,pk):
    return render(request,"ansible_add_host.html",{'pk':pk})
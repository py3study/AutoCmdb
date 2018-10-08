from django.shortcuts import render


# Create your views here.
def list(request):
    return render(request,"host_list.html")

def info(request,pk):
    return render(request,"host_info.html",{'pk':pk})

# def add(request):
#     return render(request,"host_add.html")

def cpu(request,pk):
    return render(request,"monitor/cpu.html",{'pk':pk})

def memory(request,pk):
    return render(request,"monitor/memory.html",{'pk':pk})
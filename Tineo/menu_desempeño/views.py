from django.shortcuts import render

# Create your views here.
def mostrarMenu(request):
    return render(request,'menuBase.html')
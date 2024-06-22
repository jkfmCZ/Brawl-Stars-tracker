from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .utils import graph_gen as gen

def index(request):
    if request.method == "POST":
        your_name = request.POST.get('your_name')
        print(f"Received POST data: {your_name}")
        # Do something with the name, like saving it to the database or processing
        # return HttpResponse(f"Hello, {your_name}!")  # Just an example response
    
    return render(request, "index.html")

def p_report(request):
  print(request.GET)
  return render(request,"report.html", {})

def p_games(request):
  pie_plot = gen.lossxwins()
  bar_plot = gen.bar_ratio
  

  return render(request, "p_games.html",{"pie_plot":pie_plot, "bar_plot":bar_plot })
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
  return render(request, "index.html",{})

def p_report(request, tag):
  print(tag)
  return render(request,"report.html", {})
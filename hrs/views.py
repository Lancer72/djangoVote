from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
depts_list=[
    {'no':10,'name':'财务部','location':'北京'},
    {'no': 20, 'name': '研发部', 'location': '成都'},
    {'no': 30, 'name': '销售部', 'location': '上海'},
]

def index(requset):
    return render(requset,'index.html',{'depts_list':depts_list})
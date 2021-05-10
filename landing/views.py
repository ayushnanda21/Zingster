from django.shortcuts import render
from django.views import View #(generic class view)

class Index(View):
    def get(self,request, *args, **kwargs):
        return render(request,'landing/index.html')

def Contact(request):
    return render(request,'landing/contact.html')




from django.shortcuts import render



def test_views(request):
    return render(request,'base.html')

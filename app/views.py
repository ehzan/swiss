from django.shortcuts import render

# Create your views here.


def players(request):
    return render(request, 'players.html', {})

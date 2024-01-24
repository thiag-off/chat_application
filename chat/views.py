from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def room(request, room_name):
    return render( request, 'chat/room.html', {'room_name' : room_name})

@csrf_exempt
def index(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        room_name = request.POST['room']
        request.session['nickname'] = nickname
        return redirect('room', room_name = room_name)
    else:
        return render(request, "chat/index.html")
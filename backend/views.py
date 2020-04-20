from django.shortcuts import render
import uuid
def index_view(request):
	uid=uuid.uuid1()
	return render(request, 'index.html',{'uid':uid})

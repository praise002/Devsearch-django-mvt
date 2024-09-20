from django.shortcuts import render

def custom_server_error_view(request):
    return render(request, "common/500.html", status=500)

def custom_404(request, exception):
    return render(request, 'common/404.html', status=404)


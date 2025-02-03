from django.shortcuts import render

def my_error_404(request, exception):
    return render(request, 'no_found.html', status=404)

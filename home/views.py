from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parse'
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})

def reports(request):
    return render(request, 'home/reports.html')
def budget(request):
    return render(request, 'home/budget.html')
def profile(request):
    return render(request, 'home/profile.html')
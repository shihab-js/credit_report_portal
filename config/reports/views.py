from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CreditReport, RequestedReport

@login_required
def dashboard(request):
    reports = CreditReport.objects.all()
    return render(request, 'reports/dashboard.html', {'reports': reports})
@login_required
def upload_report(request):
    if request.method == 'POST':
        CreditReport.objects.create(
            lc_number=request.POST['lc_number'],
            client_name=request.POST['client_name'],
            beneficiary_name=request.POST['beneficiary_name'],
            beneficiary_address=request.POST['beneficiary_address'],
            beneficiary_country=request.POST['beneficiary_country'],
            expiry_date=request.POST['expiry_date'],
            credit_risk=request.POST['credit_risk'],
            related_party=request.POST['related_party'],
            line_of_business=request.POST['line_of_business'],
            vendor_name=request.POST['vendor_name'],
            document=request.FILES['document'],
            entry_by=request.user   # 👈 logged-in user
        )
        return redirect('dashboard')

    return render(request, 'reports/upload.html')
@login_required
def search_report(request):
    query = request.GET.get('q')
    reports = CreditReport.objects.filter(beneficiary_name__icontains=query)
    return render(request, 'reports/search.html', {'reports': reports})
@login_required
def view_report(request, pk):
    report = get_object_or_404(CreditReport, pk=pk)
    return render(request, 'reports/view.html', {'report': report})

@login_required
def request_report(request):
    if request.method == 'POST':
        RequestedReport.objects.create(
            lc_number=request.POST['lc_number'],
            client_name=request.POST['client_name'],
            beneficiary_name=request.POST['beneficiary_name'],
            beneficiary_address=request.POST['beneficiary_address'],
            beneficiary_country=request.POST['beneficiary_country'],
            related_party=request.POST['related_party'],
            vendor_name=request.POST['vendor_name'],
           # request_date
            request_by=request.user  # 👈 logged-in user
        )
        return redirect('dashboard')

    return render(request, 'reports/request_report.html')

@login_required
def download_report(request):
    #report = get_object_or_404(CreditReport, pk=pk)
    return render(request, 'reports/download_report.html')
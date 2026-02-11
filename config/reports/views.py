from django.shortcuts import render
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CreditReport, RequestedReport,Vendor

@login_required
def dashboard(request):
    reports = CreditReport.objects.all()
    today = timezone.now().date()  # current date

    report_count = reports.count()
    vendor_count = reports.values('vendor_name').distinct().count()
    expired_count = reports.filter(expiry_date__lt=today).count()  # expired reports
    valid_count = reports.filter(expiry_date__lt=today).count()  # valid items

    return render(request, 'reports/dashboard.html', {
        'reports': reports,
        'report_count': report_count,
        'vendor_count': vendor_count,
        'expired_count': expired_count,
        'valid_count': valid_count,
    })


@login_required
def upload_report(request):
    vendors = Vendor.objects.all()  # needed for the dropdown

    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_name')  # from dropdown
        vendor = Vendor.objects.get(id=vendor_id)   # get the Vendor instance

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
            vendor_name=vendor,          # assign the ForeignKey
            document=request.FILES['document'],
            entry_by=request.user        # logged-in user
        )

        return redirect('dashboard')

    return render(request, 'reports/upload.html', {'vendors': vendors})

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

def logout_view(request):
    logout(request)
    return redirect('login')

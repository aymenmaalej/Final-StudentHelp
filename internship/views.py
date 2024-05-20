from django.shortcuts import render, redirect
from .forms import InternshipProposalForm  
from .models import Stage   

# Create your views here.


def internship_selection(request):
    return render(request, 'internship_selection.html')
    
def new_internship_proposal(request):
    if request.method == 'POST':
        form = InternshipProposalForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('index')
    else:
        form = InternshipProposalForm()
    return render(request, 'new_internship_proposal.html', {'form': form})
def view_internship_offers(request):
    stages = Stage.objects.all()  
    return render(request, 'view_internship_offers.html', {'stages': stages})
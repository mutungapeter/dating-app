from django.shortcuts import render
from .forms import AgeSubmissionForm


def age_submission_view(request):
    initial_data = {'birthday': '1970-01-01'}  
    if request.method == 'POST':
        form = AgeSubmissionForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['birthday']
            return render(request, 'success.html')
            
    else:
        form = AgeSubmissionForm(initial=initial_data)  

    return render(request, 'test.html', {'form': form})

##To go dynamic , uncomment the code below and comment out the one above

# def age_submission_view(request):
#     if request.method == 'POST':
#         form = AgeSubmissionForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return render(request, 'success.html')
#     else:
#         form = AgeSubmissionForm()

#     return render(request, 'test.html', {'form': form})
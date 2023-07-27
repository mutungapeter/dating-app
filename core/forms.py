from django import forms
from .models import User
from django.utils import timezone
class AgeSubmissionForm(forms.Form):
    birthday = forms.DateField()

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday:
            today = timezone.now().date()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            if age < 18:
                raise forms.ValidationError("Users below 18 years are not allowed.")
        return birthday
            


##To go dynamic , uncomment the code below and comment out the one above

# class AgeSubmissionForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['birthday']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         today = timezone.now().date()
#         age = today.year - self.cleaned_data['birthday'].year - ((today.month, today.day) < (self.cleaned_data['birthday'].month, self.cleaned_data['birthday'].day))
#         default_birthday = today.replace(year=today.year - age)
#         if not user.birthday:
#             user.birthday = default_birthday
#         if commit:
#             user.save()
#         return user
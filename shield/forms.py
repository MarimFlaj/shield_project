
from django import forms
from django.utils.translation import gettext_lazy as _

from shield.models import DepartmentModel, SendingTrainingModel, SendingURlsModel, TrainingPackage, Url, User

class RegisterForm(forms.ModelForm):
    
    retype_password = forms.CharField(label=_("Retype Password"))
    Department = forms.ModelChoiceField(
        queryset=DepartmentModel.objects.all(),
        empty_label="   Department",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 0px; '
                'border: 0px; '
                # 'text-align: center !important; '
                'color: gray;'
                'background-color:#eee;'
            ),
        })
    )
    
    def clean_retype_password(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')
        if password and retype_password and password != retype_password:
            mess=_("Password Not Match")
            self.add_error('retype_password', mess) 
        return retype_password
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.fields['password'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password'})
        self.fields['retype_password'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password'})

        # Add RegexValidator for password strength
        # password_validator = RegexValidator(
        #     regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        #     message=_("Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters.")
        # )
        # self.fields['password'].validators.append(password_validator)


       
   
    class Meta: 
        model=User
        fields=[
            "username",
            "f_name",
            #"m_name",
            "l_name",
            "email",
            "gander",
            "Department",
            "password",
        ]
        


class UrlForm(forms.ModelForm):
    
    
    class Meta: 
        model=Url
        fields='__all__'
    
class TrainingPackageForm(forms.ModelForm):
        
    
    class Meta: 
        model=TrainingPackage
        fields='__all__'



class DepartmentForm(forms.ModelForm):
     
    class Meta: 
        model=DepartmentModel
        fields='__all__'


class SendingURlsForm(forms.ModelForm):
    Department = forms.ModelChoiceField(
        queryset=DepartmentModel.objects.all(),
        empty_label="Select Department",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        }),
        required=False
    )

    U_ID = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        empty_label="Select User",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        }),
        required=False
    )
    
    URL_ID = forms.ModelChoiceField(
        queryset=Url.objects.all(),
        empty_label="Select Url",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        })
    )
    class Meta: 
        model=SendingURlsModel
        fields='__all__'

class SendingTrainingForm(forms.ModelForm):
    Department = forms.ModelChoiceField(
        queryset=DepartmentModel.objects.all(),
        empty_label="Select Department",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        }),
        required=False
    )

    U_ID = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False,phishing_awareness="unaware"),
        empty_label="Select User",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        }),
        required=False
    )
    
    Train_ID = forms.ModelChoiceField(
        queryset=TrainingPackage.objects.all(),
        empty_label="Select Training",  # النص المعرض بدل النقاط الافتراضية
        widget=forms.Select(attrs={
            'style': (
                'width: 100%; '
                'border-radius: 9px; '
                'height: 40px; '
                'border-right: 5px solid #2F3270 !important; '
                'border: 1.5px solid #2F3270 !important; '
                # 'text-align: center !important; '
                'color: #2F3270;'
            ),
        })
    )
    class Meta: 
        model=SendingTrainingModel
        fields='__all__'

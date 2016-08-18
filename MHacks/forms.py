from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from MHacks.widgets import ArrayFieldSelectMultiple, MHacksAdminFileWidget
from models import MHacksUser, Application
from utils import validate_url


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=128, strip=False, widget=forms.PasswordInput)
    password.longest = True

    def confirm_login_allowed(self, user):
        if not user.email_verified:
            error = forms.ValidationError('Email not verified.', code='unverified')
            error.user_pk = urlsafe_base64_encode(force_bytes(user.pk))
            raise error
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm Password"
        self.fields['password2'].longest = True

    class Meta:
        model = MHacksUser
        fields = ('first_name', 'last_name', "email",)


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.fields['school'].cols = 12
        self.fields['is_high_school'].cols = 12
        self.fields['is_high_school'].end_row = 12
        self.fields['is_international'].cols = 12
        self.fields['is_international'].end_row = 12
        self.fields['is_high_school'].general = True

        self.fields['is_high_school'].end_row = True
        self.fields['birthday'].end_row = True

        self.fields['major'].end_row = True
        self.fields['grad_date'].end_row = True

        self.fields['race'].cols = 6
        self.fields['gender'].cols = 6
        self.fields['birthday'].demographic = True
        self.fields['race'].previous = True

        self.fields['github'].cols = 6
        self.fields['devpost'].cols = 6
        self.fields['devpost'].end_row = True

        self.fields['personal_website'].cols = 6
        self.fields['resume'].cols = 6
        self.fields['resume'].end_row = True

        self.fields['num_hackathons'].cols = 12
        self.fields['num_hackathons'].end_row = True
        self.fields['mentoring'].interests = True

        self.fields['cortex'].short = True

        self.fields['github'].required = False
        self.fields['devpost'].required = False
        self.fields['personal_website'].required = False
        self.fields['other_info'].required = False
        self.fields['gender'].required = False
        self.fields['race'].required = False

        self.fields['other_info'].travel = True

        # if the user is from UMich, exclude the short answer and reimbursement/travel fields
        if self.user and 'umich.edu' in self.user.email:
            for key in ['passionate', 'coolest_thing', 'other_info', 'needs_reimbursement', 'can_pay', 'from_city', 'from_state']:
                del self.fields[key]
                self.fields['cortex'].short = False


    class Meta:
        from application_lists import TECH_OPTIONS
        model = Application

        # use all fields except for these
        exclude = ['user', 'deleted', 'score', 'reimbursement', 'submitted']

        labels = {
            'school': 'School or University',
            "grad_date": 'Expected graduation date',
            'birthday': 'Date of birth',
            'is_high_school': 'I am a high school student.',
            'is_international': 'I am an international student.',
            'github': '',
            'devpost': '',
            'personal_website': '',
            'cortex': 'CTRL/CMD + click to multi-select!',
            'passionate': 'Tell us about a project that you worked on and why you\'re proud of it. This doesn\'t have to be a hack! (150 words max)',
            'coolest_thing': 'What do you hope to take away from MHacks 8? (150 words max)',
            'other_info': 'Anything else you want to tell us?',
            'num_hackathons': 'How many hackathons have you attended? (Put 0 if this is your first!)',
            'can_pay': 'How much of the travel cost can you pay?',
            'mentoring': 'I am interested in mentoring other hackers!',
            'needs_reimbursement': 'I will be needing travel reimbursement to attend MHacks.',
            'from_city': 'Which city will you be traveling from?',
            'from_state': 'Which state or country will you be traveling from? (Type your country if you are traveling internationally)',
            'gender': 'Preferred gender pronouns',
            'resume': 'Resume (If you don\'t have a formal resume, you can upload a skills sheet, a bullet-pointed list, etc!)'
        }

        widgets = {
            "grad_date": forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY', 'id': 'graduation_date'}),
            'cortex': ArrayFieldSelectMultiple(attrs={'class': 'checkbox-inline checkbox-style'}, choices=TECH_OPTIONS),
            'birthday': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'school': forms.TextInput(attrs={'placeholder': 'Hackathon College', 'class': 'form-control input-md', 'id': 'school-autocomplete'}),
            'major': forms.TextInput(attrs={'placeholder': 'Hackathon Science', 'class': 'form-control input-md', 'id': 'major-autocomplete'}),
            'gender': forms.TextInput(attrs={'placeholder': 'Pro/Pro/Pro', 'id': 'gender-autocomplete'}),
            'race': forms.TextInput(attrs={'placeholder': 'Hacker', 'id': 'race-autocomplete'}),
            'github': forms.TextInput(attrs={'placeholder': 'GitHub', 'class': 'form-control input-md'}),
            'devpost': forms.TextInput(attrs={'placeholder': 'Devpost', 'class': 'form-control input-md'}),
            'personal_website': forms.TextInput(attrs={'placeholder': 'Personal Website', 'class': 'form-control input-md'}),
            'other_info': forms.Textarea(attrs={'class': 'textfield form-control'}),
            'coolest_thing': forms.Textarea(attrs={'class': 'textfield form-control'}),
            'passionate': forms.Textarea(attrs={'class': 'textfield form-control'}),
            'resume': MHacksAdminFileWidget(attrs={'class': 'input-md form-control'}),
            'from_state': forms.TextInput(attrs={'placeholder': 'State or country', 'id': 'state-autocomplete'})
        }

    # custom validator for urls
    def clean_github(self):
        data = self.cleaned_data['github']
        validate_url(data, 'github.com')
        return data

    def clean_devpost(self):
        data = self.cleaned_data['devpost']
        validate_url(data, 'devpost.com')
        return data

    def clean_major(self):
        data = self.cleaned_data['major']
        if not self.cleaned_data['is_high_school'] and not data:
            raise forms.ValidationError('Please enter your major.')
        return data

    def clean_grad_date(self):
        data = self.cleaned_data['grad_date']
        if not self.cleaned_data['is_high_school'] and not data:
            raise forms.ValidationError('Please enter your graduation date.')

        return data

class ApplicationSearchForm(forms.Form):
    #user related
    first_name = forms.CharField(label='first name starts with', max_length=255)
    last_name = forms.CharField(label='last Name starts with', max_length=255)
    email = forms.CharField(label='Email', max_length=255)

    #application
    school = forms.CharField(label='school name', max_length=255)
    major = forms.CharField(label='major', max_length=255)
    gender = forms.CharField(label='gender', max_length=255)
    is_minor = forms.BooleanField(label='are the applicants minor?')

    limit = forms.CharField(label='limit', max_length=255)


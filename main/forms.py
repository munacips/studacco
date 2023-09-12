from django import forms
from .models import AgentAccount, House, Room, UserAccount
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search...','class':'search'}),label='')


class AddHouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['allowed_sex','location','house_address','display_picture']


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name','sex','display_picture','number_of_beds','pricing']


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}),label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}),label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}),label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}),label='')
    agent_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Agency name'}),label='')


    class Meta:
        model = UserAccount
        fields = ['sex']
    
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields['username'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False
        self.fields['agent_name'].required = False
        self.fields['sex'].required = False

    def clean_username(self):
        username = self.cleaned_data['username']
        if '✅' in username:
            raise forms.ValidationError('Ivalid character in username')
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)


class EditHouseForm(forms.ModelForm):
    class Meta:
        model =  House
        fields = ['allowed_sex','location','house_address','display_picture']

    def __init__(self,*args,**kwargs):
        super(EditHouseForm,self).__init__(*args,**kwargs)
        self.fields['allowed_sex'].required = False
        self.fields['location'].required = False
        self.fields['house_address'].required =  False
        self.fields['display_picture'].required = False


class FeatureForm(forms.Form):
    feature = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add a feature...'}),label='')


class HousePicForm(forms.Form):
    image = forms.ImageField(label='Add house picture')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}),max_length = 164,label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label='')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}),label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}),label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}),label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),label='')



    def clean_username(self):
        username = self.cleaned_data['username']
        if '✅' in username:
            raise forms.ValidationError('Ivalid character in username')
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    
    class Meta:
        model = UserAccount
        fields = ['sex']
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AgentAccountForm(forms.Form):
    agent_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Agency name'}),label='')
    phone_number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder':'Phone number e.g. 0714125136'}),label='')

    def clean_agent_name(self):
        agent_name = self.cleaned_data['agent_name']
        if '✅' in agent_name:
            raise forms.ValidationError('Ivalid character in agent_name')
        try:
            user = AgentAccount.objects.exclude(pk=self.instance.pk).get(agent_name=agent_name)
        except User.DoesNotExist:
            return agent_name
        raise forms.ValidationError(u'Agent name "%s" is already in use.' % agent_name)


class EditRoomForm(forms.ModelForm):
    class Meta:
        model =  Room
        fields = ['room_name','sex','display_picture','number_of_beds','available_beds','available','pricing']

    def __init__(self,*args,**kwargs):
        super(EditRoomForm,self).__init__(*args,**kwargs)
        self.fields['room_name'].required = False
        self.fields['sex'].required = False
        self.fields['number_of_beds'].required =  False
        self.fields['display_picture'].required = False
        self.fields['available_beds'].required = False
        self.fields['available'].required = False
        self.fields['pricing'].required = False


class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[('1','One'),('2','Two'),('3','Three'),('4','Four'),('5','Five')],widget=forms.RadioSelect)
    comment = forms.CharField(max_length=200,widget=forms.Textarea(attrs={'rows':1,'placeholder':'Add a comment...'}),label='')
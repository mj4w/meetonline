


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm



from .models import Profile, ThreadModel, User , Post, Comment, Gender, Hobby, MessageModel, Image
class ImageForm(forms.Form):
    class Meta:
        model = Image
        fields = ['image']
class ContactForm_Report(forms.Form):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder':'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Complain Here!'}))
class ContactForm(forms.Form):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder':'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your Message'}))
# sharepost
class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'Say Something...',
        })
    )
#post 
class PostForm(forms.ModelForm):
    post = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder':'Whats on your mind?', 'class':'form-control'}))
    #fir multiple images
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['post','image']
class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={"type":"text", "class":"form-control", "placeholder":'Add your comment',}))
    class Meta:
        model = Comment
        fields= ['comment']

 
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required= True)
    class Meta: 
        model = User
        fields = ['username','email','password1','password2' ]
    def save(self, commit=True):
        user = super (NewUserForm,self).save(commit= False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class DateInput(forms.DateInput):
    input_type = "date"
# class InformationForm(ModelForm):
#     class Meta:
#         model = Information
#         fields = ('username','first_name','last_name','birthday','gender','region','favorite_color','religion','address','bio','hobby','fb_url','insta_url','twitter_url')
#         widgets  = {
#             'birthday' : DateInput(),
#         }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','type':'email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'describe yourself'}))
    school = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all()),
   
    location = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    age = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
    class Meta:
        model = User
        fields = ['username','email','name', 'last_name','bio','avatar','gender','fb_url','insta_url','twitter_url','birthday','status','location','school','age']
        widgets = {
            'birthday': DateInput(),     
    
        }

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
class ThreadForm(forms.Form):
    username = forms.CharField(label="" , max_length=100)
class MessageForm(forms.ModelForm):
    body = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={'type':'text','class':'msger-input','placeholder':'Enter your message...'}))
    image = forms.ImageField(required=False)
    class Meta:
        model = MessageModel
        fields = ['body','image']


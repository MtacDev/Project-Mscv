from django import forms

class Dateinput(forms.DateInput):
    input_type = 'date'
    
class userInfo(forms.Form):
    user = forms.CharField(required=True ,label='', max_length=100)
    password = forms.CharField(required=True ,label='',max_length=30, widget=forms.PasswordInput)

class ReporteAct(forms.Form):
    cantAgradecimiento = forms.IntegerField()
    nomAct = forms.CharField(label = '', max_length=500)
    fechaAct = forms.DateField(widget=Dateinput)
    actareu = forms.FileField(required=False,label='')
    ingrepart = forms.CharField(required= False ,widget= forms.Select
                           (attrs={'class':'remove form-control',
				                  'id':'textarea2',
                                  'multiple':'multiple',                                                        
                                  }))
    imgAct = forms.ImageField(required=False, label='')
    descact = forms.CharField(required= True, widget=forms.Textarea(attrs={'rows':7, 
                                                           'cols':20,     
                                                           'class':'form-control',
                                                           'style':'width: 49%;',                                                           
                                                           }))

class historialAct(forms.Form):
    
    fechaini = forms.DateField(widget=Dateinput)
    fechater = forms.DateField(widget=Dateinput) 

class AuthPay(forms.Form):

    auth1 = forms.ChoiceField(label='')
    auth2 = forms.ChoiceField(label='')
    
class delReporte(forms.Form):
    elmrepo = forms.IntegerField(required=False,label='', 
                                    widget=forms.HiddenInput())

from django import forms

PSYCHO_CHOICES =( 
    ("Техник", "Техник"), 
    ("Инжинер", "Инжинер"), 
    ("Нач. Лаборатории", "Нач. Лаборатории"), 
    ("Босс", "Босс"), 
)
 
class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя", initial = "введите свое имя", required = False)
    psycho_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PSYCHO_CHOICES, label="Ваша должность", initial = ("Техник", "Техник"))

class EditForm(forms.Form):
    psycho_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PSYCHO_CHOICES, label="Ваша должность", initial = ("Техник", "Техник"))

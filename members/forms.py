from django import forms


class VerifyForm(forms.Form):
    """身份验证表单"""
    name = forms.CharField(
        label='姓名',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '请输入姓名',
            'autocomplete': 'name',
        })
    )
    course = forms.CharField(
        label='课程',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '请输入课程名称',
            'autocomplete': 'off',
        })
    )

from django import forms
from .models import Student,BATCH_YEAR_REGEX, UNIVERISTY_ID_REGEX
from actor.models import User

def arn_helper(batch):
    last_student = Student.objects.all().filter(batch=batch).order_by('arn').last()
    if not last_student:
        return ((batch % 100)*1000000)+1
    else:
        last_arn_number = last_student.arn
        return last_arn_number + 1


def student_id_helper(uid):
    return int(uid[4:])


class StudentFormValidate(forms.Form):
    first_name = forms.CharField(label='first name', max_length=30)
    last_name = forms.CharField(label='last name', max_length=150)
    email = forms.EmailField(label='email address')
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, max_length=50)
    confirm_password = forms.CharField(
        label='confirm Password', widget=forms.PasswordInput, max_length=50)
    batch = forms.IntegerField(
        label="batch year", validators=[BATCH_YEAR_REGEX])
    uid = forms.CharField(label="Student ID",
                          max_length=8, validators=[UNIVERISTY_ID_REGEX])

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(StudentFormValidate, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords Do Not Match', code=400
            )

    def save(self):
        created_user = User(first_name=self.cleaned_data.get('first_name'),
                            last_name=self.cleaned_data.get('last_name'),
                            email=self.cleaned_data.get('email'),
                            username=self.cleaned_data.get('uid'))
        created_user.set_password(self.cleaned_data.get('password'))
        created_user.save()
        created_student = Student(user=created_user,
                                  uid=self.cleaned_data.get('uid'),
                                  arn=arn_helper(
                                      self.cleaned_data.get('batch')),
                                  batch=self.cleaned_data.get('batch')
                                  )
      
        # created_student = Student(user=created_user,uid=created_user.username,arn=1700006,batch=2017)
        created_student.save()
        return created_student




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['batch', 'arn', 'uid', 'degree_name_enrolled', 'degree_short_enrolled', 'department_name_enrolled', 'uni_mail', 'user']
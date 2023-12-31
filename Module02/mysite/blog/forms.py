from django import forms

# تعريف نموذج Django باسم EmailPostForm
class EmailPostForm(forms.Form):
    # حقل نص لاسم المستخدم مع تحديد الحد الأقصى للطول
    name = forms.CharField(max_length=25)

    # حقل بريد إلكتروني لعنوان البريد الإلكتروني الخاص بالمستخدم
    email = forms.EmailField()

    # حقل بريد إلكتروني لعنوان البريد الإلكتروني الخاص بالمستلم
    to = forms.EmailField()

    # حقل نص طويل يسمح للمستخدم بإدخال تعليقاته
    comments = forms.CharField(required=False, widget=forms.Textarea)

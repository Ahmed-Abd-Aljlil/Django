from django.shortcuts import render,  get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

#from .models import get_absolute_url
# def post_list(request):
#     # استعراض كافة المشاركات الموجودة في نموذج Post
#     post_list = Post.objects.all()

#     # إنشاء كائن Paginator وتحديد عدد المشاركات في كل صفحة (في هذه الحالة 3)
#     paginator = Paginator(post_list, 3)

#     # الحصول على رقم الصفحة المطلوب من الطلب الوارد (إذا لم يتم تحديده، فستكون الصفحة الأولى)
#     page_number = request.GET.get('page', 1)

#     try:
#         # محاولة استرداد الصفحة المطلوبة
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # إذا كان رقم الصفحة ليس عددًا صحيحًا، استخدام الصفحة الأولى كبديل
#         posts = paginator.page(1) 
#     except EmptyPage:
#         # إذا كان رقم الصفحة خارج نطاق الصفحات المتاحة، استخدام آخر صفحة متاحة كبديل
#         posts = paginator.page(paginator.num_pages)

#     # تقديم النتائج إلى القالب وإرجاعها كاستجابة
#     return render(request, 'blog/post/list.html', {'posts': posts})

class PostListView(ListView):
    """"
    alternative post list view
    """
    model = Post
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    # الحصول على المشاركة المحددة بناءً على السنة والشهر واليوم واسم المشاركة (slug)
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # تقديم المشاركة المحددة إلى القالب وإرجاعها كاستجابة
    return render(request, 'blog/post/detail.html', {'post': post})
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm  # استيراد نموذج البريد

def post_share(request, post_id):
    # الحصول على المشاركة بناءً على الهوية مع التحقق من الحالة
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    # تم تحديد sent على False في البداية لإشارة إلى عدم إرسال البريد الإلكتروني بعد
    sent = False

    # معالجة الطلبات الواردة
    if request.method == 'POST':
        # معالجة النموذج إذا كان الطلب POST
        form = EmailPostForm(request.POST)

        # التحقق من صحة النموذج
        if form.is_valid():  
            # استخراج البيانات النظيفة من النموذج
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            # إعداد البريد الإلكتروني
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n {cd['name']} \n comments: {cd['comments']}"

            # إرسال البريد الإلكتروني باستخدام وظيفة send_mail
            send_mail(subject, message, 'abd79363@gmail.com', [cd['to']])
            
            # تعيين sent إلى True بمجرد إرسال البريد بنجاح
            sent = True   

    else:
        # إنشاء نموذج فارغ إذا كان الطلب GET
        form = EmailPostForm()

    # عرض الصفحة مع المشاركة ونموذج البريد وحالة الإرسال
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

    
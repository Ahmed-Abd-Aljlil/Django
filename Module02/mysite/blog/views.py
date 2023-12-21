from django.shortcuts import render,  get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    # استعراض كافة المشاركات الموجودة في نموذج Post
    post_list = Post.objects.all()

    # إنشاء كائن Paginator وتحديد عدد المشاركات في كل صفحة (في هذه الحالة 3)
    paginator = Paginator(post_list, 3)

    # الحصول على رقم الصفحة المطلوب من الطلب الوارد (إذا لم يتم تحديده، فستكون الصفحة الأولى)
    page_number = request.GET.get('page', 1)

    try:
        # محاولة استرداد الصفحة المطلوبة
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # إذا كان رقم الصفحة ليس عددًا صحيحًا، استخدام الصفحة الأولى كبديل
        posts = paginator.page(1) 
    except EmptyPage:
        # إذا كان رقم الصفحة خارج نطاق الصفحات المتاحة، استخدام آخر صفحة متاحة كبديل
        posts = paginator.page(paginator.num_pages)

    # تقديم النتائج إلى القالب وإرجاعها كاستجابة
    return render(request, 'blog/post/list.html', {'posts': posts})



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


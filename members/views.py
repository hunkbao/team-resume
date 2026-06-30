from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Profile
from .forms import VerifyForm


def verify(request):
    """验证页面 — 输入姓名和课程进行身份验证"""
    error = None
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            course = form.cleaned_data['course']
            try:
                profile = Profile.objects.get(name=name, verify_course=course)
                request.session['verified_profile_id'] = profile.id
                return redirect('members:profile', pk=profile.pk)
            except Profile.DoesNotExist:
                error = '姓名或课程不正确，请重新输入'
    else:
        form = VerifyForm()

    return render(request, 'members/verify.html', {
        'form': form,
        'error': error,
    })


def profile(request, pk):
    """个人简历展示页面"""
    profile_obj = get_object_or_404(Profile, pk=pk)

    # 检查是否通过验证
    verified_id = request.session.get('verified_profile_id')
    if verified_id != profile_obj.id:
        return redirect('members:verify')

    courses = profile_obj.courses.all()
    websites = profile_obj.websites.all()

    return render(request, 'members/profile.html', {
        'profile': profile_obj,
        'courses': courses,
        'websites': websites,
    })


def logout(request):
    """退出登录，清除 session"""
    request.session.flush()
    return redirect('members:verify')

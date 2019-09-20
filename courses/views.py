from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,View
from courses.models import Course,Lesson,Category
from memberships.models import UserMembership
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class CourseListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/course_list.html'
    model = Course


class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Course

#
class LessonDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_membership_type = course.allowed_memberships.all()
        print(course_allowed_membership_type.filter(membership_type=user_membership_type))
        context = { 'lesson': None }
        if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
            context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)


# def get(self,request,course_slug,lesson_slug,*args,**kwargs):
#
#     course_qs = Course.objects.filter(slug=course_slug)
#     if course_qs.exists():
#         course = course_qs.first()
#     lesson_qs = course.lessons.filter(slug=lesson_slug)
#     if lesson_qs.exists():
#         lesson = lesson_qs.first()
#     user_membership = UserMembership.objects.filter(user=request.user).first()
#     user_membership_type = user_membership.membership.membership_type
#
#     course_allowed_membership_type = course.allowed_memberships.all()
#     context = {'lessons':None}
#
#     if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
#         context = {'lesson':lesson}
#
#     return render(request,'courses/lesson_detail.html',context)

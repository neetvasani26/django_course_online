# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .model import Course, Lesson, Submission, Question, Student

def home(request):
    return HttpResponse("Home Page")

# def course_details_bootstrap(request):
#     return HttpResponse("course_details_bootstrap Page")

def course_details_bootstraps(request, id):
    course = Course.objects.get(id=id)
    lessons = Lesson.objects.filter(course=course)

    return render(request, 'course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons
    })

def submit(request, course_id):
    student = Student.objects.first()

    if request.method == 'POST':
        Submission.objects.filter(student=student).delete()

        last_submission = None

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                choice_id = value

                last_submission = Submission.objects.create(
                    student=student,
                    question_id=question_id,
                    selected_choice_id=choice_id
                )

        return redirect('show_result', course_id=course_id, submission_id=last_submission.id)

    questions = Question.objects.filter(course_id=course_id)
    return render(request, 'exam.html', {'questions': questions})

# Show Result
def show_exam_result(request, course_id, submission_id):
    student = Student.objects.first()

    submissions = Submission.objects.filter(student=student)

    score = 0
    total = submissions.count()

    for sub in submissions:
        if sub.selected_choice.is_correct:
            score += 1

    return render(request, 'result.html', {
        'score': score,
        'total': total
    })
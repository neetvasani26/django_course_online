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

    if not student:
        return HttpResponse("No student found. Add student in admin.")

    if request.method == 'POST':
        Submission.objects.filter(student=student).delete()

        last_submission = None

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                choice_id = value

                # create submission
                submission = Submission.objects.create(
                    student=student,
                    question_id=question_id
                )

                # add selected choice (ManyToMany)
                submission.choices.add(choice_id)

                last_submission = submission

        return redirect('show_exam_result', course_id=course_id, submission_id=last_submission.id)

    questions = Question.objects.filter(lesson__course_id=course_id)  # ✅ FIXED
    return render(request, 'exam.html', {'questions': questions})

# Show Result
def show_exam_result(request, course_id, submission_id):
    student = Student.objects.first()
    course = Course.objects.get(id=course_id)

    questions = Question.objects.filter(lesson__course=course)
    submissions = Submission.objects.filter(student=student)

    total_score = 0
    possible_score = questions.count()

    selected_ids = []

    for question in questions:
        selected_choices = []

        for sub in submissions:
            if sub.question.id == question.id:
                selected_choices = list(sub.choices.values_list('id', flat=True))
                selected_ids.extend(selected_choices)

        # ✅ use required method
        if question.is_get_score(selected_choices):
            total_score += 1

    # simple grade logic
    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0

    return render(request, 'exam_result_bootstrap.html', {
        'course': course,              # ✅ REQUIRED
        'selected_ids': selected_ids,  # ✅ REQUIRED
        'grade': grade,                # ✅ REQUIRED
        'possible': possible_score     # ✅ REQUIRED
    })
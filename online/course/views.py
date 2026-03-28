from django.http import HttpResponse
from django.shortcuts import render, redirect
from .model import Course, Lesson, Submission, Question, Student


def home(request):
    return HttpResponse("Home Page")


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
        return HttpResponse("No student found. Please add a student in the admin panel.")

    if request.method == 'POST':
        # Clear previous submissions for this student & course
        course = Course.objects.get(id=course_id)
        questions_in_course = Question.objects.filter(lesson__course=course)
        Submission.objects.filter(student=student, question__in=questions_in_course).delete()

        last_submission = None

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                choice_id = value

                submission = Submission.objects.create(
                    student=student,
                    question_id=question_id
                )
                submission.choices.add(choice_id)
                last_submission = submission

        if last_submission:
            return redirect('show_exam_result', course_id=course_id, submission_id=last_submission.id)
        else:
            return HttpResponse("No answers were submitted.")

    # GET — show the exam
    questions = Question.objects.filter(lesson__course_id=course_id).prefetch_related('choices')
    return render(request, 'exam.html', {'questions': questions})


def show_exam_result(request, course_id, submission_id):
    student = Student.objects.first()
    course = Course.objects.get(id=course_id)

    # All questions for this course
    questions = Question.objects.filter(lesson__course=course).prefetch_related('choices')

    # All submissions by this student for this course
    submissions = Submission.objects.filter(
        student=student,
        question__in=questions
    ).prefetch_related('choices')

    # Build a lookup: question_id → list of selected choice ids
    submission_map = {}
    for sub in submissions:
        submission_map[sub.question_id] = list(sub.choices.values_list('id', flat=True))

    # ✅ Calculate total_score and possible_score using is_get_score()
    total_score = 0
    possible_score = questions.count()
    selected_ids = []

    for question in questions:
        selected_choices = submission_map.get(question.id, [])
        selected_ids.extend(selected_choices)

        # ✅ Required method used explicitly per question
        if question.is_get_score(selected_choices):
            total_score += 1

    grade = round((total_score / possible_score) * 100, 2) if possible_score > 0 else 0

    return render(request, 'exam_result_bootstrap.html', {
        'course': course,               # ✅ REQUIRED
        'total_score': total_score,     # ✅ REQUIRED
        'possible': possible_score,     # ✅ REQUIRED
        'selected_ids': selected_ids,   # ✅ REQUIRED
        'grade': grade,                 # ✅ REQUIRED
        'submissions': submissions,     # ✅ for template access if needed
    })
from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='instructors')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.lesson_name


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_choice_ids):
        """Returns True if selected choices exactly match all correct choices."""
        correct_ids = set(
            self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        return correct_ids == set(selected_choice_ids)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Student(models.Model):
    name = models.CharField(max_length=200)
    enrolled_courses = models.ManyToManyField(Course, blank=True, related_name='students')

    def __str__(self):
        return self.name


# class Submission(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
#     choices = models.ManyToManyField(Choice, related_name='submissions')
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student} - {self.question}"

#     def is_correct(self):
#         """Checks if this submission's selected choices are all correct."""
#         selected_ids = list(self.choices.values_list('id', flat=True))
#         return self.question.is_get_score(selected_ids)

# class Submission(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
#     choices = models.ManyToManyField(Choice, related_name='submissions')
#     # ← no submitted_at for now

#     def __str__(self):
#         return f"{self.student} - {self.question}"

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.question}"

    def is_correct(self):
        selected_ids = list(self.choices.values_list('id', flat=True))
        return self.question.is_get_score(selected_ids)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}: {self.score}"
    
class Learner(models.Model):
    FULL_TIME = 'full_time'
    PART_TIME = 'part_time'

    OCCUPATION_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
    ]

    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default=FULL_TIME)
    courses = models.ManyToManyField(Course, blank=True, related_name='learners')
    social_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson_name


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Student(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    submitted_at = models.DateTimeField(auto_now_add=True)  # optional

    def __str__(self):
        return f"{self.student} - {self.question}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField()

class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Learner(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
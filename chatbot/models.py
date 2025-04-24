from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    answer_text = models.TextField()
    related_question_1 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='related_1', blank=True)
    related_question_2 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='related_2', blank=True)
    related_question_3 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='related_3', blank=True)

    def __str__(self):
        return self.question_text

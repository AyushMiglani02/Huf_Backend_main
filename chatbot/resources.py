from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Question

class QuestionResource(resources.ModelResource):
    related_question_1 = Field(
        column_name='related_question_1',
        attribute='related_question_1',
        widget=ForeignKeyWidget(Question, 'question_text')
    )
    related_question_2 = Field(
        column_name='related_question_2',
        attribute='related_question_2',
        widget=ForeignKeyWidget(Question, 'question_text')
    )
    related_question_3 = Field(
        column_name='related_question_3',
        attribute='related_question_3',
        widget=ForeignKeyWidget(Question, 'question_text')
    )

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'answer_text', 'related_question_1', 'related_question_2', 'related_question_3')


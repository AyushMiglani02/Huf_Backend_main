# chatbot/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Question

def question_detail(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

    question = get_object_or_404(Question, pk=pk)
    response_data = {
        'id': question.id,
        'question': question.question_text,
        'answer': question.answer_text,
        'related_questions': {
            'related_question_1': {
                'id': question.related_question_1.id if question.related_question_1 else None,
                'text': question.related_question_1.question_text if question.related_question_1 else None,
            },
            'related_question_2': {
                'id': question.related_question_2.id if question.related_question_2 else None,
                'text': question.related_question_2.question_text if question.related_question_2 else None,
            },
            'related_question_3': {
                'id': question.related_question_3.id if question.related_question_3 else None,
                'text': question.related_question_3.question_text if question.related_question_3 else None,
            },
        }
    }
    return JsonResponse(response_data)



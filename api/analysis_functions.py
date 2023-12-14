import json
from controllers.models import *
from django.db.models import Count, F
from .serializers_analysis import *

def calculate_percentage(count, total):
    return (count / total) * 100 if total > 0 else 0

def analyze_survey(survey_id):
    survey = Survey.objects.get(id=survey_id)
    
    
    analysis_schema = survey.analysis_json
    
    
    basic_analysis = analysis_schema.get('basic', []) # type: ignore
    
    print('basic_analysis')
    print(basic_analysis)

    analysis_results = []

    for question_json_data in basic_analysis:
        order = question_json_data.get('order',None)
        print(f'oder {order}, survey {survey.id}') # type: ignore
        question_obj = FormInput.objects.get(survey = survey, order = order)
        
        print(question_obj.id) # type: ignore
        
        
        possible_answers = FormInputChoice.objects.filter(
            input=question_obj
        )     
        
        total_responses = SurveyParticipantAnswer.objects.filter(choice__input=question_obj).count()
        
        answer_results = []
        
        for answer in possible_answers:            
            answer_count = SurveyParticipantAnswer.objects.filter(choice=answer).count()
            
            result = None
            
            if question_json_data['display'] == 'count':
                result = answer_count
            elif question_json_data['display'] == 'percentage':
                result = calculate_percentage(answer_count, total_responses)
                
            question_analysis = {
                'answer': answer.text,
                'order': answer.order,
                'result': result,
                'display': question_json_data['display'],
                'type': question_json_data['type']
            }
            print('tutaj')
            
            print(question_analysis)
            answer_results.append(question_analysis)
            
        question_data = {
            'question': FormInputSerializerToJson(question_obj).data, # type: ignore
            'answers': answer_results
        }
        
        analysis_results.append(question_data)
        print('tutaj2')
        print(question_data)


    # Update the survey instance
    print(analysis_results)
    survey.analysis_result_json = analysis_results # type: ignore
    survey.save()
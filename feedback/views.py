from django.shortcuts import render
from .models import feedback_table
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from datetime import datetime
import time
logger = logging.getLogger('file_log')

@csrf_exempt
def add_feeback(request):
    start_time = time.time()
    logger.info("\nrequest to feedback")
    logger.info(f"Time: {datetime.now()}")
    if request.method!='POST':
        logger.info("request is not POST")
        return JsonResponse(data={"message": "only POST method allowed"}, status=405)
    try:
        # decode data
        data = json.loads(request.body.decode('utf-8'))
        logger.info("decoded data")

        # create feedback object
        feedback_obj = feedback_table(
            rating = int(data.get('rating')),
            feedback = str(data.get('feedback'))
        )
        logger.info("created feedback object")

        # validate rating
        if feedback_obj.rating>5 or feedback_obj.rating<1:
            logger.error("invalid rating")
            return JsonResponse(data={"message": "invalid rating"}, status=400)
        
        feedback_obj.save()
        logger.info("feedback saved")
        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data={"message":"feedback submitted successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while submitting request"}, status=500)

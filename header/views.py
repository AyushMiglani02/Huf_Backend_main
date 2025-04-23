from django.http import JsonResponse
from disease.models import disease_table
import logging
import time
from datetime import datetime
logger = logging.getLogger('file_log')

def header(request):
    start_time = time.time()
    logger.info("\nrequest to header")
    logger.info(f"Time: {datetime.now()}")
    try:
        # data to be sent to user
        final_data = {}

        # get all disease where show=True
        all_disease_obj = disease_table.objects.filter(show=True)
        logger.info("fetched all disease")

        # fetch list of names of all disease
        disease_list = []
        for disease in all_disease_obj:
            disease_list.append(disease.name)
        logger.info("created list")
        
        final_data.update({"diseaseList": disease_list})
        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data=final_data, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while getting data"}, status=500)
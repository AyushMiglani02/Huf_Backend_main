from django.shortcuts import render
from django.views import View
from .models import pathy_table, effective_table
from django.http import JsonResponse
import logging
import time
from datetime import datetime
logger = logging.getLogger('file_log')

class PathyView(View):
    def get(self, request):
        start_time = time.time()
        logger.info("\nrequest to pathy view")
        logger.info(f"Time: {datetime.now()}")
        try:   
            # final data to be sent to user
            final_data = {}

            # getting all pathy data
            pathy_list = []
            for pathy in pathy_table.objects.filter(show=True):
                disease_list = []

                # getting effective for data for each pathy
                for disease in effective_table.objects.filter(pathy__pk=pathy.pk, show=True):
                    disease_list.append({
                        "disease": disease.name,
                        "link": disease.link
                    })
                logger.info(f"fetched effective for data for {pathy.title}")
                pathy_list.append({
                    "imageLink": pathy.image.url,
                    "title": pathy.title,
                    "text": pathy.text,
                    "diseaseList": disease_list
                })
            final_data.update({"pathyList": pathy_list})
            logger.info("fetched all pathy data")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting pathy data"}, status=500)

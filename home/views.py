from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import key_value_table, testimonial_table, video_table
from disease.models import disease_table
import logging
import time
from datetime import datetime
logger = logging.getLogger('file_log')

class HomeView(View):
    def get(self, request):
        start_time = time.time()
        logger.info("\nrequest to home")
        logger.info(f"Time: {datetime.now()}")
        try:
            # this will be sent to user
            final_data = {}

            # # getting data for topSearchPage
            diseases = disease_table.objects.filter(show=True)
            diseaseList = []
            for disease in diseases:
                diseaseList.append(disease.name)
            final_data.update({"topSearchPage": {"diseaseList": diseaseList}})
            logger.info("all diseases fetched")

            # getting data for ourMissionPage
            final_data.update({"ourMissionPage": {
                "youtubeLink": key_value_table.objects.get(key='our_mission_ytlink').value,
                "ourMissionText": key_value_table.objects.get(key='our_mission_data').value,
            }})
            logger.info("our mission fetched")

            # getting data for testimonialPage
            testimonial_list = []
            for testimonial in testimonial_table.objects.filter(show=True):
                testimonial_list.append({
                    "heading": testimonial.heading,
                    "text": testimonial.text,
                    "name": testimonial.name,
                    "location": testimonial.location
                })
            final_data.update({"testimonialPage": {"testimonialList": testimonial_list}})
            logger.info("all testimonial fetched")

            # getting data for videoPage
            # video_list = []
            # for video in video_table.objects.filter(show=True):
            #     video_list.append({
            #         "image": video.image.url,
            #         "heading": video.heading,
            #         "ytplaylist_link": video.ytplaylist_link
            #     })
            # final_data.update({"videoPage": {
            #     "text": key_value_table.objects.get(key="video_section_text").value,
            #     "videoList": video_list 
            # }})
            # logger.info("all videos fetched")

            # getting data for bottomSearchPage
            final_data.update({"bottomSearchPage": {"text": key_value_table.objects.get(key="second_search_text").value}})
            logger.info("bottom search data fetched")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=404)
        
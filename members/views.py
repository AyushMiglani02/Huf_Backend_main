from .models import members_table, key_value_table
from django.http import JsonResponse
import logging
from datetime import datetime
import time
logger = logging.getLogger('file_log')

def get_members(request):
    start_time = time.time()
    logger.info("\nrequest to members")
    logger.info(f"Time: {datetime.now()}")
    try:
        # final data to be sent to user
        final_data = {}
        final_data.update({"text": key_value_table.objects.get(key="members_text").value})
        logger.info("fetched text for members")

        final_data.update({"teamList": []})

        team_set = set()
        for member in members_table.objects.filter(show=True):
            team_set.add(member.team)
        
        for team in team_set:
            final_data['teamList'].append(team)
        logger.info("fetched teams for members")

        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data=final_data, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while getting data"}, status=500)

def get_members_detail(request, team):
    start_time = time.time()
    logger.info("\nrequest to members detail")
    logger.info(f"Time: {datetime.now()}")
    try:
        # final data to be sent to user
        final_data = {}

        member_list = []
        for member in members_table.objects.filter(team=team, show=True):
            temp_member = {
                "name": member.name,
                "designation": member.designation,
                "imageLink": member.image.url,
                "about": member.about,
            }

            if member.linkedin_url:
                temp_member.update({"linkedinLink": member.linkedin_url})
            
            if member.email_address:
                temp_member.update({"emailAddress": member.email_address})
            
            if member.phone_number:
                temp_member.update({"phoneNumber": member.phone_number})

            member_list.append(temp_member)
        final_data.update({"memberList": member_list})

        logger.info("fetched members of team")
        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data=final_data, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while getting data"}, status=500)

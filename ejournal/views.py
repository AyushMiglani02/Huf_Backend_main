from django.views import View
from .models import key_value_table, ejournal_table, subscription_table
from django.http import JsonResponse
import logging
import re
from datetime import datetime
import time
logger = logging.getLogger('file_log')

class EjournalView(View):
    def get(self, request):
        start_time = time.time()
        logger.info("\nrequest to ejournal view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # final data to send to user
            final_data = {}

            # getting the top 3 ejournal and text
            ejournals = []
            for ejournal in ejournal_table.objects.filter(show=True, publish_date__lt=datetime.now()).order_by("-publish_date")[:3]:
                ejournals.append({
                    "imageLink": ejournal.image.url,
                    "fileLink": ejournal.file.url
                })
            logger.info("fetched top 3 ejournal data")
            
            final_data.update({
                "latestEjournalPage": {
                    "text": key_value_table.objects.get(key='ejournal_page_text').value,
                    "ejournals": ejournals
                }
            })
            logger.info("fetched data for latestEjournalPage")


            final_data.update({"allEjournalPage": {"text": key_value_table.objects.get(key='all_ejournal_page_text').value}})
            logger.info("fetched data for allEjournalPage")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)


class GetAllEjournal(View):
    def get(self, request):
        start_time = time.time()
        logger.info("\nrequest to get all journal view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # data to be sent to user
            final_data = {}

            # get year from request's query parameter
            year = int(request.GET.get('year'))
            logger.info("fetched year")

            ejournals = []
            for ejournal in ejournal_table.objects.filter(show=True, publish_date__year=year, publish_date__lt=datetime.now()):
                ejournals.append({
                    "name": ejournal.name,
                    "imageLink": ejournal.image.url,
                    "fileLink": ejournal.file.url
                })
            final_data.update({"ejournals": ejournals})
            logger.info("fetched all ejournals")
            logger.info(f"Time: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)
        
def is_valid_email(email):
    # Define a regular expression pattern for a basic email format check
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use re.match to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False

def subscribe(request):
    start_time = time.time()
    logger.info("\nrequest to subscribe")
    logger.info(f"Time: {datetime.now()}")
    try:
        # check if email already in database
        email = str(request.GET.get('email'))
        logger.info("fetched email")
        # create new user if not exist else set send=True
        if not subscription_table.objects.filter(email_address=email).exists():
            if not is_valid_email(email):
                return JsonResponse(data={"message": "invalid email address"}, status=400)
            subscriber = subscription_table(
                email_address = email,
                send = True
            )
            subscriber.save()
            logger.info("creating new subscriber")
        else:
            subscriber = subscription_table.objects.get(email_address=email)
            subscriber.send = True
            subscriber.save()
            logger.info("subscriber already exists")
        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data={"message": "subscribed successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while subscribing"}, status=500)

def unsubscribe(request):
    start_time = time.time()
    logger.info("\nrequest to unsubscribe")
    logger.info(f"Time: {datetime.now()}")
    try:
        # check if email already in database
        email = str(request.GET.get('email'))
        logger.info("email subscriber")
        # set send=False if user exist else return failed message
        if subscription_table.objects.filter(email_address=email).exists():
            subscriber = subscription_table.objects.get(email_address=email)
            subscriber.send = False
            subscriber.save()
            logger.info("subscriber unsubscribed")
        else:
            logger.error("subscriber do not exist")
            return JsonResponse(data={"message": "user not found"}, status=404)
        logger.info(f"Time taken: {time.time()-start_time}")
        return JsonResponse(data={"message": "unsubscribed successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while subscribing"}, status=500)
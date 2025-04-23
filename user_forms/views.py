from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import join_us_table, share_experience_table, ask_suggestion_table
from datetime import datetime, timedelta
import time
import logging
logger = logging.getLogger('file_log')


# Join us OTP
# def send_otp_email(email, otp):
#     logger.info("OTP sent to email successfully")
#     pass


# def recreate_and_send_join_us_otp(email):
#     logger.info("generating OTP")
#     try:
#         if join_us_otp_table.objects.filter(email_address=email).exists():
#             otp_obj = join_us_otp_table.objects.get(email_address = email)
#             otp_obj.otp = str(000000)
#             otp_obj.save()
#             send_otp_email(otp_obj.email_address, otp_obj.otp)
#         logger.info("OTP regenerated successfully")
#     except Exception as e:
#         logger.error("error while creating otp")
#         logger.error(e)


# def resend_join_us_otp(request):
#     start_time = time.time()
#     logger.info("\nrequest to resend join us otp")
#     logger.info(f"Time: {datetime.now()}")

#     if request.method != 'GET':
#         return JsonResponse(data={"message": f"method {request.method} does not exist"}, status=405)
#     try:
#         email = request.GET.get('email')
#         recreate_and_send_join_us_otp(email)
#         logger.info(f"Time taken: {time.time()-start_time}")
#         return JsonResponse(data={"message": "OTP resent successfully!"}, status=200)
#     except Exception as e:
#         logger.error(e)
#         return JsonResponse(data={"message": "error while resending OTP"}, status=500)

@csrf_exempt
def join_us(request):
    start_time = time.time()
    logger.info("\nrequest to join us")
    logger.info(f"Time: {datetime.now()}")

    # verify request method
    if request.method != 'POST':
        logger.error("invalid request method")
        return JsonResponse(data={"message": f"method {request.method} does not exist"}, status=405)

    try:
        if request.FILES['photograph'] is None:
            return JsonResponse(data={"message": "photograph missing"}, status=400)
        
        if request.FILES['document'] is None:
            return JsonResponse(data={"message": "document missing"}, status=400)
        
        photograph_obj = request.FILES['photograph']
        document_obj = request.FILES['document']

        if not (photograph_obj.name.lower().endswith('.jpg') or photograph_obj.name.lower().endswith('.jpeg') or photograph_obj.name.lower().endswith('.png')):
            return JsonResponse(data={"message": "invalid photograph format"}, status=400)
        
        if not document_obj.name.lower().endswith('.pdf'):
            return JsonResponse(data={"message": "invalid document format"}, status=400)
        
        if int(request.POST['age'])<0 or int(request.POST['age'])>200:
            return JsonResponse(data={"message": "invalid age"}, status=400)
        
        join_us_obj = join_us_table(
            name = request.POST['name'],
            age = request.POST['age'],
            gender = request.POST['gender'],
            email_address = request.POST['email_address'],
            phone_number = request.POST['phone_number'],
            address = request.POST['address'],
            pincode = request.POST['pincode'],
            city = request.POST['city'],
            state = request.POST['state'],
            country = request.POST['country'],
            profession = request.POST['profession'],
            message = request.POST['message'],
            photograph = photograph_obj,
            document = document_obj
        )
        join_us_obj.save()
        logger.info("information saved successfully")
        logger.info(f"time taken: {time.time()-start_time}")
        # OTP code
        # generated_otp = str(000000)
        # join_us_otp_obj = join_us_otp_table(
        #     join_us = join_us_obj,
        #     email_address = request.POST['email_address'],
        #     otp = generated_otp
        # )
        # join_us_otp_obj.save()
        # send_otp_email(request.POST['email_address'], generated_otp)
        return JsonResponse(data={"message": "information saved successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while saving information"}, status=500)

# join us OTP
# def join_us_otp_verify(request):
#     start_time = time.time()
#     logger.info("\nrequest to join us otp verify")
#     logger.info(f"Time: {datetime.now()}")

#     if request.method != 'GET':
#         return JsonResponse(data={"message": f"method {request.method} does not exist"}, status=405)

@csrf_exempt
def share_experience(request):
    start_time = time.time()
    logger.info("\nrequest to share experience")
    logger.info(f"Time: {datetime.now()}")

    # verify request method
    if request.method != 'POST':
        logger.error("invalid request method")
        return JsonResponse(data={"message": f"method {request.method} does not exist"}, status=405)
    
    try:
        if int(request.POST['age'])<0 or int(request.POST['age'])>200:
            return JsonResponse(data={"message": "invalid age"}, status=400)

        share_experience_obj = share_experience_table(
            name = request.POST["name"],
            age = request.POST["age"],
            gender = request.POST["gender"],
            city = request.POST["city"],
            state = request.POST["state"],
            country = request.POST["country"],
            email_address = request.POST["email_address"],
            experience = request.POST["experience"],
        )
        logger.info("object created")
        logger.info("checking optional information")
        if request.POST.get("phone_number") is not None:
            share_experience_obj.phone_number = request.POST["phone_number"]

        if request.POST.get("disease") is not None:
            share_experience_obj.disease = request.POST["disease"]

        if request.POST.get("pathies") is not None:
            share_experience_obj.pathies = request.POST["pathies"]

        if request.POST.get("date_from") is not None:
            share_experience_obj.date_from = request.POST["date_from"]

        if request.POST.get("date_to") is not None:
            share_experience_obj.date_to = request.POST["date_to"]

        if request.POST.get("show_name") is not None:
            share_experience_obj.show_name = True if request.POST["show_name"]=="true" else False

        if request.POST.get("preferred_communication") is not None:
            share_experience_obj.preferred_communication = request.POST["preferred_communication"]

        if request.FILES.get("reports") is not None:
            reports_obj = request.FILES["reports"]
            if not reports_obj.name.lower().endswith('.pdf'):
                return JsonResponse(data={"message": "invalid document format"}, status=400)
            share_experience_obj.reports = reports_obj
        
        share_experience_obj.save()
        logger.info("information saved")
        logger.info(f"time taken: {time.time()-start_time}")
        return JsonResponse(data={"message": "information saved successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while saving information"}, status=500)

@csrf_exempt
def ask_suggestion(request):
    start_time = time.time()
    logger.info("\nrequest to ask suggestion")
    logger.info(f"Time: {datetime.now()}")

    # verify request method
    if request.method != 'POST':
        logger.error("invalid request method")
        return JsonResponse(data={"message": f"method {request.method} does not exist"}, status=405)
    
    try:
        if int(request.POST['age'])<0 or int(request.POST['age'])>200:
            return JsonResponse(data={"message": "invalid age"}, status=400)

        ask_suggestion_obj = ask_suggestion_table(
            name = request.POST["name"],
            age = request.POST["age"],
            gender = request.POST["gender"],
            city = request.POST["city"],
            state = request.POST["state"],
            country = request.POST["country"],
            email_address = request.POST["email_address"],
            query = request.POST["query"],
        )
        logger.info("object created")
        logger.info("checking optional information")
        if request.POST.get("phone_number") is not None:
            ask_suggestion_obj.phone_number = request.POST["phone_number"]

        if request.POST.get("disease") is not None:
            ask_suggestion_obj.disease = request.POST["disease"]

        if request.POST.get("pathies") is not None:
            ask_suggestion_obj.pathies = request.POST["pathies"]

        if request.POST.get("show_email") is not None:
            ask_suggestion_obj.show_email = True if request.POST["show_email"]=="true" else False
        
        if request.POST.get("show_study") is not None:
            ask_suggestion_obj.show_study = True if request.POST["show_study"]=="true" else False

        if request.FILES.get("reports") is not None:
            reports_obj = request.FILES["reports"]
            if not reports_obj.name.lower().endswith('.pdf'):
                return JsonResponse(data={"message": "invalid document format"}, status=400)
            ask_suggestion_obj.reports = reports_obj
        
        ask_suggestion_obj.save()
        logger.info("information saved")
        logger.info(f"time taken: {time.time()-start_time}")
        return JsonResponse(data={"message": "information saved successfully"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "error while saving information"}, status=500)

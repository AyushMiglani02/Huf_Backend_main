from django.views import View
from .models import disease_table, pathy_table, summary_table, book_table, source_table, data_table, whatsapp_table, case_table
from django.http import JsonResponse
from django.db import models
import logging
import time
from datetime import datetime
from analytics.models import disease_analytics_table, pathy_analytics_table
from django.utils import timezone
logger = logging.getLogger('file_log')
DIRECT_CASE = 'directCase'

def update_disease_analytics(disease_object):
    disease_analytics_obj, created = disease_analytics_table.objects.get_or_create(disease=disease_object, date=timezone.now().date())
    disease_analytics_obj.count += 1
    disease_analytics_obj.save()

def update_pathy_analytics(pathy_object):
    pathy_analytics_obj, created = pathy_analytics_table.objects.get_or_create(pathy=pathy_object, date=timezone.now().date())
    pathy_analytics_obj.count += 1
    pathy_analytics_obj.save()

class DiseaseView(View):
    def get(self, request, disease):
        start_time = time.time()
        logger.info("\nrequest to disease view")
        logger.info(f"Time: {datetime.now()}")
        try:
            disease_object = disease_table.objects.get(name=disease)

            # this will be sent to user
            final_data = {}

            # return 404 if data not present or not allowed
            if (disease_object is None) or (disease_object.show is False):
                return JsonResponse(data=final_data, status=404)
            
            # update the count in analytics table
            update_disease_analytics(disease_object=disease_object)
            
            final_data.update({'disease': disease})
            final_data.update({'text': disease_object.text})
            final_data.update({'summary': disease_object.summary})
            final_data.update({'imageLink': disease_object.image_link.url})
            logger.info("disease, text, summary and imagelink fetched")

            # to store different pathies
            all_pathies = {}

            # getting data of different types of therapies
            therapiesWithDrugs = []
            for pathy in pathy_table.objects.filter(disease__name=disease, type="therapiesWithDrugs"):
                summary = summary_table.objects.get(pathy__pk=pathy.pk)
                therapiesWithDrugs.append({
                    "name": pathy.name,
                    "imageLink": pathy.image_link.url,
                    "summary": summary.summary
                })
            all_pathies.update({"therapiesWithDrugs": therapiesWithDrugs})
            logger.info("therapies with drugs fetched")

            therapiesWithoutDrugs = []
            for pathy in pathy_table.objects.filter(disease__name=disease, type="therapiesWithoutDrugs"):
                summary = summary_table.objects.get(pathy__pk=pathy.pk)
                therapiesWithoutDrugs.append({
                    "name": pathy.name,
                    "imageLink": pathy.image_link.url,
                    "summary": summary.summary
                })
            all_pathies.update({"therapiesWithoutDrugs": therapiesWithoutDrugs})
            logger.info("therapies without drugs fetched")

            lessKnownTherapies = []
            for pathy in pathy_table.objects.filter(disease__name=disease, type="lessKnownTherapies"):
                summary = summary_table.objects.get(pathy__pk=pathy.pk)
                lessKnownTherapies.append({
                    "name": pathy.name,
                    "imageLink": pathy.image_link.url,
                    "summary": summary.summary
                })
            all_pathies.update({"lessKnownTherapies": lessKnownTherapies})
            logger.info("less known therapies fetched")

            final_data.update({"pathies": all_pathies})
            logger.info("all therapies data fetched")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)


class TherapyView(View):
    def get(self, request, disease, pathy):
        start_time = time.time()
        logger.info("\nrequest to therapy view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # check whether show=True for disease
            disease_object = disease_table.objects.get(name=disease)
            if disease_object.show is False:
                return JsonResponse(data={"message": "No data for this disease"}, status=404)
            
            # check whether show=True for pathy
            pathy_object = pathy_table.objects.get(disease__name=disease, name=pathy)
            if pathy_object.show is False:
                return JsonResponse(data={"message": "No data for this Pathy"}, status=404)
            
            # update the count in analytics table
            update_disease_analytics(disease_object=disease_object)
            update_pathy_analytics(pathy_object=pathy_object)

            # final data to give to user
            final_data = {}
            final_data.update({'pathy': pathy})
            final_data.update({'text': summary_table.objects.get(pathy__pk=pathy_object.pk).summary})
            logger.info("pathy name and text fetched")

            information_sources = set()
            for data in data_table.objects.filter(pathy__pk=pathy_object.pk):
                information_sources.add(data.source.name)

            if len(case_table.objects.filter(pathy__pk=pathy_object.pk, show=True))!=0:
                information_sources.add(DIRECT_CASE)

            final_data.update({'informationSources': list(information_sources)})
            logger.info("all information source fetched")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)



class BooksView(View):
    def get(self, request, disease, pathy):
        start_time = time.time()
        logger.info("\nrequest to book view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # check whether show=True for disease
            disease_object = disease_table.objects.get(name=disease)
            if disease_object.show is False:
                return JsonResponse(data={"message": "No data for this disease"}, status=404)
            
            # check whether show=True for pathy
            pathy_object = pathy_table.objects.get(disease__name=disease, name=pathy)
            if pathy_object.show is False:
                return JsonResponse(data={"message": "No data for this Pathy"}, status=404)

            # update the count in analytics table
            update_disease_analytics(disease_object=disease_object)
            update_pathy_analytics(pathy_object=pathy_object)

            # final data to give to user
            final_data = {}

            # refining book data
            book_data = []
            for book in book_table.objects.filter(pathy__pk=pathy_object.pk, show=True):
                book_data.append({
                    "name": book.name,
                    "author": book.author,
                    "rating": str(book.rating),
                    "text": book.text,
                    "imageLink": book.image_link.url,
                    "buyLink": book.buy_link
                })

            # get all the relevant books data
            final_data.update({"books": book_data})
            logger.info("all books fetched")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)


class SourceView(View):
    def get(self, request, disease, pathy, source):
        start_time = time.time()
        logger.info("\nrequest to source view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # check whether show=True for disease
            disease_object = disease_table.objects.get(name=disease)
            if disease_object.show is False:
                logger.info("disease show is false")
                return JsonResponse(data={"message": "No data for this disease"}, status=404)
            
            # check whether show=True for pathy
            pathy_object = pathy_table.objects.get(disease__name=disease, name=pathy)
            if pathy_object.show is False:
                logger.info("pathy show is false")
                return JsonResponse(data={"message": "No data for this Pathy"}, status=404)
            
            # check whether show=True for source
            source_object = source_table.objects.get(name=source)
            if source_object.show is False:
                logger.info("source show is false")
                return JsonResponse(data={"message": "No data for this source"}, status=404)

            # update the count in analytics table
            update_disease_analytics(disease_object=disease_object)
            update_pathy_analytics(pathy_object=pathy_object)

            # data to be sent to user
            final_data = {}
            final_data.update({'text': source_object.text})
            logger.info("source text fetched")

            if source=='directCase':
                # get all the data of direct testimonial
                case_list = []
                for case in case_table.objects.filter(pathy__pk=pathy_object.pk, show=True):
                    case_list.append({
                        "caseId": str(case.pk),
                        "title": case.title,
                        "summary": case.summary,
                        "rating": str(case.rating),
                        "comment": case.comment
                    })
                final_data.update({'sourceList': case_list})
                logger.info("all direct cases fetched")
            else:
                # get all the data of a source
                source_list = []
                for src in data_table.objects.filter(pathy__pk=pathy_object.pk, source__pk=source_object.pk, show=True):
                    source_list.append({
                        "id": str(src.pk),
                        "title": src.title,
                        "link": src.link,
                        "summary": src.summary,
                        "rating": str(src.rating),
                        "comment": src.comment
                    })
                final_data.update({'sourceList': source_list})
                logger.info("all source data fetched")

            if source=='socialMedia':
                # add whatsapp data if source is social media
                final_data.update({'whatsappData': whatsapp_table.objects.get(pathy__pk=pathy_object.pk, show=True).link})
                logger.info("whatsapp data fetched")
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)


class CaseView(View):
    def get(self, request, disease, pathy, case_id):
        start_time = time.time()
        logger.info("\nrequest to case view")
        logger.info(f"Time: {datetime.now()}")
        try:
            # check whether show=True for disease
            disease_object = disease_table.objects.get(name=disease)
            if disease_object.show is False:
                logger.info("disease show is false")
                return JsonResponse(data={"message": "No data for this disease"}, status=404)
            
            # check whether show=True for pathy
            pathy_object = pathy_table.objects.get(disease__name=disease, name=pathy)
            if pathy_object.show is False:
                logger.info("pathy show is false")
                return JsonResponse(data={"message": "No data for this Pathy"}, status=404)

            # check whether show=True for case
            case_object = case_table.objects.get(pk=case_id)
            if case_object.show is False:
                logger.info("case view is false")
                return JsonResponse(data={"message": "No data for this source"}, status=404)
            
            # update the count in analytics table
            update_disease_analytics(disease_object=disease_object)
            update_pathy_analytics(pathy_object=pathy_object)

            # data to send to user
            final_data = {}
            final_data.update({"caseId": str(case_id)})
            final_data.update({"title": case_object.title})
            final_data.update({"summary": case_object.summary})
            final_data.update({"comment": case_object.comment})

            if case_object.history_link is not None:
                final_data.update({"caseHistory": case_object.history_link})
            
            if case_object.allergies_link is not None:
                final_data.update({"allergies": case_object.allergies_link})
            
            if case_object.reports_link is not None:
                final_data.update({"medicalReport": case_object.reports_link})
            logger.info("case general information fetched")

            # personal details to add
            personal_details = {}
            personal_details.update({"sex": case_object.sex.sex})

            if case_object.age is not None:
                personal_details.update({"age": case_object.age})

            if case_object.occupation is not None:
                personal_details.update({"occupation": case_object.occupation})

            if case_object.state is not None and case_object.country is not None:
                personal_details.update({"region": case_object.state + ", " + case_object.country})
            logger.info("case user general information fetched")

            # add details which allowed to be added
            if case_object.show_name is True and case_object.first_name is not None and case_object.last_name is not None:
                personal_details.update({"name": case_object.first_name + " " + case_object.last_name})

            if case_object.show_email is True and case_object.email_address is not None:
                personal_details.update({"emailAddress": case_object.email_address})

            if case_object.show_phone_number is True and case_object.phone_number is not None:
                personal_details.update({"phoneNumber": case_object.phone_number})

            if case_object.show_address is True and case_object.street_address is not None and case_object.zip_code is not None:
                personal_details.update({"address": case_object.street_address + " (" + case_object.zip_code + ")"})
            logger.info("user optional information fetched")

            # add personal details to final_data
            final_data.update({"personalDetails": personal_details})
            logger.info(f"Time taken: {time.time()-start_time}")
            return JsonResponse(data=final_data, status=200)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"message": "error while getting data"}, status=500)
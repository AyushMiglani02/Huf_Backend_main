from django.shortcuts import render
import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpResponseRedirect
import datetime
from .models import disease_analytics_table, pathy_analytics_table
from disease.models import disease_table, pathy_table
from django.http import JsonResponse

def has_plot(obj):
    return hasattr(obj, "plot")

def get_all_disease_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin/")

    if not request.user.is_superuser:
        return JsonResponse(data={"message": "not authorized"}, status=401)
    
    context = {
        "obj_list": []
    }
    obj_list1 = []

    pie_chart_info = {
        "labels": [],
        "values": []
    }

    for disease in disease_table.objects.all():
        disease_analytics_objs = disease_analytics_table.objects.filter(disease=disease).order_by("-date")
        x = [obj.date for obj in disease_analytics_objs]
        y = [obj.count for obj in disease_analytics_objs]
        temp = {
            "name": disease.name,
        }
        if len(x)>0:
            temp["plot"] = px.line(
                x=x,
                y=y,
                labels={"x": "Date", "y": "views"}
            ).to_html()
            context["obj_list"].append(temp)
        else:
            obj_list1.append(temp)

        if sum(y)>0:
            pie_chart_info[disease.name] = sum(y)
    
    for obj in obj_list1:
        context["obj_list"].append(obj)

    context["pie_chart"] = px.pie(
        pie_chart_info,
        labels=list(pie_chart_info.keys()),
        values=list(pie_chart_info.values()),
        names=list(pie_chart_info.keys()),
        hole=.5
    ).to_html()
    context["pie_chart_info"] = pie_chart_info 

    return render(request, "analytics/all_disease.html", context)

def get_disease_data(request, disease):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin/")
    
    if not request.user.is_superuser:
        return JsonResponse(data={"message": "not authorized"}, status=401) 

    context = {
        "disease": disease,
        "obj_list": []
    }
    obj_list1 = []

    pie_chart_info = {
        "labels": [],
        "values": []
    }

    for pathy in pathy_table.objects.filter(disease__name=disease):
        pathy_analytics_objs = pathy_analytics_table.objects.filter(pathy=pathy).order_by("-date")
        x = [obj.date for obj in pathy_analytics_objs]
        y = [obj.count for obj in pathy_analytics_objs]
        temp = {
            "name": pathy.name,
        }
        if len(x)>0:
            temp["plot"] = px.line(
                x=x,
                y=y,
                labels={"x": "Date", "y": "views"}
            ).to_html()
            context["obj_list"].append(temp)
        else:
            obj_list1.append(temp)

        if sum(y)>0:
            pie_chart_info[pathy.name] = sum(y)
    
    for obj in obj_list1:
        context["obj_list"].append(obj)

    context["pie_chart"] = px.pie(
        pie_chart_info,
        labels=list(pie_chart_info.keys()),
        values=list(pie_chart_info.values()),
        names=list(pie_chart_info.keys()),
        hole=.5
    ).to_html()
    context["pie_chart_info"] = pie_chart_info 

    return render(request, "analytics/disease_analytics.html", context)

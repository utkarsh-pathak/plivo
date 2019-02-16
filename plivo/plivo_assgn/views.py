from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
import json
from django.core.paginator import Paginator
from django.http import QueryDict, HttpResponse
from plivo.responses import *
from .models import ContactBook

# Create your views here.
class Index(View):

    def get(self, request):
        return HttpResponse('<h1>Welcome to Plivo Assignment !</h1>') 




class ContactBookCRUD(View):

    def get(self, request):
        try:
            response = init_response()
            data = request.GET.dict()
            contact_id = data.get('id')
            contact = get_object_or_404(ContactBook, pk=contact_id)
            response['res_data'] = contact.serialize()
        except Exception as e:
            error_response={}
            return send_400(error_response)
        return send_200(response)

    def post(self, request):
        data, response = request.POST, init_response()
        data = dict_from_query_dict(data)
        try:
            contact = ContactBook(**data)
            contact.save()
            response['res_str'] = 'Contact Created Successfully!'
            response['res_data'] = contact.serialize()
        except:
            error_response={}
            return send_400(error_response)
        return send_201(response)
    
    def put(self, request, id):
        data, response = QueryDict(request.body), init_response()
        data = dict_from_query_dict(data)
        contact = get_object_or_404(ContactBook, pk=id)
        try:
            updated_row = ContactBook.objects.filter(pk=id).update(**data)
            response['res_str'] = 'Contact Updated Successfully!'
            response['res_data'] = contact.serialize()
        except:
            error_response={}
            return send_400(error_response)
        return send_200(response)

    def delete(self, id, request):
        ''' soft deletion performed '''
        contact = get_object_or_404(ContactBook, pk=id)
        contact.is_deleted = True
        contact.save()
        response = init_response()
        response['res_str'] = 'Resoure Deleted'
        return send_204(response)


class SearchByParams(View):
    def get(self, request):
        try:
            response = init_response()
            data = request.GET.dict()
            items_per_page, page_num = data.get('items_per_page'), data.get('page_num')
            if not (items_per_page or page_num):
                return send_400({"res_str": "Please Check Request Params!"})
            if not((data.get('search_by').lower() == 'name') or data.get('search_by').lower() == 'email'):
                return send_400({"res_str": "Please Check Request Params!"})
            if(data.get('search_by').lower() == 'name'):
                name = data.get('search_val')
                if not name:
                    return send_400({"res_str": "Please Check Request Params!"})
                contacts = ContactBook.objects.filter(name__icontains=name)
                page_obj = Paginator([c for c in contacts], int(items_per_page))
                page = page_obj.page(int(page_num))
                to_return = [c.serialize() for c in page.object_list]
            elif data.get('search_by').lower() == 'email':
                email = data.get('search_val')
                if not email:
                    return send_400({"res_str": "Please Check Request Params!"})
                contacts = ContactBook.objects.filter(email_address__icontains=email)
                page_obj = Paginator([c for c in contacts], int(items_per_page))
                page = page_obj.page(int(page_num))
                to_return = [c.serialize() for c in page.object_list]
            response['res_data'] = to_return
        except Exception as e:
            error_response={}
            return send_400(error_response)
        return send_200(response)



def dict_from_query_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        data[key] = query_dict[key]
    return data
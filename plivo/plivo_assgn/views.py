from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
import json
from django.http import QueryDict
from plivo.responses import *
from .models import ContactBook

# Create your views here.

class ContactBookCRUD(View):

    def get(self, request):
        try:
            response = init_response()
            data = request.GET.dict()
            contact_id = data.get('id')
            try:
                contact = ContactBook.objects.get(pk=contact_id)
            except Question.DoesNotExist:
                raise Http404("Contact does not exist")
            except:
                return send_400({"res_str": "Please Check ID!"})
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
            if not((data.get('search_by').lower() == 'name') or data.get('search_by').lower() == 'email'):
                return send_400({"res_str": "Please Check Request Params!"})
            if(data.get('search_by').lower() == 'name'):
                name = data.get('search_val')
                if not name:
                    return send_400({"res_str": "Please Check Request Params!"})
                contacts = ContactBook.objects.filter(name__icontains=name)
                to_return = [c.serialize() for c in contacts]
            elif data.get('search_by').lower() == 'email':
                email = data.get('search_val')
                if not email:
                    return send_400({"res_str": "Please Check Request Params!"})
                contacts = ContactBook.objects.filter(email_address__icontains=email)
                to_return = [c.serialize() for c in contacts]
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
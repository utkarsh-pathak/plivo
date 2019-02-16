from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from datetime import datetime

def get_all_fields(field_list_1, field_list_2):
    field_list = list(field_list_1) + list((field_list_2))
    return field_list

def convert_date(field, date_format):
    """Convert datetime to str."""
    # convert_date will convert the date in given format
    return field.strftime(date_format)

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='created_on', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True,
                                      verbose_name='update_on', null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name='deleted')

    class Meta:
        abstract = True


class CustomUser(User, BaseModel):
    username_validator = ASCIIUsernameValidator()

    def __str__(self):
        return str(self.pk) + ' ' + str(self.first_name) + ' ' + str(self.last_name)




class ContactBook(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, default="unsaved")
    email_address = models.CharField(max_length=255, blank=False, null=False, unique=True)
    primary_contact_of = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + ' ' + str(self.name) + ' ' + str(self.email_address)

    def serialize(self, m2m=False):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)
        for field in field_list:
            if field.many_to_one:
                data[field.name] = getattr(self, field.name + '_id')
            elif field.many_to_many:
                m2m_list = []
                if m2m:
                    m2m_list = [obj.serializer() for obj in getattr(self,
                                                                    field.name).all()]
                    data[field.name] = m2m_list
            else:
                if isinstance(getattr(self, field.name), datetime):
                    data[field.name] = convert_date(getattr(self, field.name),
                                                    '%Y-%m-%d %H:%M:%S')
                else:
                    data[field.name] = getattr(self, field.name)
        # here goes properties
        return data
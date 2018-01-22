from django.db import models
from datetime import datetime,timezone

class Taxonomy_Node(models.Model):
    Identifier = models.IntegerField(primary_key=True)
    Parent = models.IntegerField(blank=False)
    Name = models.CharField(max_length=127, blank=False)
    IsCategory = models.BooleanField(default=False)
    Description = models.CharField(max_length=255)

    def __str__(self):
        return_string = str(self.Identifier) + ', '
        return_string += str(self.Parent) + ', '
        return_string += self.Name + ', '
        return_string += str(self.IsCategory) + ', '
        return_string += self.Description
        return return_string

def Load_DB_Taxonomy():
    return list(Taxonomy_Node.objects.values_list())

class Search_Request(models.Model):
    DateTime = models.DateTimeField()
    Text = models.CharField(max_length=127, blank=False)

    def record_DateTime(self):
        self.DateTime = datetime.now(timezone.utc)

    def __str__(self):
        return_string = str(self.id) + ', '
        return_string += str(self.DateTime) + ', '
        return_string += self.Text
        return return_string

def ProcessNewCustomQuery (CustomQuery):
    LastCustomRequest = Load_RecentCustomRequests(1)
    if (LastCustomRequest[0][2] != CustomQuery):
        NewCustomRequest = Search_Request(Text=CustomQuery)
        NewCustomRequest.record_DateTime()
        NewCustomRequest.save()

def Load_RecentCustomRequests(QueryNum):
    return list(Search_Request.objects.order_by('-DateTime').values_list()[:QueryNum])
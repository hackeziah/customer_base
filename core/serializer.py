from rest_framework import serializers
from .models import Customer, Profession,DataSheet,Document

class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = (
            'id','name','address','profession','data_sheet','cu_number','active','status_message','num_professions'
        )
    def get_num_professions(self,obj): #setting method Objects in Model
        return obj.num_professions()
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields =  (
          'id', 'description'
        )

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id','description','historical_data' )

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id','dtype','doc_number','customer'
        )
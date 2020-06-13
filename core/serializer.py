from rest_framework import serializers
from .models import Customer, Profession,DataSheet,Document

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

    read_omly_fields = ['customer'] #setup for readonly fields


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    # data_sheet = DataSheetSerializer(read_only = True)
    data_sheet = DataSheetSerializer()

    profession = ProfessionSerializer(many = True) # use this for many relation in Field (Whole)
    document_set = DocumentSerializer(many=True)
    # document_set =  serializers.StringRelatedField(many = True)

    # profession = ProfessionSerializer() for Professions
    # data_sheet = serializers.PrimaryKeyRelatedField(read_only = True,many = True)

    class Meta:
        model = Customer
        fields = (
            'id','name','address','profession','data_sheet','document_set','cu_number','active','status_message','num_professions'
        )
    def create(self,validated_data):#this is for serializer for create Many to many relationship
        profession = validated_data['profession'] #many to many
        del validated_data['profession']

        document_set = validated_data['document_set'] #one is to Foreign
        del validated_data['document_set']

        data_sheet = validated_data['data_sheet'] #one is to one
        del validated_data['data_sheet']

        d_sheet = DataSheet.objects.create(**data_sheet)  #one is to one
        customer = Customer.objects.create(**validated_data)
        customer.data_sheet = d_sheet

        for doc in document_set:#one is to Foreign
            Document.objects.create(
                dtype = document_set['dtype'],
                doc_number = document_set['doc_number'],
                customer_id = customer.id,
            )

        for pro in profession: #many to many
            pro = Profession.objects.create(**pro)
            customer.profession.add(pro)

        customer.save()
        return customer

    def get_num_professions(self,obj): #setting method Objects in Model
        return obj.num_professions()

    def get_data_sheet(self,obj): #setting method Objects in Model
        return obj.data_sheet.description #String Relation Fields


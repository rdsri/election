import csv
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ParlimentReport, CasteReport, StateReport
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
# Create your views here.

class GetParlimentData(APIView):
    def get(self,request:Request):
        print(request.GET)
        parliment = request.GET.get('parliment','')
        assembly = request.GET.get('assembly','')
        year = request.GET.get('year','')
        booth = request.GET.get('booth','')
        party_data = request.GET.get('party','')
        votecount = request.GET.get('votecount','')
        votecondition = request.GET.get('votecondition','')
        print("parliment-->",parliment)
        print("assembly--->",assembly)
        print("year---->",year)
        filter_params = {}
        if parliment:
            filter_params['parliment_Assembly_Name'] = parliment
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if year:
            filter_params['year'] = year
        if booth:
            filter_params['booth_Name'] = booth
        if party_data:
            filter_params['Party_Name'] = party_data
        if votecount and votecondition:
            if votecondition == 'greaterthan equal':
                filter_params['vote_Percentage__gte'] = votecount
            elif votecondition == 'lesserthan equal':
                filter_params['vote_Percentage__lte'] = votecount
        print("filter_data--",filter_params)
        data = ParlimentReport.objects.filter(**filter_params)
        filter_data = ParlimentReport.objects.all().values()
        p_assembly = filter_data.values('parliment_Assembly_Name').distinct()
        s_assembly = filter_data.values('state_Assembly_Name').distinct()
        years = filter_data.values('year').distinct()
        booth = filter_data.values('booth_Name').distinct()
        party = filter_data.values('Party_Name').distinct()
        print("s_assembly-->",s_assembly)
        if data or filter_data:
            return Response({"result": 200, 
                            "data": data.values(), 
                            "p_assembly": p_assembly, 
                            # "s_assembly": s_assembly,
                            # "booth": booth,
                            "party":party,
                            "years": years,
                            })
        else:
            return Response({"result": 400, "data": "data not available"})

class GetParlimentfilterData(APIView):
    def get(self, request:Request):
        print(request)
        print(request.GET.get('year'))
        parliment_data = request.GET.get('p_name')
        assembly = request.GET.get('a_name')
        booth_data = request.GET.get('b_name')
        filter_query = {}
        if parliment_data:
            filter_query['parliment_Assembly_Name'] = parliment_data
        if assembly:
            filter_query['state_Assembly_Name'] = assembly
        if booth_data:
            filter_query['booth_Name'] = booth_data
        print("filter_query--->",filter_query)
        data= ParlimentReport.objects.filter(**filter_query)
        print("filter data--->",data)
        s_assembly = data.values('state_Assembly_Name').distinct()
        booth_data = data.values('booth_Name').distinct()
        party_data = data.values('Party_Name').distinct()
       
        return Response({"result": 200, 
                "s_assembly": s_assembly,
                "booth_data":booth_data,
                "party_data":party_data,
                })

class GetParlimentCsvData(APIView):
    def get(self, request:Request):
        print("testtt")
        print(request.GET)
        parliment = request.GET.get('parliment','')
        assembly = request.GET.get('assembly','')
        year = request.GET.get('year','')
        booth = request.GET.get('booth','')
        party_data = request.GET.get('party','')
        votecount = request.GET.get('votecount','')
        votecondition = request.GET.get('votecondition','')
        filter_params = {}
        if parliment:
            filter_params['parliment_Assembly_Name'] = parliment
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if year:
            filter_params['year'] = year
        if booth:
            filter_params['booth_Name'] = booth
        if party_data:
            filter_params['Party_Name'] = party_data
        if votecount and votecondition:
            if votecondition == 'greaterthan equal':
                filter_params['vote_Percentage__gte'] = votecount
            elif votecondition == 'lesserthan equal':
                filter_params['vote_Percentage__lte'] = votecount
        print("filter_data--",filter_params)
        parliment_data = ParlimentReport.objects.filter(**filter_params).values()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parliment_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['parliment_Assembly_Name', 'state_Assembly_Name',
                         'booth_Name', 'Party_Name', 'vote_Percentage',
                         'total_Vote', 'year'])  # CSV header

        for row in parliment_data:
            writer.writerow([row['parliment_Assembly_Name'], row['state_Assembly_Name'],
                             row['booth_Name'],row['Party_Name'],
                             row['vote_Percentage'],row['total_Vote'],
                             row['year']])
        
        return response

class UploadParlimentData(APIView):
    def post(self,request:Request):
        print(request.FILES.get('csvFile'))
        csv_file = request.FILES.get('csvFile')
        print("csv_file-->",csv_file)
        csv_content = csv_file.read().decode('utf-8')
        csv_data = list(csv.reader(csv_content.splitlines()))
        print(csv_data)
        if csv_data:
            party_data = csv_data[0]
            csv_data.pop(0)
            print("party_data-->",party_data)
            party_data_count = (party_data.index('Total votes')+1)
            print("party_data_count->",party_data_count)
            for row in csv_data:
                print("row-->",row)
                for party_type in range(party_data_count,len(row)):
                    print("row[party_type]-->",party_data[party_type])
                    print("row[party_count]->",row[party_type])
                    parliment_report = ParlimentReport.objects.create(
                        parliment_Assembly_Name=row[1],
                        state_Assembly_Name=row[2],
                        booth_Name=row[3],
                        total_Vote=row[4],
                        Party_Name=party_data[party_type],
                        vote_Percentage=row[party_type],
                        year=row[0]
                    )
                    # parliment_report.save()
                    print("parliment_report-->",parliment_report)
            return Response({"message":True},status=status.HTTP_200_OK)
        else:     
            return Response({"message":False},status=status.HTTP_400_BAD_REQUEST)
        


class GetCasteData(APIView):
    def get(self,request:Request):
        parliment = request.GET.get('parliment','')
        assembly = request.GET.get('assembly','')
        booth = request.GET.get('booth','')
        caste_data = request.GET.get('caste','')
        filter_params = {}
        if parliment:
            filter_params['parliment_Assembly_Name'] = parliment
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if booth:
            filter_params['booth_Name'] = booth
        if caste_data:
            filter_params['caste_name'] = caste_data
        data = CasteReport.objects.filter(**filter_params)
        filter_data = CasteReport.objects.all().values()
        p_assembly = filter_data.values('parliment_Assembly_Name').distinct()
        booth = filter_data.values('booth_Name').distinct()
        caste = filter_data.values('caste_name').distinct()
        if data or filter_data:
            return Response({"result": 200, 
                            "data": data.values(), 
                            "p_assembly": p_assembly, 
                            "caste":caste,
                            })
        else:
            return Response({"result": 400, "data": "data not available"})
        
class GetCastefilterData(APIView):
    def get(self, request:Request):
        parliment_data = request.GET.get('p_name')
        assembly = request.GET.get('a_name')
        booth_data = request.GET.get('b_name')
        filter_query = {}
        if parliment_data:
            filter_query['parliment_Assembly_Name'] = parliment_data
        if assembly:
            filter_query['state_Assembly_Name'] = assembly
        if booth_data:
            filter_query['booth_Name'] = booth_data
        print("filter_query--->",filter_query)
        data= CasteReport.objects.filter(**filter_query)
        s_assembly = data.values('state_Assembly_Name').distinct()
        booth_data = data.values('booth_Name').distinct()
        caste_data = data.values('caste_name').distinct()
       
        return Response({"result": 200, 
                "s_assembly": s_assembly,
                "booth_data":booth_data,
                "caste_data":caste_data,
                })

class GetCasteCsvData(APIView):
    def get(self, request:Request):
        parliment = request.GET.get('parliment','')
        assembly = request.GET.get('assembly','')
        booth = request.GET.get('booth','')
        castes_data = request.GET.get('caste','')

        filter_params = {}
        if parliment:
            filter_params['parliment_Assembly_Name'] = parliment
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if booth:
            filter_params['booth_Name'] = booth
        if castes_data:
            filter_params['caste_name'] = castes_data

        print("filter_data--",filter_params)
        caste_data = CasteReport.objects.filter(**filter_params).values()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parliment_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['parliment_Assembly_Name', 'state_Assembly_Name',
                         'booth_Name', 'caste_name', 'count'])  

        for row in caste_data:
            writer.writerow([row['parliment_Assembly_Name'], row['state_Assembly_Name'],
                             row['booth_Name'],row['caste_name'],row['count']])
        
        return response

class UploadCasteData(APIView):
    def post(self,request:Request):
        print(request.FILES.get('csvFile'))
        csv_file = request.FILES.get('csvFile')
        print("csv_file-->",csv_file)
        csv_content = csv_file.read().decode('utf-8')
        csv_data = list(csv.reader(csv_content.splitlines()))
        print(csv_data)
        if csv_data:
            party_data = csv_data[0]
            csv_data.pop(0)
            print("party_data-->",party_data)
            party_data_count = (party_data.index('Count')+1)
            print("party_data_count->",party_data_count)
            for row in csv_data:
                print("row-->",row)
                for party_type in range(party_data_count,len(row)):
                    print("row[party_type]-->",party_data[party_type])
                    print("row[party_count]->",row[party_type])
                    parliment_report = CasteReport.objects.create(
                        parliment_Assembly_Name=row[1],
                        state_Assembly_Name=row[2],
                        booth_Name=row[3],
                        caste_name=party_data[party_type],
                        count=row[party_type],
                    )
                    # parliment_report.save()
                    print("parliment_report-->",parliment_report)
            return Response({"message":True},status=status.HTTP_200_OK)
        else:     
            return Response({"message":False},status=status.HTTP_400_BAD_REQUEST)
        


class GetStateData(APIView):
    def get(self,request:Request):
        print(request.GET)
        assembly = request.GET.get('assembly','')
        year = request.GET.get('year','')
        booth = request.GET.get('booth','')
        party_data = request.GET.get('party','')
        votecount = request.GET.get('votecount','')
        votecondition = request.GET.get('votecondition','')
        filter_params = {}
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if year:
            filter_params['year'] = year
        if booth:
            filter_params['booth_Name'] = booth
        if party_data:
            filter_params['Party_Name'] = party_data
        if votecount and votecondition:
            if votecondition == 'greaterthan equal':
                filter_params['vote_Percentage__gte'] = votecount
            elif votecondition == 'lesserthan equal':
                filter_params['vote_Percentage__lte'] = votecount
        print("filter_data--",filter_params)
        data = StateReport.objects.filter(**filter_params)
        filter_data = StateReport.objects.all().values()
        s_assembly = filter_data.values('state_Assembly_Name').distinct()
        years = filter_data.values('year').distinct()
        party = filter_data.values('Party_Name').distinct()
        if data or filter_data:
            return Response({"result": 200, 
                            "data": data.values(), 
                            "s_assembly": s_assembly,
                            "party":party,
                            "years": years,
                            })
        else:
            return Response({"result": 400, "data": "data not available"})

class GetStatefilterData(APIView):
    def get(self, request:Request):
        print(request)
        assembly = request.GET.get('a_name')
        booth_data = request.GET.get('b_name')
        filter_query = {}
        if assembly:
            filter_query['state_Assembly_Name'] = assembly
        if booth_data:
            filter_query['booth_Name'] = booth_data
        print("filter_query--->",filter_query)
        data= StateReport.objects.filter(**filter_query)
        print("filter data--->",data)
        s_assembly = data.values('state_Assembly_Name').distinct()
        booth_data = data.values('booth_Name').distinct()
        party_data = data.values('Party_Name').distinct()
       
        return Response({"result": 200, 
                "s_assembly": s_assembly,
                "booth_data":booth_data,
                "party_data":party_data,
                })

class GetStateCsvData(APIView):
    def get(self, request:Request):
        print(request.GET)
        assembly = request.GET.get('assembly','')
        year = request.GET.get('year','')
        booth = request.GET.get('booth','')
        party_data = request.GET.get('party','')
        votecount = request.GET.get('votecount','')
        votecondition = request.GET.get('votecondition','')
        filter_params = {}
        if assembly:
            filter_params['state_Assembly_Name'] = assembly
        if year:
            filter_params['year'] = year
        if booth:
            filter_params['booth_Name'] = booth
        if party_data:
            filter_params['Party_Name'] = party_data
        if votecount and votecondition:
            if votecondition == 'greaterthan equal':
                filter_params['vote_Percentage__gte'] = votecount
            elif votecondition == 'lesserthan equal':
                filter_params['vote_Percentage__lte'] = votecount
        print("filter_data--",filter_params)
        parliment_data = StateReport.objects.filter(**filter_params).values()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parliment_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['year', 'state_Assembly_Name',
                         'booth_Name', 'Party_Name', 'vote_Percentage',
                         'total_Vote'])  

        for row in parliment_data:
            writer.writerow([row['year'],row['state_Assembly_Name'],
                             row['booth_Name'],row['Party_Name'],
                             row['vote_Percentage'],row['total_Vote'],
                             ])
        
        return response

class UploadStateData(APIView):
    def post(self,request:Request):
        print(request.FILES.get('csvFile'))
        csv_file = request.FILES.get('csvFile')
        print("csv_file-->",csv_file)
        csv_content = csv_file.read().decode('utf-8')
        csv_data = list(csv.reader(csv_content.splitlines()))
        print(csv_data)
        if csv_data:
            party_data = csv_data[0]
            csv_data.pop(0)
            print("party_data-->",party_data)
            party_data_count =(party_data.index('Total votes')+1)
            print("party_data_count->",party_data_count)
            for row in csv_data:
                print("row-->",row)
                for party_type in range(party_data_count,len(row)):
                    print("row[party_type]-->",party_data[party_type])
                    print("row[party_count]->",row[party_type])
                    parliment_report = StateReport.objects.create(
                        state_Assembly_Name=row[1],
                        booth_Name=row[2],
                        total_Vote=row[3],
                        Party_Name=party_data[party_type],
                        vote_Percentage=row[party_type],
                        year=row[0]
                    )
                    # parliment_report.save()
                    print("parliment_report-->",parliment_report)
            return Response({"message":True},status=status.HTTP_200_OK)
        else:     
            return Response({"message":False},status=status.HTTP_400_BAD_REQUEST)
        
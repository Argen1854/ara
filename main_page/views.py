from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from datetime import datetime
from business_accounts import models
import calendar
from rest_framework import filters
from rest_framework.pagination import CursorPagination

class PaginationA(CursorPagination):
    page_size = 8
    page_size_query_param = 'size'
    ordering = '-id'
    page_size_query_param = None

class MainPageSearch(ListAPIView):
    queryset = models.BusinessAccount.objects.all()
    pagination_class = PaginationA
    serializer_class = serializers.BusinessAccountAPIViewSerializers
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class MainPage(ListAPIView):
    queryset = models.BusinessAccount.objects.all()
    pagination_class = PaginationA
    serializer_class = serializers.BusinessAccountAPIViewSerializers


class BusinessAccountDetail(RetrieveAPIView):
    queryset = models.BusinessAccount.objects.all()
    serializer_class = serializers.BusinessAccountAPIViewSerializers

    def get(self, request, id):
        bs = self.queryset.get(id=id)
        data = self.serializer_class(bs).data
        return Response(data = data)


class BusinessAccountService(ListAPIView):
    queryset = models.SalonService.objects.all()
    serializer_class = serializers.BusinessAccountServiceSerializers

    def get(self, request, id):
        service = self.queryset.filter(salon_id=id)
        data = self.serializer_class(service, many=True).data
        return Response(data = data)


class BusinessAccountStaff(ListAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.BusinessAccountStaffSerializers

    def get(self, request, id):
        service = self.queryset.filter(salon_id=id)
        data = self.serializer_class(service, many=True).data
        return Response(data = data)


class BusinessAccountStaff(RetrieveAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializers

    def get(self, request, id):
        bs = self.queryset.get(id=id)
        data = self.serializer_class(bs).data
        timetable = models.StaffTimetable.objects.filter(staff_id = id)
        data2 = serializers.StaffTimetableSerializers(timetable, many=True).data
        return Response(data = [data]+data2)

class SalonReview(ListAPIView):
    queryset = models.SalonReview
    serializer_class = serializers.SalonReviewSerializer

    def get(self, request, id):
        ara = self.queryset.filter(salon_id=id)
        data = self.serializer_class(ara, many=True).data
        return Response(data = data)


class StaffReview(ListAPIView):
    queryset = models.StaffReview
    serializer_class = serializers.StaffReviewSerializer

    def get(self, request, id):
        ara = self.queryset.filter(staff_id=id)
        data = self.serializer_class(ara, many=True).data
        return Response(data = data)



class CreateListRecordsAPIView(ListAPIView):
    serializer_class = serializers.CreateRecordsAPIViewSerializer
    def get(self, request):
        model = models.Records.objects.all()
        data = serializers.RecordsSerializers(model, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = serializers.CreateRecordsAPIViewSerializer(data= request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors}, status = status.HTTP_406_NOT_ACCEPTABLE)
        user_id = request.data.get('user_id')
        data = request.data.get('data')
        time = request.data.get('time')
        staff_id = request.data.get('staff_id')
        service_id = request.data.get('service_id')
        businessaccount_id = request.data.get('businessaccount_id')
        promo_code = request.data.get('promo_code')
        print(time)
        service = models.SalonService.objects.get(id = service_id)
        if promo_code == None:
            price = service.price
            discount = 0
        elif models.PromoCode.objects.filter(promo_code = promo_code).count() == 0:
                return Response(data={'message': 'Такого промокода не существует!'})
        else:
            promocode = models.PromoCode.objects.get(promo_code = promo_code)
            discount = promocode.discount
            price = (service.price - discount)
        if models.Records.objects.filter(data=data, time=time, staff_id=staff_id).count() == 0 and datetime.now() < datetime.strptime(data+time, "%Y-%m-%d%H:%M"):
            records = models.Records.objects.create(user_id=user_id,data=data,time= time, promo_code=promo_code, discount=discount, price= price, staff_id=staff_id, service_id=service_id, businessaccount_id=businessaccount_id)
        else:
            return Response(data ={'message': 'Дата с таким временем уже занята!'})
        return Response(data= serializers.RecordsSerializers(records).data, status=status.HTTP_201_CREATED)




class ListTimeRecordsAPIView(ListAPIView):
    def get(self, request, id):
        if request.GET.get('data') != None:
            date = request.GET.get('data')
        else:
            date = datetime.now()
        model = models.TimeRecords.objects.filter(staff_id=id)
        free_time = []
        for i in model:
            if models.Records.objects.filter(time= i.time, data=date).count() ==0:
                free_time.append(i)
        return Response(data=[{'free_time': i.time} for i in free_time])
        

class ListFreeDayAPIView(ListAPIView):
    serializer_class = serializers.SraffAPIViewSerializer
    def get(self, request, id):
        model = models.TimeRecords.objects.filter(staff_id=id)
        day_off = models.StaffTimetable.objects.get(staff_id = id)
        day = {}
        if request.GET.get('data') !=None:
            date = datetime.strptime(request.GET.get('data'), "%Y-%m-%d")
        else:
            date = datetime.now()
        for i in range(1, calendar.monthrange(date.year, date.month)[1]+1):
            d = f'{date.year}-{date.month}-{i}'
            if datetime.strptime(d, "%Y-%m-%d") < date.now() or int(day_off.day_off) == datetime.strptime(d, "%Y-%m-%d").weekday():
                day[d] = "gray_day"
            elif models.Records.objects.filter(data =d, staff_id = id).count() == len(model):
                day[d] = "red_day"
            else:
                day[d] = "green_day"
        return Response(data=day)


class ListUserRecordsAPIView(APIView):
    def get(self, request, id):
        model = models.Records.objects.filter(staff_id=id)
        data = serializers.ListUserRecordsAPIViewSerializers(model, many=True).data
        return Response(data=data)
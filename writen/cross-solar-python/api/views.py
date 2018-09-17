from rest_framework import viewsets,status
from rest_framework.views import APIView, Response
from .models import Panel, OneHourElectricity
from django.db.models import Avg, Sum, Max, Min
from .serializers import (
    PanelSerializer,
    OneHourElectricitySerializer,
    DayElectricitySerializer
)

class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer

class HourAnalyticsView(APIView):
    serializer_class = OneHourElectricitySerializer
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)
    def post(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayAnalyticsView(APIView):
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        # Please implement this method to return Panel's daily analytics data
        queryset = OneHourElectricity.objects\
            .filter(panel_id=panelid)\
            .extra({
                'date_time': 'date(date_time)',
                'sum': 0,
                'average': 0,
                'maximum': 0,
                'minimum': 0,
            })\
            .values('date_time')\
            .annotate(
                sum=Sum('kilo_watt'),
                average=Avg('kilo_watt'),
                maximum=Max('kilo_watt'),
                minimum=Min('kilo_watt'),
            )
            # .values('date_time')\

        # queryset = OneHourElectricity.objects.filter(panel_id=panelid,
        #                                              date_time__lte=today_end,
        #                                              date_time__gte=today_start)

        items = DayElectricitySerializer(queryset, many=True)
        return Response(items.data)

        # return Response([{
        #     "date_time": "[date for the day]",
        #     "sum": 0,
        #     "average": 0,
        #     "maximum": 0,
        #     "minimum": 0
        # }])
        # return Response([{
        #     "date_time": "[date for the day]",
        #     "sum": 0,
        #     "average": 0,
        #     "maximum": 0,
        #     "minimum": 0
        # }])
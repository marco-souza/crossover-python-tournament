from rest_framework.test import APITestCase
from rest_framework import status
from .models import Panel, OneHourElectricity

class PanelTestCase(APITestCase):
    def setUp(self):
        self.input = {
            "brand": "Areva",
            "serial": "AAAA1111BBBB2222",
            "latitude": 12.345678,
            "longitude": 98.765543
        }
        Panel.objects.create(**self.input)

    def test_panel_listing(self):
        response = self.client.get('/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        response = self.client.get('/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")

    def test_panel_post(self):
        response = self.client.post('/panel/', data=self.input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")
        self.assertEqual(response.data["id"], 2)

    def test_panel_post_wrong_long(self):
        data = self.input
        data['longitude'] = 14.1234534
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["longitude"][0]),
                         "Ensure that there are no more than 6 decimal places.")
        data['longitude'] = 123.1234534
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["longitude"][0]),
                         "Ensure that there are no more than 9 digits in total.")

    def test_panel_post_wrong_lat(self):
        data = self.input
        data['latitude'] = 4.1234534
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["latitude"][0]),
                         "Ensure that there are no more than 6 decimal places.")
        data['latitude'] = 123.1234534
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["latitude"][0]),
                         "Ensure that there are no more than 8 digits in total.")

    def test_panel_post_small_serial(self):
        data = self.input
        data['serial'] = '12312'
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["serial"][0]),
                         "Length has to be 16.")

    def test_panel_post_big_serial(self):
        data = self.input
        data['serial'] = '12341234123412341'
        response = self.client.post('/panel/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["serial"][0]),
                         "Length has to be 16.")

class PanelAnalyticsTestCase(APITestCase):
    def setUp(self):
        data_input = {
            "brand": "Areva",
            "serial": "AAAA1111BBBB2222",
            "latitude": 12.345678,
            "longitude": 98.765543
        }
        self.panel = Panel.objects.create(**data_input)
        self.input = {
            "panel": self.panel,
            "kilo_watt": 0,
            "date_time": "2018-09-15T12:59:00Z"
        }
        OneHourElectricity.objects.create(**self.input)

    def test_analytics_listing(self):
        response = self.client.get('/panel/{}/analytics/'.format(self.panel.id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_analytics_get(self):
        response = self.client.get('/panel/{}/analytics/'.format(self.panel.id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['kilo_watt'], 0)

    def test_analytics_post(self):
        data = self.input
        data['kilo_watt'] = 33
        data['panel'] = self.panel.id

        response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['kilo_watt'], 33)
        self.assertEqual(response.data['id'], 2)

        data['kilo_watt'] = 4412
        response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['kilo_watt'], 4412)
        self.assertEqual(response.data['id'], 3)

    def test_analytics_post_wrong_id(self):
        data = self.input
        data['panel'] = self.panel.id + 12

        response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['panel'][0]),
                         'Invalid pk "{}" - object does not exist.'\
                            .format(data['panel']))

    def test_analytics_post_wrong_kilo_watt(self):
        data = self.input
        data['panel'] = self.panel.id
        data['kilo_watt'] = '$12A3'

        response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['kilo_watt'][0]),
                         'A valid integer is required.')

    def test_analytics_post_negative_kilo_watt(self):
        data = self.input
        data['panel'] = self.panel.id
        data['kilo_watt'] = -1

        response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['kilo_watt'][0]),
                         'Ensure this value is greater than or equal to 1.')

    def test_analytics_get_day(self):
        response = self.client.get('/panel/{}/analytics/day/'.format(self.panel.id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sum'], 0)
        self.assertEqual(response.data[0]['average'], 0)
        self.assertEqual(response.data[0]['minimum'], 0)
        self.assertEqual(response.data[0]['maximum'], 0)

    def test_analytics_get_day_aggregations(self):
        data = self.input
        data['panel'] = self.panel.id
        def add_new(val):
            data['kilo_watt'] = val
            response = self.client.post('/panel/{}/analytics/'.format(self.panel.id),
                                        data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # add list
        [add_new(i) for i in range(1,4)]

        response = self.client.get('/panel/{}/analytics/day/'.format(self.panel.id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sum'], 6)
        self.assertEqual(response.data[0]['average'], 6/4)
        self.assertEqual(response.data[0]['minimum'], 0)
        self.assertEqual(response.data[0]['maximum'], 3)

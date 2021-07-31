import json
from django.http.response import HttpResponse
import requests
from django.db.models import Avg
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Car, Rating


@method_decorator(csrf_exempt, name='dispatch')
class Cars(View):

    class __ValidationException(Exception):

        def __init__(self, message, details='', status=400):
            self.message = message
            self.details = details
            self.status = status
            super().__init__(self.message)

        def asJsonResponse(self):
            return JsonResponse({
                'message': self.message,
                'details': self.details},
                status=self.status)

    def get(self, request):
        car_set = Car.objects.all()
        response_data = []
        for car in car_set.iterator():
            avg_rating = Rating.objects.filter(
                car__id=car.id).aggregate(Avg('value')).get('value__avg')
            if not avg_rating:
                avg_rating = 0
            response_data.append({
                'id': car.id,
                'make': car.make,
                'model': car.model,
                'avg_rating': avg_rating
            })
        return JsonResponse(response_data, safe=False, status=200)

    def post(self, request):
        request_data = json.loads(request.body.decode("utf-8"))
        for atr in ['make', 'model']:
            if not atr in request_data:
                message = 'The request is missing an attribute: {}'.format(atr)
                details = atr
                return JsonResponse({'message': message, 'details': details}, status=400)
        make = request_data.get('make')
        model = request_data.get('model')
        try:
            self.__validate_make_and_model(make, model)
        except self.__ValidationException as e:
            return e.asJsonResponse()
        car_data = {
            'make': make,
            'model': model
        }
        car = Car.objects.create(**car_data)
        return JsonResponse({'id': car.id}, status=201)

    def __validate_make_and_model(self, make, model):
        url = 'http://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{}'.format(
            make)
        params = {
            'format': 'json'
        }
        try:
            request = requests.get(url, params)
        except requests.exceptions.RequestException as e:
            message = 'Failed to fetch vehicle data'
            details = str(e)
            raise self.__ValidationException(message, details, 404)
        if request.status_code != 200:
            message = 'Failed to fetch vehicle data'
            details = request.text
            raise self.__ValidationException(message, details, 404)
        does_make_exist = False
        try:
            data = request.json()
            for res in data['Results']:
                if res['Make_Name'].lower() != make.lower():
                    continue
                does_make_exist = True
                if res['Model_Name'] != model:
                    continue
                return None
        except Exception as e:
            message = 'Failed to decode vehicle data'
            details = str(e)
            raise self.__ValidationException(message, details, 404)
        if does_make_exist:
            message = 'The model does not exist'
            details = model
            raise self.__ValidationException(message, details, 404)
        else:
            message = 'The make does not exist'
            details = make
            raise self.__ValidationException(message, details, 404)


@method_decorator(csrf_exempt, name='dispatch')
class CarsUpdate(View):

    def delete(self, request, car_id):
        car_set = Car.objects.filter(id=car_id)
        if car_set.count() == 0:
            message = 'The car does not exist'
            details = car_id
            return JsonResponse({'message': message, 'details': details}, status=404)
        car_set.delete()
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Rate(View):

    def post(self, request):
        request_data = json.loads(request.body.decode("utf-8"))
        for atr in ['car_id', 'rating']:
            if not atr in request_data:
                message = 'The request is missing an attribute: {}'.format(atr)
                details = atr
                return JsonResponse({'message': message, 'details': details}, status=400)
        car_id = request_data.get('car_id')
        rating = request_data.get('rating')
        car = self.__get_car(car_id)
        if not car:
            message = 'The car does not exist'
            details = car_id
            return JsonResponse({'message': message, 'details': details}, status=404)
        if not isinstance(rating, int):
            message = 'The rating must have an int type'
            details = rating
            return JsonResponse({'message': message, 'details': details}, status=400)
        if rating < 1 or rating > 5:
            message = 'The rating must be between 1 and 5'
            details = rating
            return JsonResponse({'message': message, 'details': details}, status=400)
        rating_data = {
            'value': rating,
            'car': car
        }
        rating = Rating.objects.create(**rating_data)
        return JsonResponse({'id': rating.id}, status=201)

    def __get_car(self, car_id):
        car_set = Car.objects.filter(id=car_id)
        if car_set.count() == 0:
            return None
        return car_set[0]


@method_decorator(csrf_exempt, name='dispatch')
class Popular(View):

    def get(self, request):
        # TODO
        pass

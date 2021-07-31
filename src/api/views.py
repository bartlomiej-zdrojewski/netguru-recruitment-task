import json
import requests
from django.db.models import Avg
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from requests import status_codes
from .models import Car, Rating


@method_decorator(csrf_exempt, name='dispatch')
class Cars(View):
    def get(self, request, *args, **kwargs):
        car_set = Car.objects.all()
        response_data = []
        for c in car_set.iterator():
            avg_rating = Rating.objects.filter(
                car__id=c.id).aggregate(Avg('value')).get('value__avg')
            if not avg_rating:
                avg_rating = 0
            response_data.append({
                'id': c.id,
                'make': c.make,
                'model': c.model,
                'avg_rating': avg_rating
            })
        return JsonResponse(response_data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body.decode("utf-8"))
        for atr in ['make', 'model']:
            if not atr in request_data:
                message = 'The request is missing an attribute: {}'.format(atr)
                details = atr
                return JsonResponse({'message': message, 'details': details}, status=400)
        make = request_data.get('make')
        model = request_data.get('model')
        validation_response = self.__validate_make_and_model(make, model)
        if validation_response:
            return validation_response
        car_data = {
            'make': make,
            'model': model
        }
        c = Car(**car_data)
        c.save()
        return JsonResponse({'id': c.id}, status=201)

    # Argument 'make' is case-insesitive
    # Argument 'model' is case-sensitive
    # Returns None on success and JsonResponse on failure
    def __validate_make_and_model(self, make, model):
        message = ''
        details = ''
        url = 'http://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{}'.format(
            make)
        params = {
            'format': 'json'
        }
        r = requests.get(url, params)
        if r.status_code == 200:
            is_make_valid = False
            try:
                data = r.json()
                for res in data['Results']:
                    if res['Make_Name'].lower() != make.lower():
                        continue
                    is_make_valid = True
                    if res['Model_Name'] != model:
                        continue
                    return None
            except Exception as e:
                message = 'Failed to decode vehicle data'
                details = str(e)
            if is_make_valid:
                message = 'The model does not exist'
                details = model
            else:
                message = 'The make does not exist'
                details = make
        else:
            message = 'Failed to fetch vehicle data'
            details = r.text
        return JsonResponse({'message': message, 'details': details}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CarsSingle(View):
    def delete(self, request, *args, **kwargs):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class Rate(View):
    def post(self, request, *args, **kwargs):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class Popular(View):
    def get(self, request, *args, **kwargs):
        pass

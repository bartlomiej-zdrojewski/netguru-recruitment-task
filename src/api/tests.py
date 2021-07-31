import json
from django.test import TestCase
from django.urls import reverse
from .models import Car


class CarsViewTest(TestCase):

    __correct_make = 'Volkswagen'
    __correct_model = 'Golf'
    __incorrect_make = 'Wolkswagen'
    __incorrect_model = 'GolF'
    __correct_makes_and_models = [
        (__correct_make, __correct_model),
        ('Honda', 'Civic'),
        ('BMW', '533i')
    ]

    def __make_get_request(self):
        return self.client.get(reverse("api:cars"))

    def __make_post_request(self, make, model):
        data = {}
        if make:
            data['make'] = make
        if model:
            data['model'] = model
        return self.client.post(
            reverse("api:cars"),
            json.dumps(data),
            content_type="application/json")

    def __assertCarCreated(self, response, make, model):
        self.assertEqual(response.status_code, 201)
        response_id = json.loads(response.content.decode("utf-8")).get('id')
        self.assertIsNotNone(response_id)
        car_set = Car.objects.filter(id=response_id)
        self.assertQuerysetEqual(car_set, [Car(response_id, make, model)])

    def __assertError(self, response, status_code, detail):
        self.assertEqual(response.status_code, status_code)
        response_detail = json.loads(
            response.content.decode("utf-8")).get('details')
        self.assertIsNotNone(response_detail)
        self.assertEqual(response_detail, detail)

    def test_list_cars(self):
        car_set = []
        for mkmd in self.__correct_makes_and_models:
            response = self.__make_post_request(mkmd[0], mkmd[1])
            response_id = json.loads(
                response.content.decode("utf-8")).get('id')
            self.assertIsNotNone(response_id)
            car_set.append({
                'id': response_id,
                'make': mkmd[0],
                'model': mkmd[1]
            })
        response = self.__make_get_request()
        response_data = json.loads(response.content.decode("utf-8"))
        for car in car_set:
            is_present = False
            for res in response_data:
                if res['id'] == car['id']:
                    self.assertIn('make', res)
                    self.assertIn('model', res)
                    self.assertIn('avg_rating', res)
                    self.assertEqual(res.get('make'), car.get('make'))
                    self.assertEqual(res.get('model'), car.get('model'))
                    is_present = True
            self.assertTrue(is_present)

    def test_create_car(self):
        make = self.__correct_make
        model = self.__correct_model
        response = self.__make_post_request(make, model)
        self.__assertCarCreated(response, make, model)

    def test_create_car_duplicate(self):
        make = self.__correct_make
        model = self.__correct_model
        responses = []
        for _ in range(2):
            responses.append(self.__make_post_request(make, model))
        for response in responses:
            self.__assertCarCreated(response, make, model)

    def test_create_car_no_make_attribute(self):
        make = None
        model = self.__correct_model
        response = self.__make_post_request(make, model)
        self.__assertError(response, 400, 'make')

    def test_create_car_no_model_attribute(self):
        make = self.__correct_make
        model = None
        response = self.__make_post_request(make, model)
        self.assertEqual(response.status_code, 400)
        self.__assertError(response, 400, 'model')

    def test_create_car_make_does_not_exist(self):
        make = self.__incorrect_make
        model = self.__correct_model
        response = self.__make_post_request(make, model)
        self.__assertError(response, 404, make)

    def test_create_car_model_does_not_exist(self):
        make = self.__correct_make
        model = self.__incorrect_model
        response = self.__make_post_request(make, model)
        self.__assertError(response, 404, model)

    def test_create_car_lowercase_make(self):
        make = self.__correct_make.lower()
        model = self.__correct_model
        response = self.__make_post_request(make, model)
        self.__assertCarCreated(response, make, model)

    def test_create_car_lowercase_model(self):
        make = self.__correct_make
        model = self.__correct_model.lower()
        response = self.__make_post_request(make, model)
        self.__assertError(response, 404, model)


class CarsUpdateViewTest(TestCase):
    pass


class RateViewTest(TestCase):
    pass


class PopularViewTest(TestCase):
    pass

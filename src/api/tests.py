import json
from django.test import TestCase
from django.urls import reverse
from .models import Car


class CarBasedViewTest(TestCase):

    correct_make = 'Volkswagen'
    correct_model = 'Golf'
    incorrect_make = 'Wolkswagen'
    incorrect_model = 'GolF'
    correct_make_and_model_set = [
        (correct_make, correct_model),
        ('Honda', 'Civic'),
        ('BMW', '533i')
    ]

    def make_get_request(self):
        return self.client.get(reverse("api:cars"))

    def make_post_request(self, make, model):
        data = {}
        if make:
            data['make'] = make
        if model:
            data['model'] = model
        return self.client.post(
            reverse("api:cars"),
            json.dumps(data),
            content_type="application/json")

    def make_delete_request(self, id):
        return self.client.delete(reverse("api:cars_update", kwargs={'car_id': id}))

    def assertCarCreated(self, response, make, model):
        self.assertEqual(response.status_code, 201)
        response_id = json.loads(response.content.decode("utf-8")).get('id')
        self.assertIsNotNone(response_id)
        car_set = Car.objects.filter(id=response_id)
        self.assertQuerysetEqual(car_set, [Car(response_id, make, model)])

    def assertError(self, response, status_code, detail=None):
        self.assertEqual(response.status_code, status_code)
        response_detail = json.loads(
            response.content.decode("utf-8")).get('details')
        if detail:
            self.assertEqual(response_detail, detail)


class CarsViewTest(CarBasedViewTest):

    def test_list_cars(self):
        car_set = []
        for mkmd in self.correct_make_and_model_set:
            response = self.make_post_request(mkmd[0], mkmd[1])
            response_id = json.loads(
                response.content.decode("utf-8")).get('id')
            self.assertIsNotNone(response_id)
            car_set.append({
                'id': response_id,
                'make': mkmd[0],
                'model': mkmd[1]
            })
        response = self.make_get_request()
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
        make = self.correct_make
        model = self.correct_model
        response = self.make_post_request(make, model)
        self.assertCarCreated(response, make, model)

    def test_create_car_duplicate(self):
        make = self.correct_make
        model = self.correct_model
        responses = []
        for _ in range(2):
            responses.append(self.make_post_request(make, model))
        for response in responses:
            self.assertCarCreated(response, make, model)

    def test_create_car_no_make_attribute(self):
        make = None
        model = self.correct_model
        response = self.make_post_request(make, model)
        self.assertError(response, 400, 'make')

    def test_create_car_no_model_attribute(self):
        make = self.correct_make
        model = None
        response = self.make_post_request(make, model)
        self.assertEqual(response.status_code, 400)
        self.assertError(response, 400, 'model')

    def test_create_car_make_does_not_exist(self):
        make = self.incorrect_make
        model = self.correct_model
        response = self.make_post_request(make, model)
        self.assertError(response, 404, make)

    def test_create_car_model_does_not_exist(self):
        make = self.correct_make
        model = self.incorrect_model
        response = self.make_post_request(make, model)
        self.assertError(response, 404, model)

    def test_create_car_lowercase_make(self):
        make = self.correct_make.lower()
        model = self.correct_model
        response = self.make_post_request(make, model)
        self.assertCarCreated(response, make, model)

    def test_create_car_lowercase_model(self):
        make = self.correct_make
        model = self.correct_model.lower()
        response = self.make_post_request(make, model)
        self.assertError(response, 404, model)


class CarsUpdateViewTest(CarBasedViewTest):

    def test_delete_car(self):
        make = self.correct_make
        model = self.correct_model
        response = self.make_post_request(make, model)
        self.assertCarCreated(response, make, model)
        response_id = json.loads(response.content.decode("utf-8")).get('id')
        self.assertIsNotNone(response_id)
        response = self.make_delete_request(response_id)
        self.assertEqual(response.status_code, 200)
        car_set = Car.objects.filter(id=response_id)
        self.assertQuerysetEqual(car_set, [])

    def test_delete_car_car_does_not_exist(self):
        id = 0
        response = self.make_delete_request(id)
        self.assertError(response, 404, id)


class RateViewTest(TestCase):

    def test_create_rating(self):
        pass

    def test_create_rating_multiple(self):
        pass

    def test_create_rating_car_does_not_exist(self):
        pass

    def test_create_rating_string_value(self):
        pass

    def test_create_rating_too_low(self):
        pass

    def test_create_rating_too_high(self):
        pass


class PopularViewTest(TestCase):
    pass

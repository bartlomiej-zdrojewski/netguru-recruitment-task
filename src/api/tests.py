import json
import random
from django.test import TestCase
from django.urls import reverse
from .models import Car, Rating


class CustomTestCase(TestCase):

    def assertErrorResponse(self, response, status_code, details=None):
        self.assertEqual(response.status_code, status_code)
        response_details = json.loads(
            response.content.decode("utf-8")).get('details')
        if details:
            self.assertEqual(response_details, details)


class CarsViewTest(CustomTestCase):

    __correct_make = 'Volkswagen'
    __correct_model = 'Golf'
    __incorrect_make = 'Wolkswagen'
    __incorrect_model = 'GolF'
    __correct_make_and_model_set = [
        (__correct_make, __correct_model),
        ('Honda', 'Civic'),
        ('BMW', '533i')
    ]

    def __make_list_cars_request(self):
        return self.client.get(reverse("api:cars"))

    def __make_create_car_request(self, make, model):
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
        self.assertQuerysetEqual(
            car_set,
            [Car(id=response_id, make=make, model=model)]
        )

    def test_list_cars(self):
        response = self.__make_list_cars_request()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertIsNotNone(response_data)

    def test_create_car(self):
        make = self.__correct_make
        model = self.__correct_model
        response = self.__make_create_car_request(make, model)
        self.__assertCarCreated(response, make, model)

    def test_create_car_duplicate(self):
        make = self.__correct_make
        model = self.__correct_model
        responses = []
        for _ in range(2):
            responses.append(self.__make_create_car_request(make, model))
        for response in responses:
            self.__assertCarCreated(response, make, model)

    def test_create_car_make_attribute_missing(self):
        make = None
        model = self.__correct_model
        response = self.__make_create_car_request(make, model)
        self.assertErrorResponse(response, 400, 'make')

    def test_create_car_model_attribute_missing(self):
        make = self.__correct_make
        model = None
        response = self.__make_create_car_request(make, model)
        self.assertEqual(response.status_code, 400)
        self.assertErrorResponse(response, 400, 'model')

    def test_create_car_make_does_not_exist(self):
        make = self.__incorrect_make
        model = self.__correct_model
        response = self.__make_create_car_request(make, model)
        self.assertErrorResponse(response, 404, make)

    def test_create_car_model_does_not_exist(self):
        make = self.__correct_make
        model = self.__incorrect_model
        response = self.__make_create_car_request(make, model)
        self.assertErrorResponse(response, 404, model)

    def test_create_car_lowercase_make(self):
        make = self.__correct_make.lower()
        model = self.__correct_model
        response = self.__make_create_car_request(make, model)
        self.__assertCarCreated(response, make, model)

    def test_create_car_lowercase_model(self):
        make = self.__correct_make
        model = self.__correct_model.lower()
        response = self.__make_create_car_request(make, model)
        self.assertErrorResponse(response, 404, model)

    def test_create_car_and_then_list_cars(self):
        car_set = []
        for mkmd in self.__correct_make_and_model_set:
            response = self.__make_create_car_request(mkmd[0], mkmd[1])
            response_id = json.loads(
                response.content.decode("utf-8")).get('id')
            self.assertIsNotNone(response_id)
            car_set.append({
                'id': response_id,
                'make': mkmd[0],
                'model': mkmd[1]
            })
        response = self.__make_list_cars_request()
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


class CarsUpdateViewTest(CustomTestCase):

    __correct_make = 'Volkswagen'
    __correct_model = 'Golf'

    def __make_delete_car_request(self, id):
        return self.client.delete(
            reverse("api:cars_update", kwargs={'car_id': id}))

    def test_delete_car(self):
        make = self.__correct_make
        model = self.__correct_model
        car = Car.objects.create(make=make, model=model)
        response = self.__make_delete_car_request(car.id)
        self.assertEqual(response.status_code, 200)
        car_set = Car.objects.filter(id=car.id)
        self.assertQuerysetEqual(car_set, [])

    def test_delete_car_car_does_not_exist(self):
        id = 0
        response = self.__make_delete_car_request(id)
        self.assertErrorResponse(response, 404, id)


class RateViewTest(CustomTestCase):

    __correct_make = 'Volkswagen'
    __correct_model = 'Golf'

    def __create_car(self):
        return Car.objects.create(
            make=self.__correct_make,
            model=self.__correct_model)

    def __list_cars(self):
        response = self.client.get(reverse("api:cars"))
        return json.loads(response.content.decode("utf-8"))

    def __make_create_rating_request(self, car, rating):
        data = {}
        if car:
            data['car_id'] = car.id
        if rating:
            data['rating'] = rating
        return self.client.post(
            reverse("api:rate"),
            json.dumps(data),
            content_type="application/json")

    def __assertRatingCreated(self, response, car, raiting):
        self.assertEqual(response.status_code, 201)
        response_id = json.loads(response.content.decode("utf-8")).get('id')
        self.assertIsNotNone(response_id)
        rating_set = Rating.objects.filter(id=response_id)
        self.assertQuerysetEqual(
            rating_set,
            [Rating(id=response_id, value=raiting, car=car)]
        )

    def test_create_rating(self):
        car = self.__create_car()
        rating = 5
        response = self.__make_create_rating_request(car, rating)
        self.__assertRatingCreated(response, car, rating)

    def test_create_rating_car_id_attribute_missing(self):
        car = None
        rating = 5
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 400, 'car_id')

    def test_create_rating_rating_attribute_missing(self):
        car = self.__create_car()
        rating = None
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 400, 'rating')

    def test_create_rating_car_does_not_exist(self):
        car = self.__create_car()
        rating = 5
        car.delete()
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 404, car.id)

    def test_create_rating_string_value(self):
        car = self.__create_car()
        rating = '5'
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 400, rating)

    def test_create_rating_value_too_low(self):
        car = self.__create_car()
        rating = 0.99
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 400, rating)

    def test_create_rating_value_too_high(self):
        car = self.__create_car()
        rating = 5.01
        response = self.__make_create_rating_request(car, rating)
        self.assertErrorResponse(response, 400, rating)

    def test_create_rating_and_then_list_cars_correct_average_ratings(self):
        base_car = self.__create_car()
        ratings = [1, 2, 2.25, 3, 3.5, 4, 4.75, 5]
        avg_rating = sum(ratings) / len(ratings)
        for rtn in ratings:
            response = self.__make_create_rating_request(base_car, rtn)
            self.__assertRatingCreated(response, base_car, rtn)
        car_list = self.__list_cars()
        self.assertTrue(len(car_list) > 0)
        for car in car_list:
            self.assertIn('id', car)
            if car['id'] == base_car.id:
                self.assertIn('avg_rating', car)
                self.assertAlmostEqual(car['avg_rating'], avg_rating)
                return
        self.fail('The car is not present in the car list')


class PopularViewTest(CustomTestCase):

    __correct_make_and_model_set = [
        ('Volkswagen', 'Golf'),
        ('Honda', 'Civic'),
        ('BMW', '533i')
    ]

    def __create_car(self, make, model):
        return Car.objects.create(
            make=make,
            model=model
        )

    def __create_rating(self, value, car):
        return Rating.objects.create(
            value=value,
            car=car
        )

    def __create_car_rates_number_set(self, seed):
        car_rates_number_set = []
        generator = random.Random()
        generator.seed(seed)
        for mkmd in self.__correct_make_and_model_set:
            car_rates_number_set.append({
                'car': self.__create_car(mkmd[0], mkmd[1]),
                'rates_number': 0
            })
        for i in range(len(car_rates_number_set)):
            rates_number = generator.randrange(10, 100)
            for _ in range(rates_number):
                value = 5.0 * generator.random()
                car = car_rates_number_set[i]['car']
                self.__create_rating(value, car)
                car_rates_number_set[i]['rates_number'] += 1
        return car_rates_number_set

    def __make_list_popular_cars_request(self, count=None):
        params = {}
        if count != None:
            params['count'] = count
        return self.client.get(reverse("api:popular"), params)

    def test_list_popular_cars(self):
        response = self.__make_list_popular_cars_request()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertIsNotNone(response_data)

    def test_list_popular_cars_count_set(self):
        self.__create_car_rates_number_set(12)
        for count in [0, 1, 2, 10]:
            response = self.__make_list_popular_cars_request(count)
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.content.decode("utf-8"))
            self.assertIsNotNone(response_data)
            self.assertTrue(len(response_data) <= count)

    def test_list_popular_cars_invalid_count_set(self):
        self.__create_car_rates_number_set(34)
        base_response = self.__make_list_popular_cars_request()
        self.assertEqual(base_response.status_code, 200)
        base_response_data = json.loads(base_response.content.decode("utf-8"))
        self.assertIsNotNone(base_response_data)
        base_count = len(base_response_data)
        self.assertTrue(base_count > 0)
        for count in [-1, 'a']:
            response = self.__make_list_popular_cars_request(count)
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.content.decode("utf-8"))
            self.assertIsNotNone(response_data)
            self.assertEqual(len(response_data), base_count)

    def test_list_popular_cars_correct_rates_numbers(self):
        car_rates_number_set = self.__create_car_rates_number_set(56)
        response = self.__make_list_popular_cars_request()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertIsNotNone(response_data)
        self.assertTrue(len(response_data) >= len(car_rates_number_set))
        for crn in car_rates_number_set:
            is_present = False
            for res in response_data:
                if res['id'] == crn['car'].id:
                    self.assertEqual(res['rates_number'], crn['rates_number'])
                    is_present = True
            self.assertTrue(is_present)

    def test_list_popular_cars_correct_order(self):
        car_rates_number_set = self.__create_car_rates_number_set(78)
        response = self.__make_list_popular_cars_request()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertIsNotNone(response_data)
        self.assertTrue(len(response_data) >= len(car_rates_number_set))
        last_rates_number = -1
        for res in response_data:
            self.assertIn('id', res)
            self.assertIn('make', res)
            self.assertIn('model', res)
            self.assertIn('rates_number', res)
            if last_rates_number >= 0:
                self.assertTrue(last_rates_number >= res['rates_number'])
            last_rates_number = res['rates_number']

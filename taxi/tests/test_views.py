from django.test import TestCase
from django.urls import reverse

from django.test import RequestFactory, TestCase
from taxi.templatetags.query_transform import query_transform

DRIVER_LIST = reverse("taxi:driver-list")
CAR_LIST = reverse("taxi:car-list")
MANUFACTURER_LIST = reverse("taxi:manufacturer-list")

class QueryTransformTagTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add_new_param(self):
        """Добавление нового query параметра"""
        request = self.factory.get("/?page=1")
        result = query_transform(request, search="john")
        self.assertIn("page=1", result)
        self.assertIn("search=john", result)

    def test_update_existing_param(self):
        """Обновление существующего параметра"""
        request = self.factory.get("/?page=1")
        result = query_transform(request, page=2)
        self.assertEqual(result, "page=2")

    def test_remove_param_when_none(self):
        """Удаление параметра, если значение None"""
        request = self.factory.get("/?page=1&search=test")
        result = query_transform(request, search=None)
        # search удалён, остался только page
        self.assertEqual(result, "page=1")

    def test_multiple_changes(self):
        """Одновременное добавление и удаление"""
        request = self.factory.get("/?page=3&filter=active")
        result = query_transform(request, page=None, sort="name")
        # page удалён, filter остался, sort добавлен
        self.assertIn("filter=active", result)
        self.assertIn("sort=name", result)
        self.assertNotIn("page=", result)


class PrivateDriverFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormat(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST)
        self.assertNotEqual(res.status_code, 200)

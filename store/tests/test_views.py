from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from store.models import Category, Product
from django.contrib.auth.models import User
from store.views import home


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        category = Category.objects.create(name='dajgno', slug='django')
        user = User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners',
                                            created_by_id=1, slug='django-beginners', price='20.00', image='django')

    def test_homepage_url(self):
        response = self.c.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_product_details_url(self):
        response = self.c.get(
            reverse('store:product_details', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_list_url(self):
        response = self.c.get(
            reverse('store:category_details', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/item/django-beginners')
        response = home(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

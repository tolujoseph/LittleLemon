from django.test import TestCase
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer

class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(name="IceCream", price=80, menu_item_description="Vanilla ice cream")
        Menu.objects.create(name="Pasta", price=120, menu_item_description="Creamy pasta")
        Menu.objects.create(name="Burger", price=100, menu_item_description="Beef burger")

    def test_getall(self):
        response = self.client.get('/restaurant/menu/items')
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
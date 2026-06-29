from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from restaurant.models import Menu


class MenuItemsViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_token = Token.objects.create(user=self.user)
        self.manager = User.objects.create_user(username='manager', password='managerpass123', is_staff=True)
        self.manager_token = Token.objects.create(user=self.manager)
        self.item1 = Menu.objects.create(name='IceCream', price=80, menu_item_description='Vanilla ice cream')
        self.item2 = Menu.objects.create(name='Pasta', price=120, menu_item_description='Creamy pasta')

    def test_get_all_menu_items_unauthenticated(self):
        """Anyone can view menu items"""
        response = self.client.get('/restaurant/menu/items')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_menu_items_authenticated(self):
        """Authenticated users can view menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get('/restaurant/menu/items')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_menu_item(self):
        """Anyone can view a single menu item"""
        response = self.client.get(f'/restaurant/menu/items/{self.item1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'IceCream')

    def test_get_nonexistent_menu_item_returns_404(self):
        """Requesting a non-existent item returns 404"""
        response = self.client.get('/restaurant/menu/items/9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_menu_item_as_manager(self):
        """Managers can create menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        data = {'name': 'Burger', 'price': '100.00', 'menu_item_description': 'Beef burger'}
        response = self.client.post('/restaurant/menu/items', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)

    def test_create_menu_item_as_regular_user_forbidden(self):
        """Regular users cannot create menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {'name': 'Burger', 'price': '100.00', 'menu_item_description': 'Beef burger'}
        response = self.client.post('/restaurant/menu/items', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_unauthenticated(self):
        """Unauthenticated users get 401"""
        data = {'name': 'Burger', 'price': '100.00', 'menu_item_description': 'Beef burger'}
        response = self.client.post('/restaurant/menu/items', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu_item_as_manager(self):
        """Managers can update menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        data = {'name': 'Updated IceCream', 'price': '90.00', 'menu_item_description': 'Updated description'}
        response = self.client.put(f'/restaurant/menu/items/{self.item1.pk}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, 'Updated IceCream')

    def test_partial_update_menu_item_as_manager(self):
        """Managers can partially update menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.patch(f'/restaurant/menu/items/{self.item1.pk}', {'price': '95.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.price, 95.00)

    def test_update_menu_item_as_regular_user_forbidden(self):
        """Regular users cannot update menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {'name': 'Hacked', 'price': '1.00', 'menu_item_description': 'Hacked'}
        response = self.client.put(f'/restaurant/menu/items/{self.item1.pk}', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_menu_item_as_manager(self):
        """Managers can delete menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.delete(f'/restaurant/menu/items/{self.item1.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)

    def test_delete_menu_item_as_regular_user_forbidden(self):
        """Regular users cannot delete menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.delete(f'/restaurant/menu/items/{self.item1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_missing_required_field(self):
        """Creating a menu item without required fields returns 400"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post('/restaurant/menu/items', {'name': 'Incomplete'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_menu_item_str_representation(self):
        """Menu model __str__ returns item name"""
        self.assertEqual(str(self.item1), 'IceCream')

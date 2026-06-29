from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from restaurant.models import Booking
from datetime import datetime


class BookingViewSetTest(APITestCase):

    def setUp(self):
        # Regular user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_token = Token.objects.create(user=self.user)

        # Second user
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.user2_token = Token.objects.create(user=self.user2)

        # Manager
        self.manager = User.objects.create_user(username='manager', password='managerpass123', is_staff=True)
        self.manager_token = Token.objects.create(user=self.manager)

        # Sample booking
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=4,
            booking_date=datetime(2026, 8, 15, 19, 0, 0)
        )

    def test_get_all_bookings_authenticated(self):
        """Authenticated users can view all bookings"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get('/restaurant/booking/tables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_all_bookings_unauthenticated(self):
        """Unauthenticated users cannot view bookings"""
        response = self.client.get('/restaurant/booking/tables/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_authenticated(self):
        """Authenticated users can create a booking"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {
            'name': 'Jane Doe',
            'no_of_guests': 2,
            'booking_date': '2026-09-01T18:00:00Z'
        }
        response = self.client.post('/restaurant/booking/tables/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_booking_unauthenticated(self):
        """Unauthenticated users cannot create a booking"""
        data = {
            'name': 'Jane Doe',
            'no_of_guests': 2,
            'booking_date': '2026-09-01T18:00:00Z'
        }
        response = self.client.post('/restaurant/booking/tables/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_booking_authenticated(self):
        """Authenticated users can view a single booking"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(f'/restaurant/booking/tables/{self.booking.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_update_booking_authenticated(self):
        """Authenticated users can update a booking"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {
            'name': 'John Updated',
            'no_of_guests': 6,
            'booking_date': '2026-08-15T19:00:00Z'
        }
        response = self.client.put(f'/restaurant/booking/tables/{self.booking.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, 'John Updated')

    def test_delete_booking_authenticated(self):
        """Authenticated users can delete a booking"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.delete(f'/restaurant/booking/tables/{self.booking.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

    def test_create_booking_missing_required_field(self):
        """Creating a booking without required fields returns 400"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post('/restaurant/booking/tables/', {'name': 'Incomplete'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_str_representation(self):
        """Booking model __str__ returns booking name"""
        self.assertEqual(str(self.booking), 'John Doe')

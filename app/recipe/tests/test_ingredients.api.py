from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from ..serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientApiTest(TestCase):
    """ Test the publicly available ingredients API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test the login is required to access the endpoint """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """ Test ingredients can be retrieve by authorized user """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients_list(self):
        """ Test retrieving a list of ingredients """
        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """
        Test that only ingredients for the authenticated user are returned 
        """
        user2 = get_user_model().objects.create_user(
            email="test2@test.com",
            password="test2pass"
        )
        ingredient = Ingredient.objects.create(user=self.user, name="Vinegar")
        Ingredient.objects.create(user=user2, name="Tumeric")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredient_successful(self):
        """ Test create a new ingredient """
        payload = {'name': "Cabbage"}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ Test creating invalid ingredient fails """
        payload = {"name": ""}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

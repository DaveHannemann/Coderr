from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import UserProfile


class ProfileCheckViewTests(APITestCase):
    def test_returns_single_profile_in_expected_shape(self):
        user = User.objects.create_user(
            username="max_mustermann",
            email="max@business.de",
            password="secret123",
        )
        UserProfile.objects.create(user=user, type="business")
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.get(f"/api/profile/{user.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"], user.id)
        self.assertEqual(response.data["username"], "max_mustermann")
        self.assertEqual(response.data["first_name"], "")
        self.assertEqual(response.data["last_name"], "")
        self.assertEqual(response.data["file"], "")
        self.assertEqual(response.data["location"], "")
        self.assertEqual(response.data["tel"], "")
        self.assertEqual(response.data["description"], "")
        self.assertEqual(response.data["working_hours"], "")
        self.assertEqual(response.data["type"], "business")
        self.assertEqual(response.data["email"], "max@business.de")
        self.assertIn("created_at", response.data)

    def test_patch_updates_profile_and_user_fields(self):
        user = User.objects.create_user(
            username="max_mustermann",
            email="max@business.de",
            password="secret123",
        )
        UserProfile.objects.create(user=user, type="business")
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.patch(
            f"/api/profile/{user.id}/",
            {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Berlin",
                "tel": "+49123456789",
                "description": "Ich baue Webprojekte.",
                "working_hours": "Mo-Fr 09:00-17:00",
                "email": "max_new@business.de",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Max")
        self.assertEqual(response.data["last_name"], "Mustermann")
        self.assertEqual(response.data["location"], "Berlin")
        self.assertEqual(response.data["tel"], "+49123456789")
        self.assertEqual(response.data["description"], "Ich baue Webprojekte.")
        self.assertEqual(response.data["working_hours"], "Mo-Fr 09:00-17:00")
        self.assertEqual(response.data["email"], "max_new@business.de")

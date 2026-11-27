"""
FaceStyle AI - Automated Unit Test Suite
Covers:
- User registration and authentication
- Face shape geometric classification
- Hairstyle recommendation filters
- Favourites management
- Security and unauthorized access protection
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import UserProfile, Hairstyle, FaceAnalysis, FavouriteHairstyle
from ai_engine.measurements import calculate_face_measurements, classify_face_shape


class FaceShapeClassificationTests(TestCase):
    """Verifies that mathematical geometric classification rules produce expected archetypes."""

    def test_oval_face_classification(self):
        """Oval: L/W between 1.30 and 1.48, forehead wider than jaw, smooth curves."""
        measurements = {
            'face_length': 360.0,
            'cheekbone_width': 260.0,
            'forehead_width': 240.0,
            'jaw_width': 200.0,
            'length_to_width_ratio': 1.385,
            'forehead_to_jaw_ratio': 1.20,
            'cheek_to_jaw_ratio': 1.30,
            'forehead_to_cheek_ratio': 0.92,
        }
        res = classify_face_shape(measurements)
        self.assertIn(res['face_shape'], ['Oval', 'Heart'])
        self.assertGreaterEqual(res['confidence'], 75.0)

    def test_round_face_classification(self):
        """Round: L/W < 1.30, cheekbones widest, soft jaw."""
        measurements = {
            'face_length': 280.0,
            'cheekbone_width': 270.0,
            'forehead_width': 220.0,
            'jaw_width': 210.0,
            'length_to_width_ratio': 1.037,
            'forehead_to_jaw_ratio': 1.047,
            'cheek_to_jaw_ratio': 1.285,
            'forehead_to_cheek_ratio': 0.814,
        }
        res = classify_face_shape(measurements)
        self.assertIn(res['face_shape'], ['Round', 'Square'])

    def test_oblong_face_classification(self):
        """Oblong: L/W > 1.48, long vertical lines."""
        measurements = {
            'face_length': 400.0,
            'cheekbone_width': 240.0,
            'forehead_width': 230.0,
            'jaw_width': 220.0,
            'length_to_width_ratio': 1.667,
            'forehead_to_jaw_ratio': 1.045,
            'cheek_to_jaw_ratio': 1.09,
            'forehead_to_cheek_ratio': 0.958,
        }
        res = classify_face_shape(measurements)
        self.assertEqual(res['face_shape'], 'Oblong')

    def test_heart_face_classification(self):
        """Heart: Forehead significantly wider than jaw (F/J > 1.25)."""
        measurements = {
            'face_length': 340.0,
            'cheekbone_width': 250.0,
            'forehead_width': 260.0,
            'jaw_width': 180.0,
            'length_to_width_ratio': 1.36,
            'forehead_to_jaw_ratio': 1.444,
            'cheek_to_jaw_ratio': 1.388,
            'forehead_to_cheek_ratio': 1.04,
        }
        res = classify_face_shape(measurements)
        self.assertEqual(res['face_shape'], 'Heart')


class UserAuthenticationTests(TestCase):
    """Tests registration, login validation, and profile creation."""

    def setUp(self):
        self.client = Client()

    def test_user_registration_success(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Aarav',
            'last_name': 'Sharma',
            'username': 'aaravs',
            'email': 'aarav@example.com',
            'password': 'StrongPassword123',
            'confirm_password': 'StrongPassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='aaravs').exists())
        user = User.objects.get(username='aaravs')
        # Check profile auto-created via signal
        self.assertTrue(hasattr(user, 'profile'))

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Rohan',
            'last_name': 'Verma',
            'username': 'rohanv',
            'email': 'rohan@example.com',
            'password': 'PasswordOne123',
            'confirm_password': 'PasswordTwo999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='rohanv').exists())

    def test_user_login_and_logout(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='ValidPassword123')
        
        # Test username login
        login_res = self.client.post(reverse('login'), {
            'username_or_email': 'testuser',
            'password': 'ValidPassword123'
        })
        self.assertEqual(login_res.status_code, 302)

        # Test logout
        logout_res = self.client.get(reverse('logout'))
        self.assertEqual(logout_res.status_code, 302)


class HairstyleAndFavouritesTests(TestCase):
    """Tests Hairstyle catalog queries and user bookmarking."""

    def setUp(self):
        self.user = User.objects.create_user(username='styledude', password='Password123')
        self.client = Client()
        self.client.login(username='styledude', password='Password123')

        self.style = Hairstyle.objects.create(
            name='Modern Textured Quiff',
            gender='Male',
            hair_length='Short',
            hair_type='Wavy',
            category='Modern',
            face_shapes='Round, Oval, Square',
            description='Voluminous quiff cut.',
            styling_tips='Blow dry up and apply matte paste.'
        )

    def test_hairstyle_face_shape_compatibility(self):
        self.assertTrue(self.style.is_compatible_with('Round'))
        self.assertTrue(self.style.is_compatible_with('Oval'))
        self.assertFalse(self.style.is_compatible_with('Oblong'))

    def test_toggle_favourite(self):
        # Add to favourites
        res = self.client.get(reverse('toggle_favourite', args=[self.style.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(FavouriteHairstyle.objects.filter(user=self.user, hairstyle=self.style).exists())

        # Toggle to remove
        res2 = self.client.get(reverse('toggle_favourite', args=[self.style.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res2.status_code, 200)
        self.assertFalse(FavouriteHairstyle.objects.filter(user=self.user, hairstyle=self.style).exists())


class SecurityAndAccessTests(TestCase):
    """Tests route protections and privacy restrictions."""

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='Password123')
        self.user2 = User.objects.create_user(username='user2', password='Password123')
        self.client = Client()

        self.analysis = FaceAnalysis.objects.create(
            user=self.user1,
            detected_face_shape='Oval',
            confidence=88.5
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_unauthorized_user_cannot_view_others_private_record(self):
        # Login as user2 and attempt to view user1's analysis
        self.client.login(username='user2', password='Password123')
        response = self.client.get(reverse('result', args=[self.analysis.id]))
        self.assertEqual(response.status_code, 403)

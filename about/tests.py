from django.test import TestCase
from django.urls import reverse
from .models import About, TeamMember

class AboutPageTestCase(TestCase):

    def setUp(self):
        # Create an About object
        self.about = About.objects.create(title="About Us", content="Some content about us.")


        TeamMember.objects.create(about=self.about, name="John Doe", role="Developer", bio="John's bio")
        TeamMember.objects.create(about=self.about, name="Jane Doe", role="Designer", bio="Jane's bio")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')
        self.assertEqual(response.context['about'], self.about)


        team_members = response.context['about'].team_members.all()
        self.assertEqual(team_members.count(), 2)
        self.assertEqual(team_members[0].name, "John Doe")
        self.assertEqual(team_members[1].name, "Jane Doe")

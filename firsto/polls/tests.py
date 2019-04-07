import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_w_old_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_w_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in future
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_w_recent_question(self):
        """
        was_published_recently() returns True for questions whose
        pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question and published the number of days offset to now,
    negative for questions published in the past and positive otherwise
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available!")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        """
        Questions with pub_date in the past are displayed
        """
        create_question("Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with pub_date in the future aren't displayed
        """
        create_question(question_text="Future question?", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available!")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_future_and_past_question(self):
        """
        When both past and future questions exist, only past are displayed
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        Display past questions even when multiple exists
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewtests(TestCase):
    def test_future_question(self):
        """
        Detail view of a question with future pub_date returns 404
        """
        future_question = create_question(question_text="Future Ques", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Detail view of question with past pub_date display question's test
        """
        past_question = create_question(question_text="Past Ques", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

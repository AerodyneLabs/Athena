from datetime import datetime
from django.test import TestCase

import atmosphere.tasks.nomads as nomads

class NOMADSTestCase(TestCase):

    def test_previous_model(self):
        t = datetime(2015, 7, 31, 5)
        self.assertEqual(nomads.previous_model(t), datetime(2015, 7, 31, 0))

    def test_conservative_previous_model(self):
        t = datetime(2015, 7, 31, 5)
        self.assertEqual(nomads.previous_model(t, conservative=True), datetime(2015, 7, 30, 18))

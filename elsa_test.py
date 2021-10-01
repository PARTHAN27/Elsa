"""This file is just for testing the components"""
import unittest

from talk1.talk1 import talk
from task1 import task

from Magic import indexer, theme, usernames, settings, history


class ElsaTest(unittest.TestCase):
    # def test<anyname>(self): should be the format for making a function to test
    def testindexfiles(self):
        self.assertIsNone(indexer.index_files())

    def testtheme(self):
        self.assertEqual(len(theme.read_theme()), 3)

    def testusernames(self):
        self.assertEqual(usernames.verify_usernames(), False)

    def testsettingspage(self):
        self.assertIsNone(settings.setting_page())

    def testtalk(self):
        self.assertIsNone(talk("Just testing the speech"))

    def testtasks(self):
        self.assertIsNone(task.tell_time())
        self.assertIsNone(task.greeting("admin"))

    def testuserfile(self):
        self.assertIsNone(history.user_file(" dummy", "testing", "testing"))


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()

    unittest.main()

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

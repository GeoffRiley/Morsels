from textwrap import dedent
import unittest

from bullets import parse_bullets


class ParseBulletsTests(unittest.TestCase):
    """Tests for parse_bullets."""
    def test_single_bullet_string_representation(self):
        bullets = parse_bullets("- Just one bullet")
        self.assertEqual(len(bullets), 1)
        self.assertEqual(str(bullets[0]), "- Just one bullet")

    def test_single_bullet(self):
        self.assertEqual(
            parse_bullets("- Just one bullet")[0].text,
            "Just one bullet",
        )

    def test_two_bullets(self):
        bullets = parse_bullets("- Do laundry\n- Clean kitchen")
        self.assertEqual(len(bullets), 2)
        self.assertEqual(str(bullets[0]), "- Do laundry")
        self.assertEqual(str(bullets[1]), "- Clean kitchen")
        self.assertEqual(bullets[0].text, "Do laundry")
        self.assertEqual(bullets[1].text, "Clean kitchen")

    def test_many_bullets_and_trailing_newline(self):
        bullets = parse_bullets(
            dedent("""
            - Do laundry
            - Write tests for new exercise
            - Write new Python Morsels emails
            - Fix Python Morsels login page bug
        """).lstrip('\n'))
        self.assertEqual(len(bullets), 4)
        self.assertEqual(str(bullets[0]), "- Do laundry")
        self.assertEqual(str(bullets[2]), "- Write new Python Morsels emails")
        self.assertEqual(bullets[1].text, "Write tests for new exercise")
        self.assertEqual(bullets[3].text, "Fix Python Morsels login page bug")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_nested_bullets(self):
        bullets = parse_bullets(
            dedent("""
            - Do laundry
            - Python Morsels
                - Write tests for new exercise
                - Fix Python Morsels login page bug
                    - Reproduce bug locally
                    - Write regression test
                    - Deploy fix
                        - Make PR for fix
                        - Code review
                        - Merge and deploy
                - Write new Python Morsels emails
            - Buy groceries
            - Training
                - Follow-up with new team training client
        """).lstrip('\n'))
        self.assertEqual(len(bullets), 4)
        self.assertEqual(
            [b.text for b in bullets],
            ["Do laundry", "Python Morsels", "Buy groceries", "Training"],
        )
        self.assertEqual(len(bullets[0].children), 0)
        self.assertEqual(len(bullets[2].children), 0)
        self.assertEqual(
            [b.text for b in bullets[1].children],
            [
                "Write tests for new exercise",
                "Fix Python Morsels login page bug",
                "Write new Python Morsels emails",
            ],
        )
        self.assertEqual(
            [b.text for b in bullets[3].children],
            ["Follow-up with new team training client"],
        )
        self.assertEqual(
            [b.text for b in bullets[1].children[1].children],
            [
                "Reproduce bug locally",
                "Write regression test",
                "Deploy fix",
            ],
        )
        self.assertEqual(
            [b.text for b in bullets[1].children[1].children[2].children],
            [
                "Make PR for fix",
                "Code review",
                "Merge and deploy",
            ],
        )
        self.assertEqual(
            [len(b.children) for b in bullets[1].children],
            [0, 3, 0],
        )
        self.assertEqual(len(bullets[3].children[0].children), 0)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_parent_attribute_and_nested_string_representation(self):
        bullets = parse_bullets(
            dedent("""
            - Do laundry
            - Python Morsels
                - Write tests for new exercise
                - Fix Python Morsels login page bug
                    - Reproduce bug locally
                    - Write regression test
                    - Deploy fix
                        - Make PR for fix
                        - Code review
                        - Merge and deploy
                - Write new Python Morsels emails
            - Buy groceries
            - Training
                - Follow-up with new team training client
        """).lstrip('\n'))

        # parent attributes
        for bullet in bullets:
            self.assertIsNone(bullet.parent)
            for child in bullet.children:
                self.assertIs(child.parent, bullet)
                for grandchild in child.children:
                    self.assertIs(grandchild.parent, child)
        greatgrandchildren = bullets[1].children[1].children[2].children
        for child in greatgrandchildren:
            self.assertIs(child.parent, bullets[1].children[1].children[2])

        # String representations
        self.assertEqual(str(bullets[0]), "- Do laundry")
        self.assertEqual(str(bullets[2]), "- Buy groceries")
        self.assertEqual(
            str(bullets[3]),
            dedent("""
            - Training
                - Follow-up with new team training client
        """).strip('\n'))
        self.assertEqual(
            str(bullets[1].children[1].children[2]),
            dedent("""
            - Deploy fix
                - Make PR for fix
                - Code review
                - Merge and deploy
        """).strip('\n'))
        self.assertEqual(
            str(bullets[1].children[1]),
            dedent("""
            - Fix Python Morsels login page bug
                - Reproduce bug locally
                - Write regression test
                - Deploy fix
                    - Make PR for fix
                    - Code review
                    - Merge and deploy
        """).strip('\n'))
        self.assertEqual(
            str(bullets[1]),
            dedent("""
            - Python Morsels
                - Write tests for new exercise
                - Fix Python Morsels login page bug
                    - Reproduce bug locally
                    - Write regression test
                    - Deploy fix
                        - Make PR for fix
                        - Code review
                        - Merge and deploy
                - Write new Python Morsels emails
        """).strip('\n'))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_bullet_list_string_representation_and_filtering(self):
        bullets = parse_bullets(
            dedent("""
            - Do laundry
            - Python Morsels
                - Write tests for new exercise
                - Fix Python Morsels login page bug
                    - Reproduce bug locally
                    - Write regression test
                    - Deploy fix
                        - Make PR for fix
                        - Code review
                        - Merge and deploy
                - Write new Python Morsels emails
            - Buy groceries
            - Python Training
                - Follow-up with new team training client
        """).lstrip('\n'))

        # string representation of bullet list
        self.assertEqual(
            str(bullets),
            dedent("""
            - Do laundry
            - Python Morsels
                - Write tests for new exercise
                - Fix Python Morsels login page bug
                    - Reproduce bug locally
                    - Write regression test
                    - Deploy fix
                        - Make PR for fix
                        - Code review
                        - Merge and deploy
                - Write new Python Morsels emails
            - Buy groceries
            - Python Training
                - Follow-up with new team training client
        """).strip('\n'))
        self.assertEqual(
            str(bullets[1].children),
            dedent("""
            - Write tests for new exercise
            - Fix Python Morsels login page bug
                - Reproduce bug locally
                - Write regression test
                - Deploy fix
                    - Make PR for fix
                    - Code review
                    - Merge and deploy
            - Write new Python Morsels emails
        """).strip('\n'))

        # filter method
        python_results = bullets.filter("python")
        self.assertEqual(python_results[0].text, "Python Morsels")
        self.assertEqual(python_results[1].text, "Python Training")
        self.assertEqual(len(python_results), 2)
        self.assertEqual(
            python_results[0].children[0].text,
            "Fix Python Morsels login page bug",
        )
        self.assertEqual(
            python_results[0].children[1].text,
            "Write new Python Morsels emails",
        )
        self.assertEqual(len(python_results[0].children), 2)
        self.assertEqual(
            str(python_results),
            dedent("""
            - Python Morsels
                - Fix Python Morsels login page bug
                - Write new Python Morsels emails
            - Python Training
        """).strip('\n'))
        new_results = bullets.filter("new")
        self.assertEqual(
            str(new_results),
            dedent("""
            - Python Morsels
                - Write tests for new exercise
                - Write new Python Morsels emails
            - Python Training
                - Follow-up with new team training client
        """).strip('\n'))


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)

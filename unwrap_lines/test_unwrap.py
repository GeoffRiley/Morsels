from textwrap import dedent
import unittest

from unwrap import unwrap_lines


class UnwrapLinesTests(unittest.TestCase):

    """Tests for unwrap_lines"""

    maxDiff = 5000

    def test_already_wrapped(self):
        text = "This text is already all on one line"
        self.assertEqual(unwrap_lines(text).strip(), text)

    def test_single_paragraph(self):
        text = dedent("""
            Whether I'm teaching new Pythonistas or long-time Python
            programmers, I frequently find that **Python programmers
            underutilize multiple assignment**.
        """).strip()
        unwrapped_text = unwrap_lines(text)
        self.assertEqual(
            unwrapped_text.strip(),
            "Whether I'm teaching new Pythonistas or long-time Python " +
            "programmers, I frequently find that **Python programmers " +
            "underutilize multiple assignment**."
        )

    def test_multiple_paragraphs(self):
        text = dedent("""
            Whether I'm teaching new Pythonistas or long-time Python
            programmers, I frequently find that **Python programmers
            underutilize multiple assignment**.

            Multiple assignment (also known as tuple unpacking or iterable
            unpacking) allows you to assign multiple variables at the same
            time in one line of code. This feature often seems simple after
            you've learned about it, but **it can be tricky to recall
            multiple assignment when you need it most**.

            In this article we'll see what multiple assignment is, we'll take
            a look at common uses of multiple assignment, and then we'll look
            at a few uses for multiple assignment that are often overlooked.

            Note that in this article I will be using [f-strings][] which are
            a Python 3.6+ feature. If you're on an older version of Python,
            you'll need to mentally translate those to use the string
            `format` method.
        """).strip()
        unwrapped_text = unwrap_lines(text)
        self.assertEqual(
            unwrapped_text.strip(),
            "Whether I'm teaching new Pythonistas or long-time Python "
            "programmers, I frequently find that **Python programmers "
            "underutilize multiple assignment**."
            "\n\n"
            "Multiple assignment (also known as tuple unpacking or iterable "
            "unpacking) allows you to assign multiple variables at the same "
            "time in one line of code. This feature often seems simple after "
            "you've learned about it, but **it can be tricky to recall "
            "multiple assignment when you need it most**."
            "\n\n"
            "In this article we'll see what multiple assignment is, we'll "
            "take a look at common uses of multiple assignment, and then "
            "we'll look at a few uses for multiple assignment that are "
            "often overlooked."
            "\n\n"
            "Note that in this article I will be using [f-strings][] which "
            "are a Python 3.6+ feature. If you're on an older version of "
            "Python, you'll need to mentally translate those to use the "
            "string `format` method."
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_extra_line_breaks_preserved(self):
        text = dedent("""
            This is a line
            that is followed by another line


            There are 2 blank lines before this
            And there was 1 before this



            And three before this one
        """).lstrip()
        expected = dedent("""
            This is a line that is followed by another line


            There are 2 blank lines before this And there was 1 before this



            And three before this one
        """).lstrip()
        unwrapped_text = unwrap_lines(text)
        self.assertEqual(unwrapped_text, expected)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_preserve_line_break_if_line_ends_in_spaces(self):
        text = dedent("""
            This is a line ends in two spaces  
            So this line doesn't wrap into it

            This line doesn't end in spaces
            So this line does wrap into it

            This line ends in 1 space 
            So this line does wrap
        """).lstrip()
        expected = dedent("""
            This is a line ends in two spaces  
            So this line doesn't wrap into it

            This line doesn't end in spaces So this line does wrap into it

            This line ends in 1 space So this line does wrap
        """).lstrip()
        unwrapped_text = unwrap_lines(text)
        self.assertEqual(unwrapped_text, expected)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_code_blocks_and_bullet_points(self):
        text = dedent("""
            This text has bullet points:
            - Point 1
            - Point 2

            There are also numbered points:
            1. First item
            2. Second item
        """).lstrip()
        expected = dedent("""
            This text has bullet points:
            - Point 1
            - Point 2

            There are also numbered points:
            1. First item
            2. Second item
        """).lstrip()
        unwrapped_text = unwrap_lines(text)
        self.assertEqual(unwrapped_text, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
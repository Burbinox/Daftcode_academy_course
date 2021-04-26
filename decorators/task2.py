import unittest


def is_palindrome(func):
    def inner(self):
        words = func(self)
        words_without_whitespaces = ''.join([elem for elem in words if elem.isalpha() or elem.isnumeric()]).lower()
        if words_without_whitespaces == words_without_whitespaces[::-1]:
            return words + " - is palindrome"
        else:
            return words + " - is not palindrome"
    return inner


class ExampleTest(unittest.TestCase):
    @is_palindrome
    def show_sentence(self):
        return "annA"

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")


if __name__ == "__main__":
    unittest.main()

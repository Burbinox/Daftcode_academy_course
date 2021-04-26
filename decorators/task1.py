import unittest


def greetings(func):
    def inner(self):
        name_and_surname = func(self)
        split_name_surname = name_and_surname.split()
        name = " "
        for word in split_name_surname:
            name = name + word[0].upper() + word[1:].lower() + " "
        greet = "Hello" + name
        return greet[:-1]
    return inner


class ExampleTest(unittest.TestCase):
    @greetings
    def show_greetings(self):
        return "joe doe"

    def test_result(self):
        self.assertEqual(self.show_greetings(), "Hello Joe Doe")


if __name__ == "__main__":
    unittest.main()
import unittest


def format_output(*args):
    def decorator(func):
        def inner(self):
            dict_form_func = func(self)
            all_correct_args = []
            temp_dict = {}
            for arg in args:
                if "__" in arg:
                    temp = arg.split('__')
                    [all_correct_args.append(elem) for elem in temp]
                    temp_dict[arg] = temp
                else:
                    all_correct_args.append(arg)
                    temp_dict[arg] = [arg]
            for elem in all_correct_args:
                if elem not in dict_form_func.keys():
                    raise ValueError

            returned_dict = {}
            i = 0
            for dict_value_list in temp_dict.values():
                returned_val = ""
                for elem in dict_value_list:
                    returned_val = returned_val + " " + dict_form_func[elem]
                returned_dict[list(temp_dict.keys())[i]] = returned_val[1:]
                i += 1
            return returned_dict
        return inner
    return decorator


class ExampleTest(unittest.TestCase):
    @format_output("first_name")
    def show_dict(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def test_result(self):
        self.assertEqual(self.show_dict(), {"first_name": "Jan"})


if __name__ == "__main__":
    unittest.main()

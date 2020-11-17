import random
import string


def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = "".join(
        (random.choice(string.ascii_letters) for i in range(letters_count))
    )
    sample_str += "".join((random.choice(string.digits)
                           for i in range(digits_count)))

    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = "".join(sample_list)
    return final_string

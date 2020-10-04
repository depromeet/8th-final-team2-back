import os

from utils import random_file_name


def path_user_image(instance, file_name):
    file = random_file_name(file_name)
    return os.path.join("users", str(instance.id), file)

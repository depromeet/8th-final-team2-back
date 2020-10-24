import os

from utils import random_file_name


def path_profile_icon_image(instance, file_name):
    file = random_file_name(file_name)
    return os.path.join("profile_icon", file)

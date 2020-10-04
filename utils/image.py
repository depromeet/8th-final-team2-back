import os
import string
import random
from datetime import datetime
from django.utils import timezone


__all__ = ["random_file_name"]


def random_file_name(file_name):
    random_string = "".join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(10))
    current = datetime.strftime(timezone.now(), "%Y%m%d")
    _, extension = os.path.splitext(file_name)

    return "{current}{random_string}{extension}".format(
        current=current,
        random_string=random_string,
        extension=extension
    )

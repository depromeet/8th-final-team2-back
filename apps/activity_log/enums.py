from django.db import models

class EXP(models.IntegerField) :
    SIGN_IN = 300
    FIRST_POST = 1000
    LIKE = 20
    WRITE_COMMENT = 20
    
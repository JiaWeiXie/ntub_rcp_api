from django.db import models


class ToDo(models.Model):
    """
    代辦事項
    """
    title = models.CharField('標題', max_length=50)
    content = models.TextField('內容')
    canNotify = models.BooleanField('是否需要通知', default=False)
    is_seal = models.BooleanField('是否封存', default=False)


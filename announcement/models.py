from django.db import models
from django.contrib.auth.models import User

from curriculum.models import Subjects


class Announcement(models.Model):
    """
    公告資料表
    """
    post_target = models.ManyToManyField(Subjects, verbose_name="公告目標")
    title = models.CharField('標題', max_length=50)
    content = models.TextField('內容')
    end_date = models.DateField('結束日期')
    post_date = models.DateTimeField('張貼日期', auto_now_add=True)
    created_user = models.ForeignKey(User, verbose_name='張貼人', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '公告資料表'


from django.db import models

from account.models import Teacher, Student


class Subjects(models.Model):
    """
    課程資料表
    """
    subjects_name = models.CharField('課程名稱', max_length=100)
    class_room = models.CharField('教室', max_length=15, blank=True)
    year = models.CharField('學年', max_length=15)
    semester = models.CharField('學期', max_length=10, null=True)
    create_date = models.DateTimeField('建立日期', auto_now_add=True, editable=False)
    is_active = models.BooleanField('是否進行中', default=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, verbose_name='課程教師', null=True)
    members = models.ManyToManyField(Student, verbose_name='課程參與人')

    def __str__(self):
        return self.subjects_name

    class Meta:
        verbose_name = '課程資料表'


class SectionTime(models.Model):
    """
    課程節次資料表
    """
    week = models.IntegerField('星期')
    section = models.IntegerField('節次')
    start_time = models.TimeField('開始時間')
    end_time = models.TimeField('結束時間')
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='科目', related_name='section_times')

    def __str__(self):
        return "星期{}{}第{}節".format(self.week, self.subjects.subjects_name, self.section)

    class Meta:
        unique_together = ('subjects', 'week', 'section')
        verbose_name = '課程節次資料表'

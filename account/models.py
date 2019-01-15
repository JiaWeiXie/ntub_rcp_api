from django.db import models
from django.contrib.auth.models import User

import uuid
import datetime


ORG_TYPE_CHOICES = (
        ('edu', '學校、教育單位'),
        ('idv', '個人、教師、獨立使用'),
    )
COUNTRY_CHOICES = (
    ('tw', '臺灣'),
)


class OrgUnits(models.Model):
    """
    單位組織資料表
    """
    org_code = models.CharField('組織單位代碼', max_length=100, primary_key=True)
    org_type = models.CharField('組織單位類型', max_length=10, help_text='ex: edu, idv, com',
                                choices=ORG_TYPE_CHOICES, blank=False)
    country = models.CharField('國家', max_length=10, help_text='ex: tw, us', choices=COUNTRY_CHOICES, default='tw')
    abbreviation = models.CharField('單位縮寫', max_length=50, help_text='ex: ntub', blank=False)
    name = models.CharField('組織單位名稱', max_length=100, help_text='ex:臺北商業大學', blank=False)
    create_date = models.DateTimeField('建立日期', auto_now_add=True, editable=False)
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    org_uuid = models.UUIDField(default=uuid.uuid4)

    def get_org_code(self):
        return '{}.{}.{}'.format(self.abbreviation, self.org_type, self.country)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.org_code = self.get_org_code()
        self.abbreviation = self.abbreviation.lower()
        self.create_date = datetime.datetime.now()
        return super(OrgUnits, self).save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '單位組織資料表'


class Teacher(models.Model):
    """
    教師資料表
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='教師使用者id')
    department = models.CharField('科系', max_length=50)
    time_case = models.CharField('專兼任', max_length=20, null=True)
    job_title = models.CharField('職務名稱', max_length=45, default='老師')
    unit_col = models.ForeignKey(OrgUnits, on_delete=models.CASCADE, verbose_name='所屬單位')

    def __str__(self):
        return '{} {}'.format(self.user.get_full_name(), self.job_title)

    class Meta:
        verbose_name = '教師資料表'


class Student(models.Model):
    """
    學生資料表
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='學生使用者id')
    department = models.CharField('科系', max_length=50)
    edu_type = models.CharField('學制', max_length=45)
    edu_year = models.CharField('入學年', max_length=45, help_text='西元年')
    team_type = models.CharField('組別', max_length=45, null=True)
    id_number = models.CharField('學號', max_length=50)
    class_number = models.CharField('班級號碼', max_length=20)
    unit_col = models.ForeignKey(OrgUnits, on_delete=models.CASCADE, verbose_name='所屬單位')

    def __str__(self):
        return '{}. {}'.format(self.user.id, self.user.username)

    class Meta:
        verbose_name = '學生資料表'


class RegisterToken(models.Model):
    """
    註冊Token資料表
    """
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.token)


class DeviceInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    device_numbers = models.CharField('推播裝置代碼', max_length=255, null=True)
    sys_type = models.CharField('系統識別', max_length=45)
    phone_number = models.CharField('電話號碼', max_length=45)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.phone_number)


def is_teacher(user):
    try:
        Teacher.objects.get(user=user)
        return True
    except Teacher.DoesNotExist:
        return False


def is_student(user):
    try:
        Student.objects.get(user=user)
        return True
    except Student.DoesNotExist:
        return False

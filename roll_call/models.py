import uuid
import random

from django.db import models

from curriculum.models import Subjects, SectionTime, Student


class Beacon(models.Model):
    curriculum = models.OneToOneField(Subjects, on_delete=models.CASCADE, verbose_name='課程')
    beacon_id = models.CharField('beacon 名稱', max_length=50)
    beacon_uuid = models.UUIDField(default=uuid.uuid4)
    beacon_major = models.IntegerField()
    beacon_minor = models.IntegerField()
    is_manual = models.BooleanField('是否手動', default=False)

    def check_unique(self, major=None, minor=None):
        try:
            return not bool(Beacon.objects.get(beacon_uuid=self.beacon_uuid,
                                               beacon_major=major if major is not None else self.beacon_major,
                                               beacon_minor=minor if major is not None else self.beacon_minor))
        except Beacon.DoesNotExist:
            return True

    def refresh_beacon(self):
        major, minor = random.sample(range(1, 65536), 2)
        while not self.check_unique(major, minor):
            major, minor = random.sample(range(1, 65536), 2)
        self.beacon_major = major
        self.beacon_minor = minor
        self.save()
        return self

    @staticmethod
    def create_beacon(curriculum):
        beacon_uuid = curriculum.teacher.unit_col.org_uuid
        beacon_id = "{}的iBeacon".format(curriculum.subjects_name)
        try:
            beacon = Beacon.objects.get(curriculum=curriculum, beacon_uuid=beacon_uuid, beacon_id=beacon_id)
        except Beacon.DoesNotExist:
            beacon = Beacon(curriculum=curriculum, beacon_uuid=beacon_uuid, beacon_id=beacon_id)
        return beacon.refresh_beacon()

    def __str__(self):
        return "{} Beacon".format(self.curriculum.subjects_name)

    class Meta:
        unique_together = ('beacon_uuid', 'beacon_major', 'beacon_minor')


class RollCallCheck(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='學生')
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, verbose_name='iBeacon')
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE, verbose_name='節次')
    check_time = models.TimeField(auto_now_add=True)
    check_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.student.user.get_full_name())

    class Meta:
        verbose_name = '點名資料表'


class RollCallCheckHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='學生')
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, verbose_name='iBeacon')
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE, verbose_name='節次')
    check_time = models.TimeField(auto_now_add=True)
    check_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '點名歷史資料表'


class RollCallRecord(models.Model):
    record_type = models.CharField('假別，曠課，到課', max_length=50, default='到課')
    record_date = models.DateField('日期')
    record_ratio = models.FloatField('到課比例', default=0.0)
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE, verbose_name='節次')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='學生')

    def __str__(self):
        return "{} {}".format(self.student.user.get_full_name(), self.record_type)

    class Meta:
        verbose_name = '缺曠紀錄資料表'

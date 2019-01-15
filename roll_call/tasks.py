import pandas

from django.db import transaction
from curriculum.models import Subjects
from .models import Beacon, RollCallCheck, RollCallRecord, RollCallCheckHistory


@transaction.atomic
def refresh_all_beacon():
    all_subjects = Subjects.objects.all()

    for obj in all_subjects:
        Beacon.create_beacon(obj)


def judge_data(item):
    if item >= 80.0:
        return "到課"
    elif 60 <= item < 80:
        return "遲到"
    else:
        return "曠課"


@transaction.atomic
def statistics_record():
    all_check = RollCallCheck.objects.all()
    check_data = list(all_check.values())
    if len(check_data) > 0:
        pd = pandas.DataFrame(check_data).drop(['id', 'check_date'], axis=1)
        pd = pd.groupby(['check_time', 'section_time_id', 'student_id'], as_index=False).count()
        pd2 = pd.groupby(['check_time', 'section_time_id'], as_index=False).max()
        pd2 = pd2.rename(columns={'beacon_id': 'max_count'}).drop(['student_id'], axis=1)
        pd = pandas.merge(pd, pd2, on=['check_time', 'section_time_id'])
        pd['beacon_id'] = pd['beacon_id'] / pd['max_count'] * 100
        pd.columns = ['record_date', 'section_time_id', 'student_id', 'record_ratio', 'max_count']
        pd['record_type'] = pd['record_ratio'].map(judge_data)
        pd['record_date'] = pd['record_date'].map(lambda d: d.strftime('%Y-%m-%d'))
        pd = pd.drop('max_count', axis=1)
        data = list(pd.to_dict(orient='records'))
        record_models = [RollCallRecord(**it) for it in data]
        if len(record_models) > 0:
            RollCallRecord.objects.bulk_create(record_models)
            history_models = [RollCallCheckHistory(**it) for it in check_data]
            RollCallCheckHistory.objects.bulk_create(history_models)
            for model in all_check:
                model.delete()

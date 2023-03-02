from account.models import User


def point_distribution():
    heads = User.objects.filter(role=User.HEAD)
    staffs_count = User.objects.filter(role=User.STAFF).count()
    new_point = staffs_count * 5
    heads.update(point = new_point)

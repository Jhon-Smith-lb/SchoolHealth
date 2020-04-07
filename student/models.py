from django.db import models

BSEX_MALE = 0
BSEX_FEMALE = 1
BSEX_ITEMS = [
    (BSEX_MALE, '男寝'),
    (BSEX_FEMALE, '女寝'),
]


SEX_MALE = 0
SEX_FEMALE = 1
SEX_ITEMS = [
    (SEX_MALE, '男'),
    (SEX_FEMALE, '女'),
]


class Admin(models.Model):
    ano = models.CharField(max_length=25, verbose_name='教工号', primary_key=True)
    name = models.CharField(max_length=25, verbose_name='管理员姓名')
    password = models.CharField(max_length=25, verbose_name='密码')
    phone = models.CharField(max_length=25, verbose_name='管理员电话')
    desc = models.CharField(max_length=255, verbose_name='备注', null=True)

    class Meta:
        verbose_name = verbose_name_plural = '管理员信息'

    def __str__(self):
        return self.name


class Build(models.Model):
    bno = models.CharField(max_length=25, verbose_name='寝室楼号', primary_key=True)
    bsex = models.PositiveIntegerField(default=BSEX_MALE, choices=BSEX_ITEMS, verbose_name='寝室类别')
    admin = models.ForeignKey(Admin, verbose_name='管理员', on_delete=models.CASCADE)
    desc = models.CharField(max_length=225, verbose_name='备注', null=True)

    def __str__(self):
        return self.bno


    class Meta:
        verbose_name = verbose_name_plural = '寝室楼信息'


class Student(models.Model):
    sno = models.CharField(max_length=10, verbose_name='学号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    idCard = models.CharField(max_length=25, verbose_name='身份证号')
    phone = models.CharField(max_length=25, verbose_name='手机号')
    sex = models.PositiveIntegerField(default=SEX_MALE, choices=SEX_MALE, verbose_name='性别')
    birthday = models.DateTimeField(verbose_name='出生日期')
    college = models.CharField(max_length=25, verbose_name='学院')
    # subject = models.CharField(max_length=25, verbose_name='专业')
    # grade = models.CharField(max_length=25, verbose_name='年级')
    # Class = models.CharField(max_length=25, verbose_name='班级')
    subject_class = models.CharField(max_length=25, verbose_name='专业班级')
    build = models.ForeignKey(Build, verbose_name='寝室楼号', on_delete=models.CASCADE)
    room = models.CharField(max_length=10, verbose_name='寝室号')
    session = models.CharField(max_length=255, verbose_name='Session', null=True)

    class Meta:
        verbose_name = verbose_name_plural = '学生信息'

    def __str__(self):
        return self.name


BEHAVE_IN = 1
BEHAVE_OUT = 0
BEHAVE_ITEMS = [
    (BEHAVE_OUT, '出'),
    (BEHAVE_IN, '入'),
]


class In_out(models.Model):
    sname = models.ForeignKey(Student, verbose_name='学生姓名', on_delete=models.CASCADE)
    behave = models.PositiveIntegerField(default=BEHAVE_IN, choices=BEHAVE_ITEMS, verbose_name='出入情况')
    reason = models.CharField(max_length=225, verbose_name='事由', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    temp = models.FloatField(verbose_name='体温')
    college = models.CharField(max_length=25, verbose_name='学院')
    subject_class = models.CharField(max_length=25, verbose_name='专业班级')
    build = models.CharField(max_length=10, verbose_name='寝室楼号')
    room = models.CharField(max_length=10, verbose_name='寝室号')

    class Meta:
        verbose_name = verbose_name_plural = '学生登记信息'

    def __str__(self):
        return self.sname

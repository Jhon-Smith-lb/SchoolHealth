import datetime
from django.shortcuts import render, reverse, redirect
from student.models import In_out, Student
from django.http import HttpResponse
from student.models import Admin
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xlwt import Workbook
from io import BytesIO
from django.db.models import Sum


def login(request):
    if request.method == 'GET':
        return render(request, 'blogin.html', locals())
    else:
        '''第一次登录，绑定'''
        pwd = request.POST.get('pwd')
        ano = request.POST.get('ano')
        try:
            admin = Admin.objects.get(ano=ano)
        except Admin.DoesNotExist:
            '''工号填写错误'''
            error_msg = '您的工号不存在'
            return render(request, 'blogin.html', locals())
        else:
            '''工号和密码不匹配'''
            if admin.password != pwd:
                error_msg = '您的密码有误'
                return render(request, 'blogin.html', locals())
            else:
                '''匹配成功，设置session,之后返给管理员一个登记页面'''
                request.session['ano'] = ano
                return redirect(reverse('in_out_list'))


def Logout(request):
    logout(request)
    return redirect(reverse('login'))


def in_out_list(request):
    ano = request.session.get('ano', None)
    if not ano:
        return redirect(reverse('login'))
    admin = Admin.objects.get(ano=ano)
    rec_list = In_out.objects.all().order_by('-date')[:50]
    paginator = Paginator(rec_list, 10)
    page = request.GET.get('page')
    flag = '#'
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request, 'bindex.html', locals())


def query(request):
    ano = request.session.get('ano', None)
    if not ano:
        return redirect(reverse('login'))
    admin = Admin.objects.get(ano=ano)
    keyword = request.POST.get('query')
    flag = keyword
    if keyword == '':
        # print('@@@')
        return redirect(reverse('in_out_list'))
    if keyword[0] == 'A':
        '''学号'''
        # print('1')
        rec_list = In_out.objects.filter(sname_id=keyword).order_by('-date')
    elif (keyword[0] == 'B' or keyword[0] == 'N') and len(keyword) > 2:
        '''楼号+寝室号'''
        # print('2')
        build = keyword[:2]
        room = keyword[-3:]
        print(build)
        print(room)
        rec_list = In_out.objects.filter(build=build).filter(room=room).order_by('-date')
    elif len(keyword) <= 2:
        '''楼号'''
        # print('3')
        build = keyword[:2]
        rec_list = In_out.objects.filter(build=build).order_by('-date')
    else:
        '''学院'''
        # print('4')
        rec_list = In_out.objects.filter(college=keyword).order_by('-date')
    if rec_list:
        paginator = Paginator(rec_list, 9)
        page = request.GET.get('page')
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)
        return render(request, 'bindex.html', locals())
    else:
        return render(request, 'bBase.html', locals())


def export(request, flag):
    if flag == '#':
        '''导出最近50条'''
        rec_list = In_out.objects.all().order_by('-date')[:50]
    elif flag[0] == 'A':
        '''学号'''
        # print('1')
        rec_list = In_out.objects.filter(sname_id=flag).order_by('-date')
    elif (flag[0] == 'B' or flag[0] == 'N') and len(flag) > 2:
        '''楼号+寝室号'''
        # print('2')
        build = flag[:2]
        room = flag[-3:]
        rec_list = In_out.objects.filter(build=build).filter(room=room).order_by('-date')
    elif len(flag) <= 2:
        '''楼号'''
        # print('3')
        build = flag[:2]
        rec_list = In_out.objects.filter(build=build).order_by('-date')
    else:
        '''学院'''
        # print('4')
        rec_list = In_out.objects.filter(college=flag).order_by('-date')
    if rec_list:
        """创建工作簿"""
        ws = Workbook(encoding="UTF-8")
        if flag == '#':
            title = '最近50条出入记录'
        else:
            title = flag + '的所有出入记录'
        w = ws.add_sheet(title)
        w.write(0, 0, u'序号')
        w.write(0, 1, u'学号')
        w.write(0, 2, u'姓名')
        w.write(0, 3, u'专业班级')
        w.write(0, 4, u'楼和寝室')
        w.write(0, 5, u'时间')
        w.write(0, 6, u'出/入')
        w.write(0, 7, u'体温')
        w.write(0, 8, u'出入理由')
        excel_row = 1
        for obj in rec_list:
            data_id = excel_row
            data_sname_id = obj.sname_id

            # 这里只能通过学号查到学生后，再获取到他的名字
            student = Student.objects.get(sno=obj.sname_id)
            data_sname = student.name

            data_subject_class = obj.subject_class
            data_build_room = str(obj.build) + ' ' + str(obj.room)

            # 这里日期date的类型要转成字符串类型，才能写入Excel
            data_date = str(obj.date)
            if obj.behave == '0':
                data_behave = '出'
            else:
                data_behave = '入'
            data_temp = obj.temp
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_sname_id)
            w.write(excel_row, 2, data_sname)
            w.write(excel_row, 3, data_subject_class)
            w.write(excel_row, 4, data_build_room)
            w.write(excel_row, 5, data_date)
            w.write(excel_row, 6, data_behave)
            w.write(excel_row, 7, data_temp)
            excel_row += 1
        sio = BytesIO()
        ws.save(sio)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        # 设置导出表的名称
        response['Content-Disposition'] = 'attachment; filename=' + title + '.xls'
        response.write(sio.getvalue)
        return response
    else:
        return HttpResponse("不可打印")


def count(request):
    colleges = [
        '电气与信息学院',
    ]


    # 获取指定日期并且查询
    get_year = request.POST.get('year')
    get_month = request.POST.get('month')
    get_day = request.POST.get('day')
    get_records = In_out.objects.filter(date__date=datetime.date(get_year, get_month, get_day))
    get_count = get_records.count()


    # 查询本周累计记录
    monday = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    week_records = In_out.objects.filter(date__gte=monday)
    week_count = week_records.count()


    # 查询本日累计记录
    today_year = datetime.datetime.now().year
    today_month = datetime.datetime.now().month
    today_day = datetime.datetime.now().day
    day_records = In_out.objects.filter(date__date=datetime.date(today_year, today_month, today_day))
    day_count = day_records.count()


    return HttpResponse(week_count)



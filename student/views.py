from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, In_out


def in_out(request, build_id):
    sno = request.session.get('sno', None)
    # test = request.POST.get('in_out')
    # print(test)
    if request.method == 'GET':
        if not sno:
            '''第一次访问或者session已过期'''
            return render(request, 'page-login.html', locals())
        else:
            '''已有session且session没有过期，请求登记页面'''
            student = Student.objects.get(sno=sno)
            if student.build_id == build_id:
                '''是这栋楼的学生'''
                return render(request, 'contact.html', locals())
            else:
                '''不是这栋楼的学生'''
                error_msg = '对不起，您不是这栋楼的学生'
                return render(request, 'error.html', locals())
    else:
        if not sno:
            '''绑定请求'''
            pwd = request.POST.get('pwd')
            sno = request.POST.get('sno')
            try:
                student = Student.objects.get(sno=sno)
            except Student.DoesNotExist:
                '''学号填写错误'''
                error_msg = '您的学号不存在'
                return render(request, 'page-login.html', locals())
            else:
                '''学号和密码不匹配'''
                idcard = student.idCard
                if idcard[-6:] != pwd:
                    error_msg = '您的密码有误'
                    return render(request, 'page-login.html', locals())
                else:
                    '''匹配成功，设置session,之后返给该学生一个登记页面'''
                    request.session['sno'] = sno
                    student = Student.objects.get(sno=sno)
                    if student.build_id == build_id:
                        '''是这栋楼的学生'''
                        return render(request, 'contact.html', locals())
                    else:
                        '''不是这栋楼的学生'''
                        error_msg = '对不起，您不是这栋楼的学生'
                        return render(request, 'error.html', locals())
        else:
            '''用户要进入或者出行'''
            student = Student.objects.get(sno=sno)
            # print(sno)
            # print(type(build_id))
            # print(type(student.build_id))
            in_out = request.POST.get('in_out')
            temp = request.POST.get('temp')
            reason = request.POST.get('reason')
            if in_out == '0':
                '''外出'''
                flag = 0
                '''创建一条这个学生的出行信息'''
                msg = In_out()
                msg.behave = 0
                if reason:
                    msg.reason = reason
                msg.temp = temp
                msg.sname_id = student.sno
                msg.build = student.build
                msg.college = student.college
                msg.room = student.room
                msg.subject_class = student.subject_class
                msg.save()
                return render(request, 'show.html', locals())
            else:
                '''进入'''
                flag = 1
                '''是这栋楼的学生，创建一条这个学生的进入信息'''
                msg = In_out()
                msg.behave = 1
                if reason:
                    msg.reason = reason
                msg.temp = temp
                msg.sname_id = student.sno
                msg.build = student.build
                msg.college = student.college
                msg.room = student.room
                msg.subject_class = student.subject_class
                msg.save()
                return render(request, 'show.html', locals())





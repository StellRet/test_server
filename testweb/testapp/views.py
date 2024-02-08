from django.shortcuts import render, redirect, reverse

from django.http import HttpResponse, HttpResponseRedirect

from .forms import RegisterForm, EditForm

from .models import User, PsychoType

import logging

log = logging.getLogger('debug')
er_log = logging.getLogger('error_log')
def index(request):
    users = User.objects.all()
    return render(request, "index.html", context = { "users" : users, "user_exist" :  request.GET.get("user_exist", False), "user_not_exist" :  request.GET.get("user_not_exist", False), "welcome" :  request.GET.get("welcome", "")})

def user(request):
    name = request.GET.get("name", "Johnny Sins")
    return render(request, "index_old.html", context={"name": name, })

def about(request):
    return HttpResponse("<p><h2>KVANT.INC</h2></p>")

def register(request):
    if request.method == "POST":
        if (request.POST.get("name") == ''):
            log.debug(f"ОШИБКА: введено пустое имя {request.POST.get('name')}")
            er_log.error(f"ОШИБКА: введено пустое имя {request.POST.get('name')}")
            return HttpResponseRedirect("/")
        if (request.POST.get("name") != ''):
            log.info(f"Создан сотрудник {request.POST.get('name')}")
        log.info(f"Добро пожаловать в КВАААААНТ! {request.POST.get('name')}")
        if (len(request.POST.getlist("psycho_types", [])) == 0):
            log.debug(f"ОШИБКА: нет должности {request.POST.get('name')}")
            er_log.error(f"ОШИБКА: нет должности {request.POST.get('name')}")
        if (len(request.POST.getlist("psycho_types", [])) > 0):
            log.info(f'Должность сотрудника - {request.POST.getlist("psycho_types", [])}')
        log.info(f'Сотруднику присвоенна должность {request.POST.getlist("psycho_types", [])}')
        user, created = User.objects.get_or_create(name = request.POST.get("name"))

        if not created:
            return HttpResponseRedirect("/?user_exist=True")

        ptypes = request.POST.getlist("psycho_types", [])
        user.save()

        for ptype in ptypes:
            pt, _ = PsychoType.objects.get_or_create(name = ptype)
            user.ptypes.add(pt)
        return HttpResponseRedirect(f"/?welcome=Добро пожаловать в KVANT {' и '.join(ptypes)}")
    return render(request, "register.html", { "form" : RegisterForm() })

def edit(request, name):
    try:
        if request.method == "GET":
            return render(request, "register.html", { "form" : EditForm(), "name" : request.GET.get('name')})
        if request.method == "POST":
            user = User.objects.get(name = name)
            ptypes = request.POST.getlist("psycho_types", [])
            user.save()
            user.ptypes.clear()
            log.info(f"Сотрудник изменен {name}")


            for ptype in ptypes:
                pt, _ = PsychoType.objects.get_or_create(name = ptype)
                user.ptypes.add(pt)
            return HttpResponseRedirect("/?welcome=Пользователь отредактирован")
    except User.DoesNotExist:
        return HttpResponseRedirect("/?user_not_exist=True")

def delete(request, name):
    try:
        user = User.objects.get(name = name)
        user.delete()
        log.info(f"Сотрудник уволен {name}")
        return redirect("index")
    except User.DoesNotExist:
        return HttpResponseRedirect("/?user_not_exist=True")

from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})
    
def chat_list(request):
    terms = terms_work.get_chat_for_table()
    return render(request, "chat_list.html", context={"terms": terms})

def add_term(request):
    return render(request, "term_add.html")
    
def add_chat(request):
    return render(request, "chat.html")

def video_lessons(request):
    return render(request, "videolessons.html")

def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание не должно быть пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин не должен быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_chat(request)
        
def send_chat(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Текст отзыва не должен быть пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Тема отзыва не должна быть пустой"
        else:
            context["success"] = True
            context["comment"] = "Ваш отзыв принят"
            terms_work.write_msg(new_term, new_definition, user_name)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "chat_request.html", context)
    else:
        add_term(request)

def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

def hist(request):
    return render(request, "hist.html")
    
def chat(request):
    return render(request, "chat.html")
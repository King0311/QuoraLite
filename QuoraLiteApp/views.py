from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Count
from .models import *


@login_required(login_url="login")
def index(request):
    question_with_top_answers = []
    questions = Question.objects.all()
    for question in questions:
        # print(question.id, question.no_of_answers)
        if question.no_of_answers == 0:
            question_with_top_answers.append(
                {
                    "question_details": question.question_text,
                    "question_user_id": question.user.id,
                    "question_id": question.id,
                    "answer_detail": "No answers yet",
                    "answer_id": 0,
                    "answer_count": 0,
                }
            )
        elif question.no_of_answers == 1:
            answer = Answer.objects.filter(question=question.id)[0]
            question_with_top_answers.append(
                {
                    "question_details": question.question_text,
                    "question_user_id": question.user.id,
                    "question_id": question.id,
                    "answer_detail": answer.answer_text,
                    "answer_id": answer.id,
                    "answer_count": 1,
                }
            )
        else:
            answers = Answer.objects.filter(question=question.id)
            max_like = 0
            temp = answers[0]
            for answer in answers:
                likes = len(Likes.objects.filter(answer=answer.id))
                if likes >= max_like:
                    max_like = likes
                    temp = answer
            question_with_top_answers.append(
                {
                    "question_details": question.question_text,
                    "question_user_id": question.user.id,
                    "question_id": question.id,
                    "answer_detail": temp.answer_text,
                    "answer_id": temp.id,
                    "answer_count": question.no_of_answers,
                }
            )

    for question in question_with_top_answers:
        if question["answer_count"] >= 1:
            question["liked"] = len(
                Likes.objects.filter(answer=question["answer_id"], user=request.user.id)
            )
        # breakpoint()

    print(question_with_top_answers)

    return render(
        request, "index.html", {"question_with_top_answers": question_with_top_answers}
    )


@login_required(login_url="login")
def liking(request, answer_id):
    if request.method == "POST":
        re = request.POST["re"]
    else:
        re = request.GET["re"]

    print(re)
    user = request.user
    answer = get_object_or_404(Answer, id=answer_id)

    like_obj = Likes.objects.filter(answer=answer, user=user)

    if like_obj.exists():
        like_obj.delete()
    else:
        Likes.objects.create(answer=answer, user=user)

    return redirect(f"/{re}")  # Ensure proper slash usage


@login_required(login_url="login")
def viewall(request,question_id):
    if request.method == "POST":
        answer_text = request.POST["answer_text"]
        Answer.objects.create(
            question=Question.objects.filter(id=question_id)[0],
            answer_text=answer_text,
            user=request.user,
        )
        return redirect(f"/viewall/{question_id}")

    question = Question.objects.filter(id=question_id)[0]
    answer = Answer.objects.filter(question=question.id)
    data = [{
        "question" : question,
    }]
    answer_details_list = []
    for ans in answer:
        answer_details_list.append(
            {
                "answer": ans,
                "likes": len(Likes.objects.filter(answer=ans)),
                "youliked": len(Likes.objects.filter(answer=ans,user=request.user)),
            }
        )
    data[0]["answer_details"] = answer_details_list
    print(data)
    return render(request,"viewall.html",{"data":data})


@login_required(login_url="login")
def yourquestions(request):
    if request.method == "POST":
        question_text = request.POST["question_text"]
        question = Question.objects.create(user=request.user, question_text=question_text)
        return redirect("yourquestions")
    
    user = request.user
    all_questions = Question.objects.filter(user=user)
    data = []
    for question in all_questions:  
        data.append({
            "question_details" : question,
            "answer_details" :[] 
        })

    for question in data:
        all_answers = Answer.objects.filter(question=question["question_details"])
        for answer in all_answers:
            question["answer_details"].append({
                "answer_details" : answer,
                "likes" : len(Likes.objects.filter(answer=answer, user=user)),
            })

    print(data)

    return render(request, "yourquestions.html", {"data": data})


def login(request):
    if request.method == "POST":
        username = request.POST["loginName"]
        password = request.POST["loginPassword"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            user = auth.authenticate(email=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Something went wrong")
                return redirect("login")
    else:
        return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        try:
            print(request.POST)
            first_name = request.POST["registerFirstName"]
            last_name = request.POST["registerLastName"]
            username = request.POST["registerUsername"]
            email = request.POST["registerEmail"]
            password1 = request.POST["registerPassword"]
            password2 = request.POST["registerRepeatPassword"]

            if password1 != password2:
                messages.info(request, "Passwords do not match")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email is already registered")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username is already taken")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                return redirect("login")

        except Exception as e:
            print("Signup Error:", e)
            messages.error(request, "Something went wrong. Try again.")

    return render(request, "signup.html")


def logout(request):
    auth.logout(request)
    return redirect("/")

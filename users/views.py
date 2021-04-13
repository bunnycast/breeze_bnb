import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView

from mixins import LoggedOutOnlyView, LoggedInOnlyView, EmailLoginOnlyView
from settings import config
from users.models import User
from users.forms import LoginForm, SignUpForm


class LoginView(LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(reverse("core:home"))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

    """  Refactoring Using FormView 
    def get(self, request):
        form = LoginForm(initial={"email": "abc@de.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})
    """


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:home")

    # count = User.objects.last().pk
    # initial = {
    #     "first_name": "user",
    #     "last_name": f"test{count}",
    #     "email": f"berzzubunny+test{count}@gmail.com",
    # }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # TODO : add success msg
    except User.DoesNotExist:
        # TODO : add error msg
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = config["GH_ID"]
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_url={redirect_uri}&scope=user:email&allow_signup=false"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = config["GH_ID"]
        client_secret = config["GH_SECRET"]
        code = request.GET.get("code", None)
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None:
                return GithubException("Can't get access token")
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_request = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                email_json = email_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = email_json[0].get("email")
                    bio = profile_json.get("bio")

                    # blank 검증
                    name = "" if name is None else name
                    bio = "" if bio is None else bio

                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            # 다른 방식으로 같은 메일을 사용하여 소셜 로그인을 한 경우
                            raise GithubException(
                                f"Please log in with: {user.login_mehtod}"
                            )
                    except User.DoesNotExist:
                        # 신규 소셜 로그인 가입
                        user = User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()  # 소셜 로그인 계정에 발급하는 임시 비밀번호
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = config["K_KEY"]
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = config["K_KEY"]
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        print(token_json)
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("not Token")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        profile_json = profile_request.json()

        # 이메일 추출
        email = profile_json.get("kakao_account").get("email", None)

        # 이메일 동의 안하면 나가리
        if email is None:
            raise KakaoException(
                "Can't get authorization code. Please confirm your Email agreement."
            )

        # 닉네임, 프로필 추출
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")

        try:
            # 이전에 카카오 계정으로 로그인 했는지 검증
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException("Please also give me your email")
        except User.DoesNotExist:
            # 없으니까 계정 만듬
            user = User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = User
    # 현재 로그인한 유저 호출
    context_object_name = "user_obj"


class UpdateUserProfileView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "users/update-profile.html"
    context_object_name = "user_obj"
    success_message = "Update Profile Success!"
    fields = (
        "first_name",
        "last_name",
        "bio",
        "gender",
        "birthday",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.request.user.pk,))


class UpdateUserPasswordView(LoggedInOnlyView, EmailLoginOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update-password.html"
    success_message = "Password Updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "user_obj": self.request.user,
            }
        )
        return context

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))
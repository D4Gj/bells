from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from .forms import (
    BellCreationForm,
    BellForm,
    BellMovementRequest,
    BellMovementRequestForm,
    BellTowerCreationForm,
    LoginForm,
    RegistrationForm,
)
from .models import Bell, BellMovementRequest, Belltower


@method_decorator(login_required, name="dispatch")
class CreateBellTowerView(View):
    def get(self, request):
        if (
            request.user.user_type != "church_operator"
            and not request.user.is_superuser
        ):
            return redirect("home")
        form = BellTowerCreationForm()
        return render(request, "create_belltower.html", {"form": form})

    def post(self, request):
        if (
            request.user.user_type != "church_operator"
            and not request.user.is_superuser
        ):
            return redirect("home")
        form = BellTowerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            bell = form.save(commit=False)
            bell.save()
            return redirect("home")  # Redirect after successful creation
        return render(request, "create_belltower.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class CreateBellView(View):
    def get(self, request):
        if (
            request.user.user_type != "church_operator"
            and not request.user.is_superuser
        ):
            return redirect("home")
        form = BellCreationForm()
        return render(request, "create_bell.html", {"form": form})

    def post(self, request):
        if (
            request.user.user_type != "church_operator"
            and not request.user.is_superuser
        ):
            return redirect("home")
        form = BellCreationForm(request.POST, request.FILES)
        if form.is_valid():
            bell = form.save(commit=False)
            bell.save()
            return redirect("home")  # Redirect after successful creation
        return render(request, "create_bell.html", {"form": form})
@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

@method_decorator(login_required, name="dispatch")
class BellListView(ListView):
    model = Bell
    template_name = "bell_list.html"
    context_object_name = "bell_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class HomeView(TemplateView):
    template_name = "home.html"


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or homepage
                return redirect(
                    "home"
                )  # Change 'home' to the name of your homepage URL pattern
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "login"
            )  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def create_bell_movement_request(request):
    if request.method == "POST":
        form = BellMovementRequestForm(request.POST)
        if form.is_valid():
            bell_movement_request = form.save(commit=False)
            bell_movement_request.requester = request.user
            bell_movement_request.save()
            return redirect("bell_movement_request_detail", pk=bell_movement_request.pk)
    else:
        form = BellMovementRequestForm()
    return render(request, "create_bell_movement_request.html", {"form": form})


@login_required
def edit_bell_movement_request(request, pk):
    bell_movement_request = get_object_or_404(BellMovementRequest, pk=pk)
    if request.method == "POST":
        form = BellMovementRequestForm(
            request.POST, instance=bell_movement_request, user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("bell_movement_request_list")
    else:
        form = BellMovementRequestForm(
            instance=bell_movement_request, user=request.user
        )
    return render(request, "edit_bell_movement_request.html", {"form": form})


@login_required
def edit_bell(request, pk):
    bell = get_object_or_404(Bell, pk=pk)
    if request.method == "POST":
        form = BellForm(request.POST, instance=bell)
        if form.is_valid():
            form.save()
            return redirect("bell_list")
    else:
        form = BellForm(instance=bell)
    return render(request, "edit_bell.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class BellMovementRequestDetailView(DetailView):
    model = BellMovementRequest
    template_name = "bell_movement_request_detail.html"
    context_object_name = "movement_request"


@method_decorator(login_required, name="dispatch")
class BellMovementRequestListView(ListView):
    model = BellMovementRequest
    template_name = "bell_movement_request_list.html"
    context_object_name = "movement_requests"


@method_decorator(login_required, name="dispatch")
class BellTowerListView(ListView):
    model = Belltower
    template_name = "belltower_list.html"  # Specify the template to use
    context_object_name = "belltowers"


@login_required
def edit_belltower(request, pk):
    belltower = get_object_or_404(Belltower, pk=pk)
    if request.method == "POST":
        form = BellTowerCreationForm(request.POST, instance=belltower)
        if form.is_valid():
            form.save()
            return redirect("belltower_list")
    else:
        form = BellTowerCreationForm(instance=belltower)
    return render(request, "edit_belltower.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class BelltowerUpdateView(UpdateView):
    model = Belltower
    form_class = BellTowerCreationForm
    template_name = "edit_belltower.html"
    success_url = reverse_lazy("belltower_list")

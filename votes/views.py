from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from .models import *


def index(request):
    if request.method == 'POST':
        Region.objects.create(
            name=request.POST['name']
        )
        return HttpResponseRedirect(reverse('votes:allregions'))
    return render(request, 'votes/index.html')


def registration(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
        )
        Voter.objects.create(
            name=request.POST['name'],
            address=request.POST['address'],
            user=user
        )

        return HttpResponseRedirect(reverse('votes:login'))
    return render(request, 'votes/registration.html', {})


def login_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votes:allregions'))
        else:
            return render(request, 'votes/login.html')
    return render(request, 'votes/login.html')


def logout_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('votes:login'))


@login_required(login_url='/login/')
def all_regions(request):
    region_list = Region.objects.all()
    admin = False
    if request.user.is_superuser:
        admin = True
    if request.method == 'POST':
        Region.objects.create(
            name=request.POST['name']
        )

    return render(request, 'votes/regions.html', {'form': region_list, 'admin': admin})


@login_required(login_url='/login/')
def details(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    user = request.user
    admin = False
    if request.user.is_superuser:
        admin = True
    if request.method == 'POST':
        region.candidate_set.create(
            name=request.POST['name']
        )
    return render(request, 'votes/details.html', {"region": region, 'admin': admin, 'user': user})


@login_required(login_url='/login/')
def vote(request, region_id):

    region = get_object_or_404(Region, pk=region_id)
    user = request.user
    try:
        voter = Voter.objects.get(user=user)
    except:
        return HttpResponse('invalid user')
    # region.voter_set.add(voter)
    # voter.save()
    # print(voter.region)
    try:
        selected_candidate = region.candidate_set.get(pk=request.POST['candidate'])
    except (KeyError, Candidate.DoesNotExist):
        return render(request, 'votes/details.html', {
            'region': region,
            'error_message': "You didn't select a candidate.",
        })
    else:
        selected_candidate.votes += 1
        selected_candidate.save()
        return HttpResponseRedirect(reverse('votes:details', args=(region.id,)))

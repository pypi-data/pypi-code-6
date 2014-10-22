# -*- coding: utf-8 -*-
import datetime, re
from operator import itemgetter
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import PermissionDenied #change error 
from django.db.models import Q
from .models import Penalty
from .forms import newPenaltyForm
from django.contrib.auth import get_user_model


@login_required
def redwine_home(request):
    try:
        return redwine_com(request, request.user.groups.filter(pk__in=settings.USER_SEARCH_GROUPS)[0])
    except(IndexError):
        return render(request, 'index.html', { "error":True, "errorMessage":"You have no active redwine committees!"})

def redwine_com(request, committee):
    User = get_user_model()
    submitted=False
    showDeleted=False
    ownDelete=False
    editedUser=-1
    try:
        kom = request.user.groups.filter(name=committee)[:1].get();
    except:                                                             #TODO: handle exception better!
        return render(request, 'index.html', { 
            "error":True, 
            "errorMessage":"You don't have access to this committee. If you think you should, please contact a sysadmin."
            })

    if request.method == 'POST':
        act=str(request.POST['act'])
        form = newPenaltyForm(data=request.POST)
        if act =='add':
            if int(form.data['amount'])<=10 and 1<len(form.data['reason'])<=100:
                #todo: sjekk at man gir til samme komite
                item=str(form.data['type'].encode('utf8')).split(".")
                if len(item)<1:
                    return

                s=Penalty(
                    giver=     request.user,
                    committee= str(form.data['committee'].encode('utf8')),
                    to=        User.objects.get(pk=(int(form.data['to']))),
                    amount=    int(form.data['amount']),
                    reason=    str(form.data['reason'].encode('utf8')),
                    item=      item[0],
                    item_name= item[1]
                    )
                s.save()
                editedUser=int(form.data['to'])
            else:
                return render(request, 'index.html', { "error":True, "errorMessage":"The reason must be between 1 and 100 chars."})
                
        elif 'delete' in act: 
            #filter for koms
            penalty=Penalty.objects.get(pk=int(act.split(" ")[1]))
            if str(penalty.to.id) != str(request.user.id):
                penalty.deleted=True
                penalty.save()
                editedUser=penalty.to.id

        elif 'nuke' in act:
            #filter for kom
            for penalty in Penalty.objects.filter(to=User.objects.get(pk=int(act.split(" ")[1]))):
                if str(penalty.to.id) != str(request.user.id):
                    penalty.deleted=True
                    penalty.save()
                    editedUser=int(act.split(" ")[1])
                else:
                    ownDelete=True

        elif 'showhidden' in act:
            showDeleted=True
            editedUser=int(act.split(" ")[1])

        else:
            form=newPenaltyForm()

    committees = {} #move total into loop if multiple coms in one page
    total = lambda user: sum([penalty.amount for penalty in user.penalties.filter(deleted=False, committee=com)])
    by_kom= lambda user: user.penalties.filter(deleted=False, committee=com)
    for com in request.user.groups.filter(pk__in=settings.USER_SEARCH_GROUPS):
        if com==kom:
            
            committees[com] = [(user, total(user), by_kom(user)) for user in com.user_set.all()] 
            committees[com].sort(key=itemgetter(1),reverse=True)
        else:
            committees[com] = (0,0,0)

    return render(request, 'index.html', {  
        'committees'   : committees,
        'currCom'      : kom,
        'submittedNew' : submitted,
        'showDeleted'  : showDeleted,
        'editedUser'   : editedUser,
        'ownDelete'    : ownDelete,
        #'form' : form,
        })
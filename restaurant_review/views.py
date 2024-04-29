"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Users 
from .forms import UserForm, AccessForm
from django.http import HttpResponse

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .table import UsersHTMxTable
from .filters import UsersFilter

import pandas as pd

class UsersHTMxTableView(SingleTableMixin, FilterView):
    table_class = UsersHTMxTable
    queryset = Users.objects.all()
    filterset_class = UsersFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "restaurant_review/users_table_partial.html"
        else:
            template_name = "restaurant_review/users_table_htmx.html"

        return template_name


def home(request):
    """Renders the home page."""
    quest_numb = 2
    if quest_numb == 1:
       if (request.method == "POST"):
           twitter = request.POST.get("twitter")
           email = request.POST.get("email")
           ordinals_address = request.POST.get("ordinals_address")
           user_info = Users(twitter = twitter,email = email,ordinals_address = ordinals_address, 
                             points = 50, ref_status= False, date_created = datetime.now(), date_updated = datetime.now(), tweet_link = '', wl = False, fcfs = False)
           user_info.save()
           table = users_uplodad()
           return render(request, "restaurant_review/results.html", {'pandas_table': table.to_html()})
       else:
           userform = UserForm()
           table = users_uplodad()
           return render(request, "restaurant_review/index.html", {"form": userform, 'pandas_table': table.to_html()})
    elif quest_numb == 2:
        code = request.POST.get("access_code")
        verif_code = Users.objects.filter(ref_status=True)
        if (request.method == "POST" and code == None):
           twitter = request.POST.get("twitter")
           email = request.POST.get("email")
           ordinals_address = request.POST.get("ordinals_address")
           user_info = Users(twitter = twitter,email = email,ordinals_address = ordinals_address, 
                             points = 50, ref_status= False, date_created = datetime.now(), date_updated = datetime.now(), tweet_link = '', wl = False, fcfs = False)
           user_info.save()
           table = users_uplodad()
           return render(request, "restaurant_review/results.html", {'pandas_table': table.to_html()})
        elif (request.method == "POST" and code != None):
           fin_code = False
           for i in verif_code:
                if(i.twitter == code):
                    referral = Users.objects.get(twitter=code)
                    referral.points += 100
                    referral.save()
                    fin_code = True
           if fin_code == True:
               access_code = True
               userform = UserForm()
               table = users_uplodad()
               return render(request, "restaurant_review/index.html", {"form": userform, 'pandas_table': table.to_html()})
           else:
               table = users_uplodad()
               return render(request, "restaurant_review/block.html", {'pandas_table': table.to_html()})
        else:
           access_form = AccessForm()
           table = users_uplodad()
           return render(request, "restaurant_review/index.html", {"form": access_form, 'pandas_table': table.to_html()})
    else:
       #ADD functionality for tweets and join user (if no username in db by link)
       access_form = AccessForm()
       table = users_uplodad()
       return render(request, "restaurant_review/index.html", {"form": access_form, 'pandas_table': table.to_html()})


def users_uplodad():
    cell_hover = {  # for row hover use <tr> instead of <td>
            'selector': 'td:hover',
            'props': [('background-color', '#ffffb3')]
        }
    index_names = {
            'selector': '.index_name',
            'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
        }
    headers = {
            'selector': 'th:not(.index_name)',
            'props': 'background-color: white; color: black; font-size: 1em;padding: 0.3em; padding-right: 2em; padding-left: 2em; border-width:5px; border-style: dotted; border-color:black; font-weight: 500; '
        }
    all_users = Users.objects.all()
    df = pd.DataFrame({'Twitter' : [all_users[id].twitter for id in range(len(all_users)-3,len(all_users))],
                             'Points': [all_users[id].points for id in range(len(all_users)-3,len(all_users))]},
                      index = [all_users[id].date_created.strftime("%H:%M:%S")  for id in range(len(all_users)-3,len(all_users))])
    table = df.style.set_table_styles([cell_hover, index_names, headers])
    return table


def contact(request):
    """Renders the contact page."""
    return render(
        request,
        'restaurant_review/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    return render(
        request,
        'restaurant_review/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

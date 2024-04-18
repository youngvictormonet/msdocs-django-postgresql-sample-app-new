from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from restaurant_review.models import Restaurant, Review, Users 


from datetime import datetime
from .forms import UserForm, AccessForm
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .table import UsersHTMxTable
from .filters import UsersFilter
import pandas as pd

# Create your views here.

def index(request):
    quest_numb = 1
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
           return render(request, "restaurant_review/first_quest.html", {"form": userform, 'pandas_table': table})
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
               return render(request, "restaurant_review/first_quest.html", {"form": userform, 'pandas_table': table.to_html()})
           else:
               table = users_uplodad()
               return render(request, "restaurant_review/block.html", {'pandas_table': table.to_html()})
        else:
           access_form = AccessForm()
           table = users_uplodad()
           return render(request, "restaurant_review/first_quest.html", {"form": access_form, 'pandas_table': table.to_html()})
    else:
       #ADD functionality for tweets and join user (if no username in db by link)
       access_form = AccessForm()
       table = users_uplodad()
       return render(request, "restaurant_review/first_quest.html", {"form": access_form, 'pandas_table': table.to_html()})


@cache_page(60)
def details(request, id):
    print('Request for restaurant details page received')
    restaurant = get_object_or_404(Restaurant, pk=id)
    request.session["lastViewedRestaurant"] = restaurant.name
    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})


def create_restaurant(request):
    print('Request for add restaurant page received')
    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
    except (KeyError):
        # Redisplay the form
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description
        Restaurant.save(restaurant)

        return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))


@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        # Redisplay the form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)

    return HttpResponseRedirect(reverse('details', args=(id,)))



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
            'props': 'background-color: #000066; color: white; font-size: 0.8em;padding: 0.6em;'
        }
    all_users = Users.objects.all()
    df = pd.DataFrame({'Twitter' : [all_users[id].twitter for id in range(len(all_users)-0,len(all_users))],
                             'Points': [all_users[id].points for id in range(len(all_users)-0,len(all_users))]},
                      index = [all_users[id].date_created.date()  for id in range(len(all_users)-0,len(all_users))])
    table = df.style.set_table_styles([cell_hover, index_names, headers])
    return [all_users[id].twitter for id in range(len(all_users)-0,len(all_users))]


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

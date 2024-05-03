from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from datetime import datetime

from restaurant_review.models import Restaurant, Review, Users
from restaurant_review.forms import UserForm, AccessForm

import pandas as pd

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from restaurant_review.table import UsersHTMxTable
from restaurant_review.filters import UsersFilter

from django.views import View
from django.http import HttpResponse

from sqlalchemy.exc import OperationalError, ProgrammingError

# Create your views here.

def index(request):
       if (request.method == "POST"):
           twitter = request.POST.get("twitter")
           email = request.POST.get("email")
           ordinals_address = request.POST.get("ordinals_address")
           user_info = Users(twitter = twitter,email = email,ordinals_address = ordinals_address, points = 50, ref_status= False, date_created = datetime.now(), date_updated = datetime.now(), tweet_link = '', wl = False, fcfs = False, invitation_code = 'Public')
           user_info.save()
           table = users_uplodad()
           return render(request, "restaurant_review/results.html", {'pandas_table': table.to_html()})
       else:
           userform = UserForm()
           table = users_uplodad()
           return render(request, "restaurant_review/index.html", {"form": userform, 'pandas_table': table.to_html()})
           
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
            'props': 'background-color: white; color: black; font-size: 1em; padding: 0.3em; padding-right: 2em; padding-left: 2em; border-width:5px; border-style: dotted; border-color:black; font-weight: 500; '
        }
    all_users = Users.objects.all()
    df = pd.DataFrame({'Twitter' : [all_users[id].twitter for id in range(len(all_users)-3,len(all_users))], 'Code': [all_users[id].invitation_code for id in range(len(all_users)-3,len(all_users))]}, index = [all_users[id].date_created.strftime("%H:%M:%S")  for id in range(len(all_users)-3,len(all_users))])
    table = df.style.set_table_styles([cell_hover, index_names, headers])
    return table

class UsersHTMxTableView(SingleTableMixin, FilterView):
    table_class = UsersHTMxTable
    try:
       queryset = Users.objects.all().order_by('points')
    except (OperationalError, ProgrammingError) as e:
       queryset = []
    #queryset = Users.objects.all().order_by('points')
    print(queryset[1].twitter)
    print(queryset[1].invitation_code)
    filterset_class = UsersFilter
    paginate_by = 15
    template_name = "restaurant_review/users_table_htmx.html"

class MyView(View):
    def get(self, request):
        return render(request, 'restaurant_review/create_restaurant.html')

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

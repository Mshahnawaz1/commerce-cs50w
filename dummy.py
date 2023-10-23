from auctions.models import *

# item= Listing.objects.get(item= 'asdf')
# pr = Bid.objects.filter(bid_amount=500)
# pr = Bid.objects.filter(item=)


# winner_user = Bid.objects.get(bid_amount=500, item=item)

categories = Listing.Category
items= Listing.objects.all()

sample = []

for category_k, category in categories:
    for item in items:
        if (category == item.category) and (item.sold == False):
            sample.append(category, item.id)


#             <!-- <a href="{% url 'category' %}?item_id={{categor}}"></a><li>{{ category_value }} </li> -->

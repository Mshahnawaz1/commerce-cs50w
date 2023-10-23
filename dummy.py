from auctions.models import *

item= Listing.objects.get(item= 'asdf')
pr = Bid.objects.filter(bid_amount=500)
pr = Bid.objects.filter(item=)


winner_user = Bid.objects.get(bid_amount=500, item=item)

from network.models import *

p = Posts.objects.get(id=13)

u = User.objects.get(username="ron")
print(u.post_user)
print(p)

from utils import write_dict_list
from requester import Requester

from settings import token

user_1 = 'dayogaru'
user_2 = 'yoga_rimma'


requester = Requester(token=token)

# user_id = requester.find_id(user_1)
# print user_id

user_id = '611334517'

# posts = requester.get_posts(user_id)
# write_dict_list(posts, '../data/posts_1.csv')

# followers = requester.get_followers(user_id)
# write_dict_list(followers, '../data/followers_1.csv')

print requester.get_user_info(user_id)
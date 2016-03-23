from datetime import datetime

from utils import get_json


class Requester:
    '''
    The class for making requests to Instagram API
    '''

    def __init__(self, token):
        self.token = token

    def find_id(self, username, raw=False):

        # make request
        url = 'https://api.instagram.com/v1/users/search?q=' + username + '&client_id=e467b070519f452abe8e687393081b96'
        params = {
            'q': username,
            'access_token': self.token
        }
        data = get_json(url, params)['data']
        # for debug
        if raw:
            return data

        # search for username in response
        res = None
        for user in data:
            if user['username'] == username:
                res = user['id']
                break

        # not found handling
        if not res:
            print 'User not found'
            return None

        return res

    def get_user_info(self, user_id, raw=False):

        # make request
        url = 'https://api.instagram.com/v1/users/' + str(user_id)
        params = {
            'access_token': self.token
        }
        try:
            data = get_json(url, params)['data']
        except:
            print 'User not found'
            return None

        # for debug
        if raw:
            return data

        # extract necessary user info from response
        user = {}
        keys = ['id', 'username', 'bio', 'full_name']
        for key in keys:
            user[key] = data[key]

        user['media_count'] = data['counts']['media']
        user['followed_by_count'] = data['counts']['followed_by']
        user['follows_count'] = data['counts']['follows']
        user['pic_url'] = data['profile_picture']

        return user

    def get_posts(self, user_id, raw=False):

        # make request
        url = 'https://api.instagram.com/v1/users/' + str(user_id) + '/media/recent'
        params = {
            'access_token': self.token
        }
        try:
            data = get_json(url, params)['data']
        except:
            print 'User not found'
            return None

        # for debug
        if raw:
            return data

        # extract necessary posts data from response
        posts = []
        for item in data:
            post = {}
            post['user_id'] = item['user']['id']

            if item['caption']:
                post['caption'] = item['caption']['text']
            else:
                post['caption'] = ''

            post['type'] = item['type']
            post['tags'] = " ".join(item['tags'])  # need to be stored in distinct db table
            post['created_time'] = datetime.fromtimestamp(float(item['created_time']))
            post['likes_count'] = item['likes']['count']

            if item['location']:
                post['loc_latitude'] = item['location']['latitude']
                post['loc_longitude'] = item['location']['longitude']
            else:
                post['loc_latitude'] = ''
                post['loc_longitude'] = ''

            posts.append(post)

        return posts

    def get_followers(self, user_id, raw=False):

        # make request
        url = 'https://api.instagram.com/v1/users/' + str(user_id) + '/followed-by'
        params = {
            'access_token': self.token
        }

        # make request with pagination
        users = []
        cursor = ''
        counter = 0
        while not (cursor is None) and counter < 100:
            params['cursor'] = cursor
            resp = get_json(url, params)
            data = resp['data']

            if raw:
                print data

            if resp['pagination']:
                cursor = resp['pagination']['next_cursor']
            else:
                cursor = None

            for item in data:
                user = {}
                keys = ['id', 'username', 'full_name']
                for key in keys:
                    user[key] = item[key]
                users.append(user)
            counter += 1
        return users
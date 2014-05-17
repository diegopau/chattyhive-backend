import re

__author__ = 'lorenzo'

from uuid import uuid4
from social.backends.facebook import FacebookOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.twitter import TwitterOAuth
from social.exceptions import AuthException
from social.pipeline.user import USER_FIELDS
from core.models import ChProfile


    ### ======================================================== ###
    ###                    Social Pipeline                       ###
    ### ======================================================== ###


# overwrite for the social's create_user default function
def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return
    # get user fields from "pipeline flow"
    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',   # TODO *1
                                               USER_FIELDS))
    if not fields:
        return

    username = fields['username']
    email = fields['email']
    password = uuid4().hex      # aleatory provisional password

    # TODO *1 by creating a new strategy we can avoid this?
    fieldspass = {'username': username, 'email': email, 'password': password}

    user = strategy.create_user(**fieldspass)
    profile = ChProfile(user=user)
    profile.save()

    return {
        'is_new': True,
        'user': user
    }


# overwrite for the social's get_username default function
def get_username(strategy, details, user=None, *args, **kwargs):
    if 'username' not in strategy.setting('USER_FIELDS', USER_FIELDS):
        return
    storage = strategy.storage

    if not user:
        email_as_username = strategy.setting('USERNAME_IS_FULL_EMAIL', False)

        # We only use email as username
        if email_as_username and details.get('email'):
            username = details['email']
        else:
            raise AuthException(
                strategy.backend,
                'No email given from provider'
            )

        final_username = username

    else:
        final_username = storage.user.get_username(user)
    return {'username': final_username}


def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Fill user details using data from provider."""
    if user:
        if kwargs.get('is_new'):
            profile = ChProfile.objects.get(user__username=user)
            original_name = re.sub('[.-]', '_', details.get('username'))
            original_name = re.sub('[^0-9a-zA-Z_]+', '', original_name)
            public_name = original_name
            ii = 0
            while True:
                try:
                    ChProfile.objects.get(public_name=public_name)
                except ChProfile.DoesNotExist:
                    break
                ii += 1
                public_name = original_name + '_' + str(ii)

            profile.set_public_name(public_name)
            profile.set_first_name(details.get('first_name'))
            profile.set_last_name(details.get('last_name'))
            profile.set_sex(details.get('sex'))
            profile.set_language(details.get('language'))
            profile.set_location(details.get('location'))
            profile.set_public_show_age(False)
            profile.set_private_show_age(True)
            profile.save()


    ### ======================================================== ###
    ###                    Social Backends                       ###
    ### ======================================================== ###


# overwrite for the social's GooglePlus backend
class ChGooglePlusAuth(GooglePlusAuth):

    EXTRA_DATA = [
        ('id', 'user_id'),
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('access_type', 'access_type', True),
        ('code', 'code'),                       # provisional place
        ('link', 'link')                        # provisional place
    ]

    def get_user_details(self, response):
        """Return user details from Orkut account"""

        language = response.get('lang')
        # lang_provided = response.get('lang')
        # if lang_provided == 'es':             # todo how to get/show language
        #     language = 'es-es'
        # else:
        #     language = 'en-gb'

        return {'username': response.get('email', '').split('@', 1)[0],     # First part of the email as profile public
                'email': response.get('email', ''),                         # name, is not the user username
                'fullname': response.get('name', ''),
                'first_name': response.get('given_name', ''),
                'last_name': response.get('family_name', ''),
                'sex': response.get('gender', ''),
                'location': response.get('locale', 'es'),  # todo how to show location
                'language': language,
                'url_picture': response.get('picture')}


# overwrite for the social's Twitter backend
class ChTwitterOAuth(TwitterOAuth):

    EXTRA_DATA = [
        ('id', 'id'),
        ('url', 'url'),
        ('protected', 'protected'),
        ('verified', 'verified')
    ]

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        # try to get name and last name from twitter name, not fully accurate
        try:
            first_name, last_name = response['name'].split(' ', 1)
        except:
            first_name = response['name']
            last_name = ''

        # email not provided by twitter, as temporal solution, we create this fake email
        # user must enter a valid email in the last step of user creation
        email = response['screen_name'] + '@twitter.com'

        language = response.get('lang')
        # lang_provided = response.get('lang')
        # if lang_provided == 'es':             # todo how to get/show language
        #     language = 'es-es'
        # else:
        #     language = 'en-gb'

        return {'username': response['screen_name'],
                'email': email,  # not supplied?
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name,
                'sex': '',
                'location': response.get('location', 'es'),
                'language': language,
                'url_picture': response.get('profile_background_image_url', '')}


# overwrite for the social's Facebook backend
class ChFacebookOAuth2(FacebookOAuth2):

    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('verified', 'verified'),
        ('link', 'link'),               # provisional place
        ('birthday', 'birthday')        # provisional place
    ]

    def get_user_details(self, response):
        """Return user details from Facebook account"""

        language = response.get('lang')
        # lang_provided = response.get('lang')
        # if lang_provided == 'es':             # todo how to get/show language
        #     language = 'es-es'
        # else:
        #     language = 'en-gb'

        picture = 'http://graph.facebook.com/' + response.get('id') + '/picture'

        return {'username': response.get('username', response.get('email')).split('@', 1)[0],
                'email': response.get('email', ''),
                'fullname': response.get('name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', ''),
                'sex': response.get('gender', ''),
                'location': response.get('locale', ''),
                'language': language,
                'url_picture': picture}

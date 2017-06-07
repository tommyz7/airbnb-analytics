import requests


class AuthError(BaseException):
    pass


class AirbnbAPI(object):
    """SDK for Airbnb API

    Based on documentation from: http://airbnbapi.org/
    """

    API_URL = "https://api.airbnb.com"

    def __init__(self, client_id: str):
        """
        :param client_id: (API Key)
        """
        self.client_id = client_id
        self._access_token = None
        self._response = None
        self._session = requests.Session()

    def login_by_google(self):
        """TODO: I don't need it but perhaps someday I'll implement it"""
        raise NotImplementedError

    def login_by_facebook(self):
        """TODO: I don't need it but perhaps someday I'll implement it"""
        raise NotImplementedError

    def login_by_email(self, username: str, password: str):
        """Gets an access_token, given a valid user account email and password.

        :param username:        airbnbdev@gmail.com     Account's email address
        :param password:        password                Account's clear-text password (note: endpoint uses HTTPS)
        """

        user_agent = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

        self._session.headers.update({
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            'User-Agent': user_agent
        })

        login_payload = {
            "client_id": self.client_id,
            "grant_type": 'password',
            "username": username,
            "password": password,
            "prevent_account_creation": "true"
        }

        self._response = self._session.post(self.API_URL + "/v1/authorize", json=login_payload)

        try:
            self._access_token = self._response.json()['access_token']
            self._session.headers.update({"X-Airbnb-OAuth-Token": self._access_token})
        except KeyError:
            raise AuthError('{} - {}'.format(
                self._response.json()['error_code'], self._response.json()['error_message']))

    def listing_search(self, **optional_params) -> requests.models.Response:
        """
        Optional URL Parameters:

        Key	                    Sample Value	                            Description
        locale	                en-US	                                    Desired lagnuage
        currency	            USD	                                        Desired currency
        _format	                for_search_results
                                || for_search_results_with_minimal_pricing	Search with pricing or not.
        _limit	                10	                                        Number of listings to show at a time.
        _offset	                0	                                        Number of listings to offset in search.
        guests	                1	                                        Number of guests.
        ib	                    false	                                    Setting to true will only show listings
                                                                            that are instant bookable.
        ib_add_photo_flow	    true	                                    Not sure.
        location	            Los%20Angeles%2C%20CA	                    Search by location name
                                                                            -- if unsure of lat/lng, etc.
        min_bathrooms	        0	                                        Minimum number of bathrooms.
        min_bedrooms	        0	                                        Minimum number of bedrooms.
        min_beds	            0	                                        Minimum number of beds.
        price_min	            40	                                        Minimum price.
        price_max	            210	                                        Maximum price.
        min_num_pic_urls	    10	                                        Minimum number of pictures.
        sort	                1	                                        Sorting order
                                                                            (1: forward order, 0: reverse order).
        suppress_facets	        true	                                    Not sure.
        user_lat	            37.18722222222222	                        Latitude search coordinate.
        user_lng	            -122.42833333333333	                        Longitude search coordinate.

        """
        if "location" in optional_params:
            optional_params['location'] = optional_params['location'].replace(' ', '-')

        return self._session.get(self.API_URL + "/v2/search_results/", params=optional_params)

    def view_listing_info(self, listing_id, **optional_params) -> requests.models.Response:
        """Returns detailed information about a listing, given its ID (e.g., found in the search endpoint reponse).

        Optional URL Parameters:

        Key                 Sample Value	    Description
        locale	            en-US	            Desired lagnuage
        _source	            mobile_p3	        Not sure. I'm guessing this means the request is coming from
                                                an Android mobile phone.
        number_of_guests	1	                Determines listing availability dates based on the # of guests.


        :param listing_id:
        :return requests.models.Response
        """

        # API result format(just put this - it won't work without it)
        optional_params.update({"_format": "v1_legacy_for_p3"})
        return self._session.get(self.API_URL + "/v2/listings/" + str(listing_id), params=optional_params)

    def get_reviews(self, listing_id: int, **optional_params) -> requests.models.Response:
        """Returns reviews for a given listing.


        Optional URL Parameters:

        Key	        Sample Value	                                    Description
        locale	    en-US	                                            Desired lagnuage
        currency	USD	                                                Desired currency
        _format	    for_mobile_client
                    || for_search_results
                    || for_search_results_with_minimal_pricing	        Not sure what the difference is.
        _limit	    10	                                                Number of reviews to show at a time.
        _offset	    0	                                                Number of reviews to offset.

        :param listing_id:
        :param optional_params:
        :return requests.models.Response:
        """
        optional_params.update({"listing_id": listing_id, "role": "all"})
        return self._session.get(self.API_URL + "/v2/reviews/", params=optional_params)

    def view_user_info(self, user_id, **optional_params) -> requests.models.Response:
        """Returns detailed information about a user, given his/her/its ID
        (e.g., found in the view listing endpoint response).

        Optional URL Parameters:

        Key	        Sample Value	    Description
        locale	    en-US	            Desired lagnuage
        currency	USD	                Currency for listings.
        """
        optional_params.update({"_format": "v1_legacy_show"})
        return self._session.get(self.API_URL + "/v2/users/" + str(user_id), params=optional_params)

    def get_host_listings(self, user_id, **optional_params) -> requests.models.Response:
        """Returns information about all the listings a user hosts.

        Optional URL Parameters:

        Key	                    Sample Value	        Description
        locale	                en-US	                Desired lagnuage
        currency	            USD	                    Desired currency
        _format	                v1_legacy_long	        Not sure...
        _limit	                10	                    Max listings to return
        _offset	                0	                    Listing offset
        has_availability	    false	                Whether to show listings that are currently active or not
        user_id	                57297136	            The ID of the user whose listings you'd like to get
        """
        optional_params.update({"user_id": user_id})
        return self._session.get(self.API_URL + "/v2/listings", data=optional_params)

    def create_message_thread(self,
                              listing_id: int,
                              number_of_guests: int,
                              checkin_date: str,
                              checkout_date: str,
                              message: str,
                              **optional_params) -> requests.models.Response:
        """
        Optional URL Parameters:

        Key	        Sample Value	Description
        locale	    en-US	        Desired lagnuage
        currency	USD	            Currency for listings
        :param listing_id:
        :param number_of_guests:
        :param checkin_date:        2018-04-01T00:00:00.000-0700
        :param checkout_date:       2018-04-02T00:00:00.000-0700
        :param message:
        :return:
        """
        data = {
            "listing_id": listing_id,
            "number_of_guests": number_of_guests,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "message": message
        }
        data.update(optional_params)
        return self._session.post(self.API_URL + "v1/threads/create", data=data)

    def get_messages(self, **optional_params) -> requests.models.Response:
        """Returns message threads, given an AirBnB access token (from authenticating with login endpoints).

        Optional URL Parameters:

        Key	                Sample Value	    Description
        locale	            en-US	            Desired lagnuage
        currency	        USD	                Desired currency
        offset	            0	                Number of message threads to offset in search
        items_per_page	    10	                Number of message threads to display at once
        role	            guest	            Type of threads to retrieve. "guest", "host",
                                                    or don't include this param for both

        :param optional_params:
        :return requests.models.Response:
        """
        return self._session.get(self.API_URL + "/v1/threads", data=optional_params)

    def get_user_info(self, **optional_params):
        """Get basic info about the logged-in user, such as name, picture, phone number, verifications, etc.

        Optional URL Parameters:

        Key	                Sample Value	        Description
        locale	            en-US	                Desired lagnuage
        currency	        USD	                    Desired currency
        offset	            0	                    Number of message threads to offset in search
        items_per_page	    10	                    Number of message threads to display at once
        role	            guest	                Type of threads to retrieve. "guest", "host",
                                                    or don't include this param for both
        alert_types[]	    reservation_request	    Not sure...
        """
        return self._session.get(self.API_URL + "/v1/account/active", params=optional_params)

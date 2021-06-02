"""Module for generating favorite customer sellers report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonreports.views import Connection

def favseller_list(request):
    """Function to build an HTML report of fav sellers"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            # Query for all sellers
            db_cursor.execute("""
                SELECT
                    c.id AS customer_id,
                    c.phone_number,
                    c.address,
                    u.first_name || ' ' || u.last_name AS customer_name,
                    au.first_name || ' ' || au.last_name AS seller_name
                FROM
                    bangazonapi_customer c
                LEFT JOIN 
                    bangazonapi_favorite f ON f.customer_id = c.id
                JOIN
                    auth_user u ON c.user_id = u.id
                LEFT JOIN
                    bangazonapi_customer cs ON f.seller_id = cs.id
                LEFT JOIN
                    auth_user au ON cs.user_id = au.id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "maker": "Bar Games",
            #                 "skill_level": 3,
            #                 "number_of_players": 4,
            #                 "gametype_id": 2
            #             }
            #         ]
            #     }
            # }

            fav_seller = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                seller = Customer()
                seller.seller_name = row["seller_name"]
                uid = row["customer_id"]

                # Store the user's id
                # uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in fav_seller:
                    # Add the current game to the `games` list for it
                    fav_seller[uid]['sellers'].append(seller)

                else:
                    # Otherwise, create the key and dictionary value
                    fav_seller[uid] = {}
                    fav_seller[uid]["id"] = uid
                    fav_seller[uid]["customer_name"] = row["customer_name"]
                    fav_seller[uid]["address"] = row["address"]
                    fav_seller[uid]["phone_number"] = row["phone_number"]
                    fav_seller[uid]["sellers"]= [seller]

        # Get only the values from the dictionary and create a list from them
        list_of_user_favs = fav_seller.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_favs.html'
        context = {
            'userfav_list': list_of_user_favs
        }

        return render(request, template, context)
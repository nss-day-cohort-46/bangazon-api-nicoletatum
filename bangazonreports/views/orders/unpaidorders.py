"""Module for generating all unpaid orders report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def unpaidorders_list(request):
    """Function to build an HTML report of Orders"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            # Query for all sellers
            db_cursor.execute("""
                SELECT
                    o.id,
                    sum(p.price) AS total,
                    u.first_name || ' ' || u.last_name AS seller_name
                FROM
                    bangazonapi_order o
                JOIN 
                    bangazonapi_customer c ON o.customer_id = c.id
                JOIN
                    auth_user u ON c.user_id = u.id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.product_id
                WHERE
                    payment_type_id IS NULL 
                GROUP BY
                o.id
            """)

            dataset = db_cursor.fetchall()

            unpaid_orders = {}

            for row in dataset:
                uid = row["id"]


                # create the key and dictionary value
                unpaid_orders[uid] = {}
                unpaid_orders[uid]["id"] = uid
                unpaid_orders[uid]["seller_name"] = row["seller_name"]
                unpaid_orders[uid]["total"] = row["total"]

        # Get only the values from the dictionary and create a list from them
        list_of_unpaid_orders = unpaid_orders.values()

        # Specify the Django template and provide data context
        template = 'orders/list_with_unpaidorders.html'
        context = {
            'unpaidorders_list': list_of_unpaid_orders
        }

        return render(request, template, context)
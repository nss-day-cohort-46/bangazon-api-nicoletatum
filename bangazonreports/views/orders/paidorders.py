"""Module for generating all unpaid orders report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def paidorders_list(request):
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
                    pm.merchant_name,
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
                JOIN 
                    bangazonapi_payment pm ON pm.id = o.payment_type_id
                GROUP BY
                o.id
            """)

            dataset = db_cursor.fetchall()

            paid_orders = {}

            for row in dataset:
                uid = row["id"]


                # create the key and dictionary value
                paid_orders[uid] = {}
                paid_orders[uid]["id"] = uid
                paid_orders[uid]["seller_name"] = row["seller_name"]
                paid_orders[uid]["total"] = row["total"]
                paid_orders[uid]["merchant_name"] = row["merchant_name"]
        # Get only the values from the dictionary and create a list from them
        list_of_paid_orders = paid_orders.values()

        # Specify the Django template and provide data context
        template = 'orders/list_with_paidorders.html'
        context = {
            'paidorders_list': list_of_paid_orders
        }

        return render(request, template, context)
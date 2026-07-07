"""Parameterized SQL query templates for DB-validation tests (see db_connection.py)."""

GET_ORDER_BY_ID = "SELECT * FROM wp_wc_orders WHERE id = :order_id"
GET_ORDER_STATUS = "SELECT status FROM wp_wc_orders WHERE id = :order_id"
GET_CUSTOMER_BY_EMAIL = "SELECT * FROM wp_users WHERE user_email = :email"
GET_PRODUCT_STOCK = "SELECT stock_quantity FROM wp_wc_product_meta_lookup WHERE product_id = :product_id"

# order_composite.py
from flask import Flask, request, jsonify
import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

@app.route("/order/checkout", methods=["POST"])
def checkout():
    data = request.json

    for item in data["items"]:
        inv_response = requests.get(f"http://localhost:5006/inventory/{item['id']}")

        print(f"Inventory API Response for {item['id']}: {inv_response.status_code} - {inv_response.text}")  # Debugging

        if inv_response.status_code != 200:
            return jsonify({
                "code": 400,
                "message": f"Error fetching inventory for {item['name']}"
            }), 400

        inv_data = inv_response.json()
        
        # ✅ Ensure we're correctly reading "numAvailable"
        if "data" in inv_data and isinstance(inv_data["data"], dict):
            available_stock = inv_data["data"].get("numAvailable", 0)  # ✅ Correct extraction
        else:
            available_stock = 0  # Fallback if the structure is wrong

        print(f"Checking numAvailable for {item['id']} - Available: {available_stock}, Requested: {item['quantity']}")  # Debugging

        if available_stock < item["quantity"]:
            return jsonify({
                "code": 400,
                "message": f"Insufficient numAvailable for {item['name']} (Available: {available_stock}, Requested: {item['quantity']})"
            }), 400

    # 2. Place the order via your order atomic service
    order_response = requests.post(
        "http://localhost:5003/api/orders/place", json=data
    )
    if order_response.status_code != 201:
        return jsonify({
            "code": 400,
            "message": "Error placing order"
        }), 400

    order_data = order_response.json()

    # 3. Initiate payment via your payment atomic service
    payment_payload = {
        "orderId": order_data["orderId"],
        "amount": data["totalPrice"],
        "items": data["items"]
    }
    payment_response = requests.post(
        "http://localhost:5004/api/payment/create", json=payment_payload
    )
    if payment_response.status_code != 201:
        return jsonify({
            "code": 400,
            "message": "Error initiating payment"
        }), 400

    payment_data = payment_response.json()

 

    # 5. Return a unified response with order and payment details
    return jsonify({
        "code": 201,
        "message": "Order placed, payment completed, and numAvailable updated",
        "orderId": order_data["orderId"],
        "sessionId": payment_data["sessionId"]
    }), 201

@app.route("/order/payment-success", methods=["POST"])
def payment_success():
    """Called by the frontend AFTER payment success to update order and inventory."""
    data = request.json  # Should contain orderId and session_id

    try:
        print(f"Received payment success request: {data}")

        # Fetch payment status
        payment_response = requests.get(f"http://localhost:5004/api/payment/status?session_id={data['session_id']}")
        print(f"Payment Status Response: {payment_response.status_code} - {payment_response.text}")

        if payment_response.status_code != 200:
            return jsonify({"code": 400, "message": "Error verifying payment status"}), 400

        payment_data = payment_response.json()
        if payment_data.get("status") != "complete":
            return jsonify({"code": 400, "message": "Payment not completed"}), 400

        print(f"Payment confirmed for order: {data['orderId']}")

        # Update order status
        update_order_response = requests.post(
            "http://localhost:5003/api/orders/update-payment",
            json={"orderId": data["orderId"], "paymentIntentId": data["session_id"]}
        )
        print(f"Order Update Response: {update_order_response.status_code} - {update_order_response.text}")

        if update_order_response.status_code != 200:
            return jsonify({"code": 400, "message": "Error updating order payment status"}), 400

        print(f"Order successfully marked as paid: {data['orderId']}")

        # Fetch order details to update inventory
        order_response = requests.get(f"http://localhost:5003/api/orders/{data['orderId']}")
        print(f"Order Details Response: {order_response.status_code} - {order_response.text}")

        if order_response.status_code != 200:
            return jsonify({"code": 400, "message": "Error fetching order details"}), 400

        order_data = order_response.json()
        if "data" not in order_data or "items" not in order_data["data"]:
            print(f"Invalid order data received: {order_data}")
            return jsonify({"code": 400, "message": "Invalid order data received"}), 400

        print(f"Order Items: {order_data['data']['items']}")

        #  Fetch stock from inventory service
        for item in order_data["data"]["items"]:
            print(f"Fetching inventory for {item['id']}...")

            # Get stock from inventory service
            inventory_response = requests.get(f"http://localhost:5006/inventory/{item['id']}")

            if inventory_response.status_code != 200:
                print(f"Error fetching stock for {item['id']}: {inventory_response.text}")
                continue  # Skip stock update if inventory fetch fails

            inventory_data = inventory_response.json()

            if "data" not in inventory_data or "numAvailable" not in inventory_data["data"]:
                print(f"Invalid inventory data received for {item['id']}: {inventory_data}")
                continue

            current_stock = inventory_data["data"]["numAvailable"]  # Get  field
            new_stock = max(current_stock - item["quantity"], 0)  # Prevent negative stock

            print(f"Updating numAvailable for {item['id']} - Current: {current_stock}, Ordered: {item['quantity']}, New: {new_stock}")

            update_payload = {"stock": new_stock}  # Keep this as "stock" since inventory API expects "stock"

            inv_update_response = requests.put(
                f"http://localhost:5006/inventory/{item['id']}", json=update_payload
            )

            print(f"Inventory Update Response for {item['id']}: {inv_update_response.status_code} - {inv_update_response.text}")

            if inv_update_response.status_code != 200:
                return jsonify({"code": 400, "message": f"Error updating stock for {item['name']}"}), 400

            print(f"numAvailable updated for {item['id']} - New stock: {new_stock}")

        return jsonify({"code": 200, "message": "Payment confirmed, order updated, and stock adjusted"}), 200

    except Exception as e:
        print(f"Error processing payment success: {str(e)}")
        return jsonify({"code": 500, "message": f"Error processing payment success: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5005, debug=True)

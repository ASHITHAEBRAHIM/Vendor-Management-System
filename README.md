# Vendor Management System
The Vendor Management System (VMS) is a comprehensive solution designed to streamline and optimize the management of vendors in an organization. It provides a centralized platform for businesses to efficiently handle vendor-related operations, from onboarding to performance evaluation.
## Features
- Vendor Onboarding: Simplify the process of adding new vendors to the system. Capture essential information such as contact details, vendor codes, and address.
- Performance Metrics: Track and evaluate vendor performance through key metrics like on-time delivery rates, quality ratings, average response times, and fulfillment rates.
- Purchase Order Management: Create and manage purchase orders seamlessly. Keep track of order dates, delivery dates, quantities, and order statuses.
- Acknowledgment: Allow vendors to acknowledge purchase orders, updating acknowledgment dates and triggering real-time recalculation of average response times.
- Metrics Calculation: Efficiently calculate and update vendor metrics using Django signals to ensure real-time updates when related data is modified.
## Acknowledgements
- Python 3.8
 - Django 3.1
 - Django REST Framework
 - My SQL
## Installation

Install my-project

```bash
cd my-project
mkvirtualenv vendor
pip install django
pip install django restframework
django -admin startproject vendor_management
cd vendor_management
python manage.py startapp vendor_app
python manage.py runserver 
  
```    
## Usage/Examples

```javascript
Start the Django development server:

    ```bash
    python manage.py runserver
    ```
    Open your web browser and navigate to (http://localhost:8000/admin/).
    Log in using the superuser account you created during the installation:

    ```bash
    python manage.py createsuperuser
    ```
    In the Django Admin Panel, you can perform the following actions:

   - **Vendors:** Manage vendor details, contact information, and performance metrics.
   - **Purchase Orders:** Create, update, and acknowledge purchase orders.
   - **Vendor Performance:** View performance metrics for vendors.
### Interacting with API Endpoints
1. Explore the available API endpoints:

   - **Vendors:** (http://localhost:8000/api/vendors/)
   - **Purchase Orders:** (http://localhost:8000/api/purchase_orders/)
   - **Vendor Performance:** (http://localhost:8000/api/vendor-performance/)

2. Use tools like [Postman](https://www.postman.com/) or `curl` to interact with the API endpoints.

### Acknowledging a Purchase Order via API
To acknowledge a purchase order via the API, use the following `curl` command:
```bash
curl -X POST http://localhost:8000/api/purchase_orders/{po_id}/acknowledge/ -d "po_id={po_id}"

## Authentication
This Vendor Management System uses token-based authentication to secure API endpoints. Follow the steps below to interact with authenticated endpoints:

### 1. Create a User Account

#### Use the Django Management Command to Create a User
Make a POST request to the Token Obtain API endpoint:
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/api/token/

```
## API Reference

#### Vendor Profile Management

```http
  POST/api/vendors
  GET/api/vendors
  GET /api/vendors/{vendor_id}
  PUT /api/vendors/{vendor_id}
  DELETE /api/vendors/{vendor_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api/vendors` | `string` | Create new vendors and List all vendors
 |api/vendors/{vendor_id} | `string` |  Retrieve, Update and Delete a specific vendor's details
 |
#### Purchase Order Tracking

```http
POST /api/purchase_orders
GET /api/purchase_orders
GET /api/purchase_orders/{po_id}
PUT /api/purchase_orders/{po_id}
DELETE /api/purchase_orders/{po_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api/purchase_orders` | `string` | Create Purchase Order and List all Purchase Orders
 |api/purchase_orders/{po_id} | `string` |  Retrieve, Update and Delete a specific Purchase Order
 |

#### Vendor Performance Evaluation
 ```http
GET /api/vendors/{vendor_id}/performance
POST /api/purchase_orders/{po_id}/acknowledge
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api/vendors/{vendor_id}/performance` | `string` | Retrieves the calculated performance metrics for a specific vendor
 |`api/purchase_orders/{po_id}/acknowledge` | `string` |  vendors to acknowledge POs
 |

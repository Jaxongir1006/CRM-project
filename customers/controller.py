from ninja_extra import api_controller, http_post, http_get, http_put, http_delete
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAdminManagerSales
from .models import Customer
from .schemas import (
    CustomerSchema,
    CreateCustomerSchema,
    ErrorSchema,
    UpdateCustomerSchema,
)
from typing import List
from ninja_extra.permissions import IsAuthenticated
from django.db.models import Q
import logging

logger = logging.getLogger("__name__")

@api_controller("/customers", auth=JWTAuth())
class CustomerController:

    @http_post(
        "/create/",
        response={201: CustomerSchema, 400: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def create_customer(self, request, data: CreateCustomerSchema):
        user = request.user
        try:
            customer = Customer.objects.create(
                **data.model_dump(exclude_unset=True), user=user
            )
        except Exception as e:
            logger.exception(f"{e}")
            return 400, {"error": str(e)}

        return 201, customer

    @http_get(
        "/",
        response=List[CustomerSchema],
        permissions=[IsAuthenticated],
        auth=JWTAuth(),
    )
    def get_customers(self, request):
        return Customer.objects.filter(Q(status=Customer.StatusEnum.ACTIVE) | Q(status=Customer.StatusEnum.POTENTIAL))

    @http_put(
        "/{customer_id}/",
        response={200: CustomerSchema, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def update_customer(self, request, customer_id: int, data: UpdateCustomerSchema):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return 404, {"error": "Customer not found"}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
        customer.save()

        return 200, customer

    @http_delete(
        "/{customer_id}/",
        response={200: dict, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def delete_customer(self, request, customer_id: int):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return 404, {"error": "Customer not found"}

        if request.user.role == "admin":
            customer.delete()
            return 200, {"message": "The customer has been deleted permanently"}

        if customer.status == Customer.StatusEnum.CLOSED:
            return 200, {"message": "This customer's status is already 'closed'"}

        return 200, {
            "message": "The customer's status has been changed to 'closed'\nIf you want to delete the customer permanently ask the admin"
        }

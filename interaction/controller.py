from ninja_extra import api_controller, http_post, http_get, http_put, http_delete, http_generic
from .schemas import InteractionSchema, CreateInteractionSchema, ErrorSchema, UpdateInteractionSchema
from .models import Interaction
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAdminManagerSales
from typing import List
from ninja_extra.permissions import IsAuthenticated
from customers.models import Customer
from django.db.models import Count


@api_controller("/interaction", auth=JWTAuth(), permissions=[IsAuthenticated])
class InteractionController:
    @http_post("/create/", response={201: InteractionSchema, 400: ErrorSchema},permissions=[IsAdminManagerSales])
    def create_interaction(self, request, data: CreateInteractionSchema):
        data = data.model_dump(exclude_unset=True)
        customer = data.pop("customer")
        try:
            customer = Customer.objects.get(id=customer)
        except Customer.DoesNotExist:
            return 400, {"error": "Customer not found"}
        data["customer"] = customer
        data["created_by"] = request.user
        try:
            interaction = Interaction.objects.create(**data)
        except Exception as e:
            return 400, {"error": str(e)}

        return 201, interaction
    
    @http_get("/", response=List[InteractionSchema])
    def get_interactions(self, request):
        return Interaction.objects.all()
    
    @http_get("/{interaction_id}/", response={200: InteractionSchema, 404: ErrorSchema})
    def get_interaction(self, request, interaction_id: int):
        try:
            interaction = Interaction.objects.get(id=interaction_id)
        except Interaction.DoesNotExist:
            return 404, {"error": "Interaction not found"}

        return 200, interaction
    
    @http_put("/{interaction_id}/", response={200: dict, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def update_interaction(self, request, interaction_id: int, data: UpdateInteractionSchema):
        try:
            interaction = Interaction.objects.get(id=interaction_id)
        except Interaction.DoesNotExist:
            return 404, {"error": "Interaction not found"}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(interaction, key, value)
        interaction.save()

        return 200, {
            "message": "The interaction has been updated",
            "interaction": InteractionSchema.from_orm(interaction)
        }

    @http_delete("/{interaction_id}/", response={200: dict, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def delete_interaction(self, request, interaction_id: int):
        try:
            interaction = Interaction.objects.get(id=interaction_id)
        except Interaction.DoesNotExist:
            return 404, {"error": "Interaction not found"}

        interaction.delete()
        return 200, {"message": "The interaction has been deleted permanently"}

    
    @http_get("/customer/{customer_id}/", response=List[InteractionSchema], permissions=[IsAdminManagerSales])
    def get_customer_interactions(self, request, customer_id: int):
        return Interaction.objects.filter(customer=customer_id)


    @http_get("/stats/by-user/", response=List[dict], permissions=[IsAdminManagerSales])
    def interaction_stats(self, request):
        return (
            Interaction.objects.values("created_by__username")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

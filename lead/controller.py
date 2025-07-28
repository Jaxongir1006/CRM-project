from ninja_extra import api_controller, http_post, http_get, http_put, http_delete
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAdminManagerSales
from .models import Lead,Deal
from .schemas import (
    LeadSchema,
    DealSchema,
    CreateLeadSchema,
    ErrorSchema,
    UpdateLeadSchema,
    CreateDealSchema,
    UpdateDealSchema,
    CloseDealSchema,
)
from typing import List
from ninja_extra.permissions import IsAuthenticated
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
import datetime

@api_controller('/lead', tags=['Lead'])
class LeadController:
    @http_get(
        "/",
        response=List[LeadSchema]
    )
    def get_leads(self, request):
        return Lead.objects.all()
    
    @http_post(
        "/create/",
        response={201: LeadSchema, 400: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def create_lead(self, request, data: CreateLeadSchema):
        user = request.user
        data = data.model_dump(exclude_unset=True)
        data["created_by"] = user
        try:
            lead = Lead.objects.create( **data)
        except Exception as e:
            return 400, {"error": str(e)}

        return 201, lead
    

    @http_put(
        "/{lead_id}/",
        response={200: LeadSchema, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def update_lead(self, request, lead_id: int, data: UpdateLeadSchema):
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return 404, {"error": "Lead not found"}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(lead, key, value)
        lead.save()

        return 200, lead
    

    @http_delete(
        "/{lead_id}/",
        response={200: dict, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def delete_lead(self, request, lead_id: int):
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return 404, {"error": "Lead not found"}

        lead.delete()

        return 200, {"message":"The lead has been deleted"}

    @http_get('/export/pdf/', response=dict)
    def lead_export_pdf(self, request):
        leads = Lead.objects.all()
        html_string = render_to_string("lead_pdf.html", {
            "leads": leads,
            "today": datetime.date.today(),
        })

        pdf_file = BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)

        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="leads.pdf"'
        return response

@api_controller("/deals", auth=JWTAuth(), tags=['Deal'], permissions=[IsAuthenticated])
class DealController:
    @http_post("/create/", response={201: DealSchema, 400: ErrorSchema}, permissions=[IsAdminManagerSales])
    def create_deal(self, request, data: CreateDealSchema):
        lead = Lead.objects.get(id=data.lead)
        if lead.status == Lead.StatusEnum.LOST:
            return 400, {"error":"The lead has been lost"}
        if not lead:
            return 400, {"error":"Lead not found"}
        data = data.model_dump(exclude_unset=True)
        data['lead'] = lead
        try:
            deal = Deal.objects.create(**data)
        except Exception as e:
            return 400, str(e)

        return 201, deal    

    @http_get("/", response=List[DealSchema])
    def get_deals(self, request):
        return Deal.objects.filter(status=Deal.StatusEnum.OPEN)
    
    @http_get("/{deal_id}/", response={200: DealSchema, 404:ErrorSchema})
    def get_deal(self, deal_id: int, request):
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            return 404, {"error":"Deal not found"}
        if deal.status == Deal.StatusEnum.LOST:
            return 404, {"error":"The deal has been lost"}
        return 200, deal
    
    @http_put("/update/{deal_id}/", response={200: dict, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def update_deal(self, deal_id: int, request, data: UpdateDealSchema):
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            return 404, {"error":"Deal not found"}
      
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(deal, key, value)
        deal.save()

        return 200, {"message":"The deal has been updated"}
    
    @http_delete("/delete/{deal_id}/", response={200: dict, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def delete_deal(self, deal_id: int, request):
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            return 404, {"error", "Deal not found"}
        deal.delete()

        return 200, {"message":"The deal has been deleted"}
    

    @http_post("/{deal_id}/close/", response={200: DealSchema, 404: ErrorSchema, 400: ErrorSchema}, permissions=[IsAdminManagerSales])
    def close_deal(self, request, deal_id: int, data: CloseDealSchema):
        try:
            deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            return 404, {"error": "Deal not found"}

        if data.status not in [Deal.StatusEnum.WON, Deal.StatusEnum.LOST]:
            return 400, {"error": "Invalid closing status"}

        deal.status = data.status
        deal.save()
        return 200, deal


@api_controller("/statistics", auth=JWTAuth(), tags=['Statistics'], permissions=[IsAuthenticated])
class StatisticsController:
    @http_get("/leads/stats/", response=dict)
    def lead_stats(self, request):
        return {
            "total": Lead.objects.count(),
            "new": Lead.objects.filter(status='new').count(),
            "converted": Lead.objects.filter(status='converted').count(),
        }
    
    @http_get("/deals/summary/", response=dict)
    def deal_summary(self, request):
        total = Deal.objects.count()
        won = Deal.objects.filter(status='won').count()
        lost = Deal.objects.filter(status='lost').count()
        open = Deal.objects.filter(status='open').count()
        return {
            "total": total,
            "won": won,
            "lost": lost,
            "open": open
        }

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from utils.permissions import IsAdminManagerSales
from .models import Reminder
from .schemas import ReminderSchema, CreateReminderSchema, ErrorSchema, UpdateReminderSchema
from ninja_jwt.authentication import JWTAuth
from customers.models import Customer
from typing import List
import logging

logger = logging.getLogger('__name__')

@api_controller('/reminder', auth=JWTAuth(), permissions=[IsAuthenticated])
class ReminderController:
    
    @http_get('/', response={200:List[ReminderSchema], 404:ErrorSchema})
    def get_reminders(self, request):
        reminders = Reminder.objects.all()
        if reminders.exists():
            return 200, reminders   
        return 404, {'error':"Not any reminders found"}
    
    @http_post('/create/', response={201: ReminderSchema, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def create_reminder(self, request, data: CreateReminderSchema):
        user = request.user
        data = data.model_dump(exclude_unset=True)
        data['user'] = user
        try:
            customer = Customer.objects.get(email=data['customer_mail'])
        except Customer.DoesNotExist:
            return 404, {'error': 'Customer with this email does not exist or it has been changed'}
        
        data['customer'] = customer
        data.pop('customer_mail')
        reminder = Reminder.objects.create(**data)
        logger.info(f"The new reminder created by {user}")
        return 201, reminder
    
    @http_put('/update/{reminder_id}/', response={200: ReminderSchema, 404: ErrorSchema, 400: ErrorSchema}, permissions=[IsAdminManagerSales])
    def update_reminder(self, reminder_id, request, data: UpdateReminderSchema):
        user = request.user
        try:
            reminder = Reminder.objects.get(id=reminder_id)
        except Reminder.DoesNotExist:
            logger.error(f"'{user}' This user tried to update reminder with fake id")
            return 404, {"error":"Reminder with this id does not exist or has been deleted"}
        if user != reminder.user or user.role != 'admin':
            logger.error(f"{user} This user tried to update the reminder, which does not belong to him/her")
            return 400, {"error": "You are not the one who created this reminder or you are not admin, so you cannot change or delete this reminder"}
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(reminder, key, value)
        logger.info(f"'{reminder}' This reminder has been updated by {user}")
        reminder.save()
        return 200, reminder


    @http_delete('/delete/{reminder_id}/', response={200: dict, 404: ErrorSchema, 400: ErrorSchema}, permissions=[IsAdminManagerSales])
    def delete_reminder(self, reminder_id, request):
        user = request.user
        try:
            reminder = Reminder.objects.get(id=reminder_id)
        except Reminder.DoesNotExist:
            logger.error(f"'{user}' This user tried to update reminder with fake id")
            return 404, {"error":"reminder with this id does not exist or has been deleted"}
            
        if user.role != 'admin' or user != reminder.user:
            return 400, {"error":"You are not the one who created this reminder or you are not admin, so you cannot change or delete this reminder"}
        
        reminder.delete()
        return 200, {'message':'The reminder has been deleted successfully'}
    
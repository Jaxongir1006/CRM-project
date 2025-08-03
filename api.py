from ninja_extra import NinjaExtraAPI
from users.controller import UserController
from customers.controller import CustomerController
from interaction.controller import InteractionController
from lead.controller import LeadController, DealController, StatisticsController
from tasks.controller import TaskController, MeetingController
from reminders.controller import ReminderController

api = NinjaExtraAPI(docs_url="/swagger/", openapi_url="/openapi.json")

api.register_controllers(
    UserController,
    CustomerController,
    InteractionController,
    LeadController,
    DealController,
    StatisticsController,
    TaskController,
    MeetingController,
    ReminderController,
)

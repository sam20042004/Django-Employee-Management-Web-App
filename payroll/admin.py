from django.contrib import admin
from .models import Leave,Employee,Contact,hrProfile,LeaveStatus,User

# Register your models here.
admin.site.register(Leave)
admin.site.register(Employee)
admin.site.register(Contact)
admin.site.register(hrProfile)
admin.site.register(LeaveStatus)
admin.site.register(User)

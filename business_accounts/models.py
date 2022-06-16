from datetime import datetime
from django.db import models
from user.models import User


class BusinessAccount(models.Model): # Аккаунт салона 
    admin = models.ForeignKey(User, on_delete=models.CASCADE) # Админ который привязан к салону и может вносить изменения 
    title = models.CharField(max_length=100)
    start_time = models.CharField(max_length=5) # начало работы салона
    end_time = models.CharField(max_length=5) # конец работы салона
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="") # главная фотка салона
    
    def __str__(self):
        return self.title

    @property
    def services(self): # Услуги салона
        review = SalonService.objects.filter(businessaccount = self)
        return [{'id': i.id, 'title': i.title,} for i in review]

    @property
    def rating(self): # Средний рейтинг салона
        p = 0
        for i in self.salon_reviews.all():
            p += int(i.stars)
        s = p/self.salon_reviews.all().count() if p/self.salon_reviews.all().count()!=0 else "None"
        return 
        # return SalonReviews.objects.filter(businessaccounts = self).aggregate(Avg('stars'))


    @property
    def reviews(self): # Отзывы
        reviews = SalonReview.objects.filter(businessaccount = self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars, 'user_id': i.user.id, 'user_name': i.user.name} for i in reviews]
    
    

STARS = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    ]
class SalonReview(models.Model): # Отзывы салона
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name='salon_reviews')
    text = models.TextField()
    stars = models.CharField(max_length=100, choices=STARS, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Staff(models.Model): # Работники салона
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to="")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    service_type = models.CharField(max_length=100)
    work_experience = models.CharField(max_length=100)
    review = models.TextField()
    def __str__(self):
        return self.name

    @property
    def stafftimetable(self):
        workday = StaffTimetable.objects.filter(staff = self)
        return [{'id': i.id, 'time_records': i.time_records}for i in workday]


    @property
    def reviews(self):
        reviews = StaffReview.objects.filter(staff = self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars, 'user_id': i.user.id, 'user_name': i.user.name} for i in reviews]




SERVICE_TYPE = [
    ('Фиксированная','Фиксированная'),
    ('Динамеческая', 'Динамечиская')
]
class SalonService(models.Model): # Услуги салона
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=SERVICE_TYPE)
    duration = models.TimeField()
    price = models.IntegerField() 
    price_2 = models.IntegerField(null=True, blank=True)
    # Цена зависит от типа если динамическая то цена от и до а если фиксированная тогда фиксированная
    # Поэтому две цены если фиксированная тогда выводим только 1 а если динамическая тогда 2 от и до
    # Если захотите сделать по другому делайте только скажите нам когда будите менять модельки

    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name='salon_services')
    staff = models.ManyToManyField(Staff, blank=True)
    # Услуга привязана к салону и к работникам которые могут сделать эту услугу
    def __str__(self):
        return self.title


Monday = 0
Tuesday = 1
Wednesday = 2
Thursday = 3
Friday = 4
Saturday = 5
Sunday = 6
class StaffTimetable(models.Model): # Расписание работников
    # Тут возможно будет много изменений в будущем так что работайте с этой моделькой в конце
    DAYS_OF_WEEK = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday')
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    day_off = models.PositiveIntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.staff.name

class TimeRecords(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    time =models.TimeField()


class Interior(models.Model): # Картинки салона
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")

class StaffWork(models.Model): # Картинки работ работников
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")

class StaffReview(models.Model): # Не знаю зачем но отдельные отзывы для Работников салона
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_reviews')
    text = models.TextField()

    stars = models.CharField(max_length=100, choices=STARS, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

STATUS_TYPE = [
    ("На прием", "На прием"),
    ("Подтвержден", "Подтвержден")
]
class Records(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    data = models.DateField()
    time = models.CharField(max_length=10)
    discount = models.TimeField(null=True, blank=True)
    price = models.IntegerField()
    promo_code = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(choices=STATUS_TYPE, max_length=100, default="На прием")
    businessaccount = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service = models.ForeignKey(SalonService, on_delete=models.CASCADE)


    @property
    def staff_info(self):
        return {'id': self.staff.id, 'name': self.staff.name}

class PromoCode(models.Model):
    promo_code = models.CharField(max_length=10)

    discount = models.IntegerField()
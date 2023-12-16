from django.db import models
from django.contrib.auth.models import User

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name = None, name = None, min_value = None, max_value = None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value,"max_value": self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
class Monitor(models.Model):
    model_name = models.SlugField(max_length=50, verbose_name="Название модели", help_text="Введите название модели", null=False, blank=False)
    diagonal = models.IntegerField(verbose_name="Размер диагонали", help_text="Введите размер диагонали", null=False, blank=False)
    color = models.CharField(max_length=50, verbose_name="Цвет", help_text="Введите цвет модели", null=False, blank=False)

    def __str__(self):
        return "Монитор " + self.model_name

    class Meta:
        db_table = "Monitor"
class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя заказчика", help_text="Введите имя заказчика", null=False, blank=False)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия заказчика", help_text="Введите фамилию заказчика", null=False, blank=False)
    address = models.CharField(max_length=100, verbose_name="Адрес", help_text="Введите адрес", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя", help_text="Выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Заказчик: " + self.first_name + " " + self.last_name + " " + self.address

    class Meta:
        db_table = "Customer"
class Provider(models.Model):
    first_name = models.CharField(max_length=50,  verbose_name="Имя поставщика", help_text="Введите имя поставщика", null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия поставщика", help_text="Введите фамилию поставщика", null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя", help_text="Выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Поставщик: " + self.first_name + " " + self.last_name

    class Meta:
        db_table = "Provider"

class Statistics(models. Model):
    monitor = models.ManyToManyField(Monitor)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Поставщик", null=False, blank=False)
    region = models.CharField(max_length=50, verbose_name="Регион поставки", help_text="Введите регион поставки",
                                  null=True, blank=True)

    def __str__(self):
        print(self.monitor.all())
        return (self.region) +" Мониторы: " + (", ".join([element.model_name for element in self.monitor.all()]))


class Order(models.Model):
    number = IntegerRangeField(max_value = 15, min_value=1,verbose_name="Номер заказа", null = False, blank = False)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, verbose_name="Монитор", null=False, blank=False)
    amount = models.IntegerField(verbose_name="Количество", null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Заказчик", null=False, blank=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Поставщик", null=False, blank=False)
    statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE, verbose_name="Статистика", null=True, blank=True)
    order_date = models.DateField(verbose_name="Дата получения", null=False, blank=False)

    def __str__(self):
        return "Заказ: " + self.monitor.__str__() + " Количество: " + self.amount.__str__() + "шт. Дата заказа: " + self.order_date.__str__()

    class Meta:
        db_table = "Order"

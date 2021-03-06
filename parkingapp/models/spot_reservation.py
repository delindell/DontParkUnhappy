from django.db import models
from django.shortcuts import reverse
from safedelete.models import SOFT_DELETE, SafeDeleteModel
from django.contrib.auth.models import User
from .spot import Spot
from .payment_type import PaymentType
from .vehicle import Vehicle

class SpotReservation(SafeDeleteModel):

    created_at = models.DateTimeField(auto_now_add=True)
    res_end_time = models.DateTimeField(auto_now_add=False)
    total_cost = models.IntegerField()
    spot = models.ForeignKey(Spot, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    _safedelete_policy = SOFT_DELETE

class Meta:
    verbose_name = ("spot_reservation")
    verbose_name_plural = ("spot_reservations")

    def __str__(self):
        return self.created_at

    def get_absolute_url(self):
        return reverse("spot_reservation_detail", kwargs={"pk": self.pk})

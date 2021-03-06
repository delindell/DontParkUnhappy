from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from parkingapp.models import Spot, Lot, Vehicle, PaymentType, SpotReservation
from ...helpers import check_reservation

@login_required
def lot_details(request, lot_id, user_id):
    if request.method == 'GET':

      check_reservation()

      lot = Lot.objects.get(pk=lot_id)

      lot.spots = Spot.objects.filter(lot_id=lot_id)

      payments = PaymentType.objects.filter(user_id=user_id)

      vehicles = Vehicle.objects.filter(user_id=user_id)

      reservations = SpotReservation.objects.filter(user_id=user_id)

      template = 'lots/detail.html'

      context = {
        'lot': lot,
        'payments': payments,
        'vehicles': vehicles,
        'reservations': reservations
      }

      return render(request, template, context)

    elif request.method == 'POST':

        form_data = request.POST

        if(
          'actual_method' in form_data
          and form_data['actual_method'] == 'DELETE'
        ):

            spot = Spot.objects.get(pk=int(form_data['spot_id']))
            spot.delete()

            return redirect(reverse('parkingapp:lot_details', args=[lot_id, user_id]))
            
        elif(
          'actual_method' in form_data
          and form_data['actual_method'] == 'PUT'
        ):

            spots = Spot.objects.filter(lot_id=lot_id)

            new_spot_number = len(spots) + 1

            for spot in spots:
                if spot.number == new_spot_number:
                    new_spot_number += 1

            new_spot = Spot.objects.create(
              number = new_spot_number,
              is_reserved = False,
              lot_id = lot_id
            )

            return redirect(reverse('parkingapp:lot_details', args=[lot_id, user_id]))

        
        lot = Lot.objects.get(pk=lot_id)

        """
        Getting number of hours reserved off of the form
        converting into an int, then getting current time and 
        adding the number of hours reserved to get the expiration
        time for the reservation
        """

        hours = int(form_data['num_of_hours'])
        current_time = datetime.now(tz=get_current_timezone())
        hours_added = timedelta(hours=hours)
        exp_time = current_time + hours_added

        """Calculating total cost of reservation based off hours reserved"""

        cost = lot.hourly_rate * hours

        spot = int(form_data['spot'])

        new_reservation = SpotReservation.objects.create(
          created_at = current_time,
          res_end_time = exp_time,
          total_cost = cost,
          spot_id = spot,
          payment_type_id = form_data['payment'],
          user_id = user_id,
          vehicle_id = form_data['vehicle']
        )

        spot_to_update = Spot.objects.get(pk=spot)
        spot_to_update.is_reserved = True
        spot_to_update.save()

        return redirect(reverse('parkingapp:reservation_confirmation', args=[new_reservation.id]))



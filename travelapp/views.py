from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import HotelForm, RoomForm, ChoiceForm
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SeatForm, FlightForm, CityForm, ReviewForm
from .models import BookFlight, BookHotel, BookPackage, Flights, Famous
from django.shortcuts import render, get_object_or_404
from .models import Hotels, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'index.html')


def hotel_view(request):
    form = HotelForm(request.POST or None)
    if form.is_valid():
        city = form.cleaned_data['city'].upper()
        date = form.cleaned_data['date']
        hotels = Hotels.objects.filter(city__city__icontains=city)
        response = {'date': date, 'Hotels': hotels, 'form': form}
        return render(request, 'hotels.html', response)
    context = {'form': form}
    return render(request, 'hotels.html', context)


def flight_view(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        source = form.cleaned_data['source'].upper()
        destination = form.cleaned_data['destination'].upper()
        date = form.cleaned_data['date']
        flights = Flights.objects.filter(source__iexact=source, destination__iexact=destination)
        response = {'date': date, 'Flights': flights, 'form': form}
        return render(request, 'flights.html', response)
    context = {'form': form}
    return render(request, 'flights.html', context)


@login_required
def hotel_submit(request, hotel=None, date=None, room=None):
    user = request.user
    b = BookHotel.objects.create(username_id=user, hotel_name=hotel, date=date, room=room)
    b.save()
    return redirect('dashboard')


@login_required
def cancel_hotel(request, hotel=None, date=None, room=None):
    hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()
    hotels = [hotel_obj]
    price = room * hotel_obj.hotel_price if hotel_obj else 1
    response = {'Hotel': hotels, 'price': price, 'room': room, 'date': date}
    return render(request, 'cancelhotel.html', response)


@login_required
def confirm_cancel_hotel(request, hotel=None, date=None, room=None):
    user = request.user
    BookHotel.objects.filter(username_id=user, hotel_name=hotel, date=date, room=room).delete()
    return redirect('dashboard')


@login_required
def dashboard(request):
    user = request.user
    flights = BookFlight.objects.filter(username_id=user)
    hotels = BookHotel.objects.filter(username_id=user)
    packages = BookPackage.objects.filter(username_id=user)
    response = {
        'flights': flights,
        'hotels': hotels,
        'packages': packages,
    }
    return render(request, 'dashboard.html', response)


@login_required
def submit_flight(request, flight_number=None, date=None, seat=None):
    user = request.user
    BookFlight.objects.create(username_id=user, flight=flight_number, date=date, seat=seat)
    return redirect('dashboard')

@login_required
def submit_package(request, flight=None, hotel=None, date=None, seat=None, room=None):
    user = request.user
    BookPackage.objects.create(username_id=user, flight=flight, seat=seat, hotel_name=hotel, room=room, date=date)
    return redirect('dashboard')

@login_required
def cancel_flight(request, flight=None, date=None, seat=None):
    flight_obj = Flights.objects.filter(flight_number=flight).first()
    flights = [flight_obj]
    price = seat * flight_obj.eprice
    response = {
        'Flight': flights,
        'price': price,
        'seat': seat,
        'date': date,
    }
    return render(request, 'cancelflight.html', response)

@login_required
def confirm_cancel_flight(request, flight=None, date=None, seat=None):
    user = request.user
    BookFlight.objects.filter(username_id=user, flight=flight, date=date, seat=seat).delete()
    return redirect('dashboard')

def package_view(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source'].upper()
            date = form.cleaned_data['date']
            destination = form.cleaned_data['destination'].upper()
            flights = Flights.objects.filter(source=source, destination=destination)
            famplaces = Famous.objects.filter(city__city__contains=destination)
            hotels = Hotels.objects.filter(city__city__contains=destination)
            response = {
                'form': form,
                'source': source,
                'Hotels': hotels,
                'Flights': flights,
                'date': date,
                'Famplace': famplaces,
            }
            return render(request, 'package.html', response)
    else:
        form = FlightForm()
        response = {'form': form}
        return render(request, 'package.html', response)

@login_required
def cancel_package(request, flight=None, seat=None, hotel=None, date=None, room=None):
    flight_obj = Flights.objects.filter(flight_number=flight).first()
    hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()
    flights = [flight_obj]
    hotels = [hotel_obj]
    price_flight = seat * flight_obj.eprice
    price_hotel = room * hotel_obj.hotel_price
    response = {
        'Flight': flights,
        'pricef': price_flight,
        'seat': seat,
        'Hotel': hotels,
        'priceh': price_hotel,
        'room': room,
        'date': date,
    }
    return render(request, 'cancelpackage.html', response)

@login_required
def confirm_cancel_package(request, flight=None, seat=None, hotel=None, date=None, room=None):
    user = request.user
    BookPackage.objects.filter(username_id=user, flight=flight, seat=seat, hotel_name=hotel, date=date, room=room).delete()
    return redirect('dashboard')

def places_view(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            famplaces = Famous.objects.filter(city__city__contains=city)
            response = {
                'form': form,
                'Famplace': famplaces,
            }
            return render(request, 'places.html', response)
    else:
        form = CityForm()
        response = {'form': form}
        return render(request, 'places.html', response)

def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = SignUpForm()
    response = {'form': form}
    return render(request, 'registration/register.html', response)


@login_required
def package_book(request, source=None, destination=None, date=None):
    form = ChoiceForm(request.POST)
    all_flights = Flights.objects.filter(source=source, destination=destination)
    all_hotels = Hotels.objects.filter(city__city__contains=destination)
    context = {'allflights': all_flights, 'allhotels': all_hotels, 'form': form}

    if request.method == "POST" and form.is_valid():
        flight_number = form.cleaned_data['flight'].upper()
        hotel_name = form.cleaned_data['hotel']
        seats = form.cleaned_data['seats']
        rooms = form.cleaned_data['rooms']

        if BookFlight.objects.filter(flight=flight_number, date=date).exists() or BookHotel.objects.filter(hotel_name=hotel_name, date=date).exists():
            return HttpResponse("This flight or hotel has already been booked")

        flight = Flights.objects.get(flight_number=flight_number)
        hotel = Hotels.objects.get(hotel_name=hotel_name)
        flights = [flight]
        hotels = [hotel]

        booked_flight_seats = BookFlight.objects.filter(flight=flight_number, date=date).aggregate(Sum('seat'))['seat__sum'] or 0
        booked_package_seats = BookPackage.objects.filter(flight=flight_number, date=date).aggregate(Sum('seat'))['seat__sum'] or 0
        seat_remain = flight.seats - booked_flight_seats - booked_package_seats

        booked_hotel_rooms = BookHotel.objects.filter(hotel_name=hotel_name, date=date).aggregate(Sum('room'))['room__sum'] or 0
        booked_package_rooms = BookPackage.objects.filter(hotel_name=hotel_name, date=date).aggregate(Sum('room'))['room__sum'] or 0
        room_remain = hotel.rooms - booked_hotel_rooms - booked_package_rooms

        context.update({
            'flavailability': "available" if seat_remain - seats > 0 else "unavailable",
            'havailability': "available" if room_remain - rooms > 0 else "unavailable",
            'pricef': seats * flight.eprice,
            'priceh': rooms * hotel.hotel_price,
            'seatsreq': seats,
            'roomreq': rooms,
            'seatrem': seat_remain,
            'roomrem': room_remain,
            'Flights': flights,
            'Hotels': hotels,
            'date': date,
        })
        context.update({
            'Flights': flights,
            'flavailability': "available" if seat_remain - seats > 0 else "unavailable",
            'seatrem': seat_remain,
            'pricef': seats * flight.eprice,
        })

        return render(request, 'bookpackage.html', context)

    return render(request, 'bookpackage.html', context)



@login_required
def book_flight(request, flight_number=None, date=None):
    if request.method == "POST":
        form = SeatForm(request.POST)
        if form.is_valid():
            flight = Flights.objects.filter(flight_number=flight_number).first()
            seats = form.cleaned_data['seats']
            booked_flights = BookFlight.objects.filter(flight=flight.flight_number).filter(date=date)
            booked_packages = BookPackage.objects.filter(flight=flight.flight_number).filter(date=date)
            price = seats * flight.eprice
            seat_remain = flight.seats
            flights = [flight]
            for j in booked_flights:
                cs = j.seat
                seat_remain -= cs
            for k in booked_packages:
                cs = k.seat
                seat_remain -= cs
            availability = "available" if (seat_remain - seats) > 0 else "unavailable"
            if not flight.separately_booked:
              response = {
                  'flight': flights,
                  'flight_number': flight_number,
                  'date': date,
                  'form': form,
                  'seat_remain': seat_remain,
                  'availability': availability,
                  'seatsreq': seats,
                  'price': price,
              }
              return render(request, 'bookflight.html', response)
            else:
              return HttpResponse("This flight has already been booked separately.")
    else:
        form = SeatForm()
    response = {'form': form}
    return render(request, 'bookflight.html', response)


@login_required
def hotel_book(request, hotel=None, date=None):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        room = form.cleaned_data['rooms']
        hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()
        if hotel_obj:
            book_hotels = BookHotel.objects.filter(hotel_name=hotel_obj, date=date)
            book_packages = BookPackage.objects.filter(hotel_name=hotel_obj, date=date)
            booked_rooms = sum([book.room for book in book_hotels]) + sum([book.room for book in book_packages])
            available_rooms = hotel_obj.rooms - booked_rooms
            availability = "available" if available_rooms >= room else "unavailable"
            price = room * hotel_obj.hotel_price
            hotels = [hotel_obj]

            if not hotel_obj.separately_booked:
              response = {'hotel': hotels, 'date': date, 'availability': availability,
                          'price': price, 'roomreq': room, 'roomrem': available_rooms, 'form': form}
              return render(request, 'bookhotel.html', response)
            else:
              return HttpResponse("This hotel has already been booked separately.")
    context = {'form': form}
    return render(request, 'bookhotel.html', context)



def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotels, pk=pk)
    reviews = Review.objects.filter(hotel=hotel)
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'reviews': reviews})



class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'add_reviews.html'

    def form_valid(self, form):
        form.instance.hotel_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("hotel_detail", kwargs={'pk': self.kwargs['pk']})


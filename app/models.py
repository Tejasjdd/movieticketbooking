from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=25, null=True)
	phone = models.CharField(max_length=13, null=True)

	def __str__(self):
		return self.name

class Theater(models.Model):
	name = models.CharField(max_length=25, null=True)
	description = models.CharField(max_length=100, null=True)
	address = models.CharField(max_length=30,null=True)
	no_of_screen = models.IntegerField(null=True)
	def __str__(self):
		return self.name

class Movie(models.Model):

	name = models.CharField(max_length=25, null=True, default="")
	duration = models.CharField(max_length=25, null=True, default="")
	genre = models.CharField(max_length=25, null=True, default="")
	release_date = models.CharField(max_length=20, null=True, default="")
	language_avail = models.CharField(max_length=50,null=True)
	shown_in_theater = models.ManyToManyField(Theater)	
	trailer = models.URLField(blank=True)
	image = models.ImageField(null=True,blank=True)
	def __str__(self):
		return self.name

class Shows(models.Model):
	name = models.CharField(max_length=25, null=True)
	theater = models.ForeignKey(Theater, null=True, on_delete= models.CASCADE)
	movie_shown = models.ForeignKey(Movie, null=True, on_delete= models.SET_NULL)
	language = models.CharField(max_length=50,null=True)
	screen = models.IntegerField(default=1)
	datetime = models.DateTimeField(null=True)
	def __str__(self):
		return self.name

class BookedSeat(models.Model):
	BOOKING_STATUS = (
		('BOOKED', 'BOOKED'),
		('AVAILABLE', 'AVAILABLE'), 
		('RESERVED','RESERVED'),
		('NOT_AVAILABLE','NOT_AVAILABLE')
	)

	seat_code = models.CharField(max_length=3, null=True)
	booking_status = models.CharField(max_length=25, null=True, choices=BOOKING_STATUS, default=BOOKING_STATUS[1][0])
	booked_by_customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	shows = models.ForeignKey(Shows, null=True, on_delete= models.SET_NULL)
	
	def __str__(self):
		return str(self.id)	

class Seat(models.Model):
    seat_choice = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no_of_seats = models.IntegerField(null=True)
    seat_code = models.CharField(max_length=20,null=True,blank=False)
    seat_type = models.CharField(max_length=8, choices=seat_choice, blank=False)
    show = models.ForeignKey(Shows, on_delete=models.CASCADE)
    total_amount = models.IntegerField(null=True)
    class Meta:
        unique_together = ('seat_code', 'show')

class Booking(models.Model):
    payment_choice = (
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
        ('Net Banking', 'Net Banking'),
        ('Wallet', 'Wallet'),
    )
    id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=11,default='Debit Card', choices=payment_choice)
    amount_paid = models.IntegerField(null=True)
    paid_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    paid_for = models.ForeignKey(Shows, on_delete=models.DO_NOTHING)

# Generated by Django 3.2.13 on 2022-05-08 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Born', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('ids', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=25, null=True)),
                ('duration', models.CharField(default='', max_length=25, null=True)),
                ('genre', models.CharField(default='', max_length=25, null=True)),
                ('language', models.CharField(max_length=50, null=True)),
                ('trailer', models.URLField(max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('cast', models.ManyToManyField(related_name='related', to='app.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=30, null=True)),
                ('no_of_screen', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shows',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25, null=True)),
                ('language', models.CharField(max_length=50, null=True)),
                ('screen', models.IntegerField(default=1)),
                ('datetime', models.DateTimeField(null=True)),
                ('total_seats', models.IntegerField(default=200)),
                ('movie_shown', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.movie')),
                ('theater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.theater')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='theaters',
            field=models.ManyToManyField(to='app.Theater'),
        ),
        migrations.CreateModel(
            name='BookedSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_seats', models.CharField(max_length=30, null=True)),
                ('booking_status', models.CharField(blank=True, choices=[('BOOKED', 'BOOKED'), ('AVAILABLE', 'AVAILABLE')], default='AVAILABLE', max_length=25, null=True)),
                ('booked_by_customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('shows', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked', to='app.shows')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_seats', models.IntegerField(blank=True, null=True)),
                ('seat_code', models.CharField(max_length=30, null=True)),
                ('seat_type', models.CharField(choices=[('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum')], max_length=200)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.shows')),
            ],
            options={
                'unique_together': {('seat_code', 'show')},
            },
        ),
    ]

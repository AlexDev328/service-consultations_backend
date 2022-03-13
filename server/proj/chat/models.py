from django.db import models

from consultations.models import Consultation, UserProfile


class Room(models.Model):
    consultaion = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    collocutors = models.ManyToManyField(UserProfile)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)
    text = models.TextField()


def create_room(insigator_id, consultant_id, consultation_id):
    room = Room.objects.create(consultation_id=consultation_id)
    room.collocutors.add(insigator_id)
    room.collocutors.add(consultant_id)
    room.save()

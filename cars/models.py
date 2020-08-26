from django.db import models


class VoteModel(models.Model):
    class Meta:
        abstract = True

    votes = models.PositiveIntegerField(default=0)
    sum_of_rates = models.PositiveIntegerField(default=0)

    def upvote(self, rate):
        self.votes += 1
        self.sum_of_rates += rate
        self.save()

    @property
    def average(self):
        if self.votes:
            return round((self.sum_of_rates / self.votes), 2)
        else:
            return 'Not rated yet'


class CarManager(models.Manager):
    def filter_by_popularity(self):
        return super().get_queryset().order_by('-votes')


class Car(VoteModel):
    make = models.CharField(max_length=120)
    model = models.CharField(max_length=120)

    objects = CarManager()

    def __str__(self):
        return '%s %s' % (self.make, self.model)

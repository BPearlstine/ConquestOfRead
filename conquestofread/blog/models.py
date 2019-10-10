from django.db import models
from django.dispatch import receiver


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class Blog(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    tags = models.ManyToManyField(Tag)

    def summary(self):
        return self.body[:200]

    def pub_day(self):
        return self.pub_date.strftime('%x')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


@receiver(models.signals.post_delete, sender=Blog)
def delete_periodic_tasks(sender, instance, *args, **kwargs):
    instance.image.delete()

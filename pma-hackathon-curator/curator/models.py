from django.db import models


class Persona(models.Model):
  name = models.CharField(max_length=20)

  def __str__(self):
    return self.name


class Gallery(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name_plural = 'Galleries'

  def __str__(self):
    return self.name


class GalleryActivity(models.Model):
  description = models.CharField(max_length=800)
  gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

  class Meta:
    verbose_name_plural = 'Gallery activities'
    unique_together = ('gallery', 'persona')

  def __str__(self):
    return '{} - {}'.format(self.gallery, self.persona)


class Artwork(models.Model):
  id = models.IntegerField(primary_key=True)
  gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  artist = models.CharField(max_length=50)
  thumbnail = models.CharField(max_length=100)
  fact = models.CharField(max_length=500)

  class Meta:
    verbose_name_plural = 'Artwork'

  def __str__(self):
    return self.title


class ArtworkAttribute(models.Model):
  artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
  key = models.CharField(max_length=100)
  value = models.CharField(max_length=300)
  weight = models.IntegerField()

  def __str__(self):
    return '{}:{}'.format(self.key, self.value)


class Visitor(models.Model):
  id = models.IntegerField(primary_key=True)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)


class ReactionType(models.Model):
  symbol = models.CharField(max_length=20, unique=True)
  value = models.IntegerField()

  def __str__(self):
    return self.symbol


class Reaction(models.Model):
  visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
  artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
  reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)

  def __str__(self):
    return '{} {} {}'.format(self.visitor, self.reaction_type, self.artwork)

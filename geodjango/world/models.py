from django.db import models

from django.contrib.gis.db import models

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    # def __unicode__(self):
    #     return self.name

    # class Meta:
    #     ordering = ['name']

class Stops(models.Model):

    # stop_name text NOT NULL,
    stop_name = models.CharField(max_length=50, blank=True)
    # commune_id integer NOT NULL,
    commune_id = models.IntegerField(blank=True)
    # commune_name text NOT NULL,
    commune_name = models.CharField(max_length=50, blank=True)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    mean_of_transport = models.CharField(max_length=20)


    class Meta:
        ordering = ['stop_name']

    def __str__(self):
        return f'{self.stop_name}, {self.commune_id}, {self.commune_name}'


class QuartiersCada(models.Model):
    numquartie = models.SmallIntegerField(blank=True)

    nomquartie = models.CharField(max_length=100)

    geom = models.GeometryField()
    # models.GeometryField(geography=False)

    class Meta:
        ordering = ['nomquartie']

    def __str__(self):
        return f'{self.numquartie}, {self.nomquartie}'


class SecteursCada(models.Model):
    numsecteur = models.SmallIntegerField(blank=True)

    nomsecteur = models.CharField(max_length=100)

    geom = models.GeometryField()
    # models.GeometryField(geography=False)

    class Meta:
        ordering = ['numsecteur']

    def __str__(self):
        return f'{self.numsecteur}, {self.nomsecteur}'


class IlotsCada(models.Model):
    idgothing = models.IntegerField(blank=True)

    numilot = models.IntegerField(blank=True)

    numsecteur = models.IntegerField(blank=True)

    nomsecteur = models.CharField(max_length=100)

    numquartie = models.IntegerField(blank=True)

    nomquartie = models.CharField(max_length=100)

    geom = models.GeometryField()
    # models.GeometryField(geography=False)

    class Meta:
        ordering = ['idgothing']

    def __str__(self):
        return f'{self.idgothing}, {self.numilot}'


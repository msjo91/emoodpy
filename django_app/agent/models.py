from django.db import models


class InstitutionManager(models.Manager):
    def create_inst(self, name):
        institution = self.model(name=name)
        institution.save(using=self._db)
        return institution

    class Meta:
        ordering = ('id',)


class Institution(models.Model):
    name = models.CharField(max_length=30)

    objects = InstitutionManager()


class TeamManager(models.Manager):
    def create_team(self, name, institution):
        team = self.model(name=name, institution=institution)
        team.save(using=self._db)
        return team


class Team(models.Model):
    name = models.CharField(max_length=30)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    objects = TeamManager()

    class Meta:
        ordering = ('institution',)

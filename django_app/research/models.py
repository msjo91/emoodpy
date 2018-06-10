from django.db import models


class InstitutionManager(models.Manager):
    def create_inst(self, name):
        institution = self.model(name=name)
        institution.save(using=self._db)
        return institution


class Institution(models.Model):
    name = models.CharField(max_length=50)

    objects = InstitutionManager()

    class Meta:
        ordering = ('name',)


class ProjectManager(models.Manager):
    def create_proj(self, title):
        proj = self.model(title=title)
        proj.save(using=self._db)
        return proj


class Project(models.Model):
    title = models.CharField(max_length=100)

    objects = ProjectManager()

    class Meta:
        ordering = ('title',)


class ProjGroupManager(models.Manager):
    def create_grp(self, name, proj):
        grp = self.model(name=name, proj=proj)
        grp.save(using=self._db)
        return grp


class ProjGroup(models.Model):
    name = models.CharField(max_length=100)
    proj = models.ForeignKey(Project, related_name='groups', on_delete=models.CASCADE)

    objects = ProjGroupManager()

    class Meta:
        ordering = ('name',)

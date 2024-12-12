# from django.db import models
# from django.core.validators import FileExtensionValidator

# class About(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()

# class SliderImage(models.Model):
#     image = models.ImageField(upload_to='slider_images/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
#     caption = models.CharField(max_length=200, blank=True, null=True)

# class TeamMember(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='team_members/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

# class FullWidthImage(models.Model):
#     image = models.ImageField(upload_to='full_width_images/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

# class MediaItem(models.Model):
#     image = models.ImageField(upload_to='media_items/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True, null=True)
#     videoUrl = models.URLField(blank=True, null=True)


# class FormSubmission(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name    
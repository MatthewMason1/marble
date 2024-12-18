# Generated by Django 5.1.2 on 2024-10-22 23:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_post_updated_at_userprofile_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "png"]
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="videos/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["mp4", "mov"]
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="banner",
            field=models.ImageField(
                default="default_banner.png",
                upload_to="banners/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "png"]
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(
                default="default_profile.png",
                upload_to="profile_pictures/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "png"]
                    )
                ],
            ),
        ),
    ]
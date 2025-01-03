# Generated by Django 5.1.2 on 2024-10-27 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0009_remove_message_recipient_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="chat_room",
        ),
        migrations.AlterUniqueTogether(
            name="contact",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="contact",
            name="user1",
        ),
        migrations.RemoveField(
            model_name="contact",
            name="user2",
        ),
        migrations.RemoveField(
            model_name="message",
            name="sender",
        ),
        migrations.RemoveField(
            model_name="publicmessage",
            name="room",
        ),
        migrations.RemoveField(
            model_name="publicmessage",
            name="sender",
        ),
        migrations.RemoveField(
            model_name="publicroom",
            name="participants",
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="description",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name="ChatRoom",
        ),
        migrations.DeleteModel(
            name="Contact",
        ),
        migrations.DeleteModel(
            name="Message",
        ),
        migrations.DeleteModel(
            name="PublicMessage",
        ),
        migrations.DeleteModel(
            name="PublicRoom",
        ),
    ]

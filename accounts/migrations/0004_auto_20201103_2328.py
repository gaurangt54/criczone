# Generated by Django 3.1.3 on 2020-11-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201103_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='tags',
            field=models.ManyToManyField(choices=[('Pending', 'Pending'), ('Out of Delivery', 'Out of Delivery'), ('Delivered', 'Delivered')], null=True, to='accounts.Tag'),
        ),
    ]

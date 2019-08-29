# Generated by Django 2.2.4 on 2019-08-10 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('intro', models.CharField(default='', max_length=511, verbose_name='介绍')),
                ('create_date', models.DateField(null=True, verbose_name='成立日期')),
                ('is_hot', models.BooleanField(default=False, verbose_name='是否热门')),
            ],
            options={
                'verbose_name': '学科',
                'verbose_name_plural': '学科',
                'db_table': 'tb_subject',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('detail', models.CharField(blank=True, default='', max_length=1023, verbose_name='详情')),
                ('photo', models.CharField(default='', max_length=1023, verbose_name='照片')),
                ('good_count', models.IntegerField(default=0, verbose_name='好评数')),
                ('bad_count', models.IntegerField(default=0, verbose_name='差评数')),
                ('subject', models.ForeignKey(db_column='sno', on_delete=django.db.models.deletion.PROTECT, to='vote.Subject', verbose_name='所属学科')),
            ],
            options={
                'verbose_name': '老师',
                'verbose_name_plural': '老师',
                'db_table': 'tb_teacher',
            },
        ),
    ]

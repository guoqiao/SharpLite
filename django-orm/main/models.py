#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):
    username = models.CharField()
    password = models.CharField()
    
    class Meta:
        db_table = 'User'
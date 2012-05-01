#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):
    username = models.CharField(default="", max_length=63)
    password = models.CharField(default="", max_length=63)
    
    class Meta:
        db_table = 'User'
#!/usr/bin/env python
# -*- coding: UTF8 -*-
# 
#   Jumping Qu @ BPO
#
#vim: ts=4 sts=4 et sw=4
#
import boto
import boto.ec2

conn = boto.connect_ec2()

def get_offerings(zone, typeOfInstance, maxOfDuration, description='Linux/UNIX'):
    offerings = conn.get_all_reserved_instances_offerings(instance_type=typeOfInstance, availability_zone=zone, product_description=description, max_duration=maxOfDuration, include_marketplace=True)
    for offering in offerings:
        print offering.id, second_day_month(offering.duration), float(offering.fixed_price), float(offering.usage_price),'/hourly'


def second_day_month(second):
    '''
    from second to day
    from day to month
    '''
    days = second/24/3600
    if days > 30:
        return "%d M" % (days/12)
    elif days < 0:
        return "%d S" % second
    else:
        return "%d D" % days

def main():
    '''
    '''
    get_offerings('us-east-1a', 'm1.small', 31536000)


if __name__ == '__main__':
    main()


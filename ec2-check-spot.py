#!/usr/bin/env python
# -*- coding: UTF8 -*-
# 
#   Jumping Qu @ BPO
#
#vim: ts=4 sts=4 et sw=4
#
import time
import datetime
import boto


format_time = "%Y-%m-%dT%H:%M:%S.000Z"

def cmpfloat(a,b):
    val =  int(a*10000) - int(b*10000) 
    if val < 0:
        return 1
    else:
        return 0

def fetchHistory(startTime,endTime,zoneName,conn=None,description='Linux/UNIX',instanceType='m1.small'):
    if not conn:
        conn = boto.connect_ec2()
    historys = conn.get_spot_price_history(start_time=startTime, end_time=endTime, availability_zone=zoneName, instance_type=instanceType,product_description=description)
    return historys

def caclTime(period):
    '''
    from now to int(period) days before
    INPUT:  period --int, 
    OUTPUT: now, now+period 
    '''
    #format_time = "%Y-%m-%dT%H:%M:%S.000Z"
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(int(period))
    return(start_time.strftime(format_time), end_time.strftime(format_time))

def comparePrice(historys):
    maxTime = 0.0
    minprice = 0.0
    maxprice = 0.0
    curprice = 0.0
    totalprice = 0.0
    prices = [ history.price for history in historys ]
    for history in historys:

        #the current time's value is the biggest one
        timee = time.mktime(datetime.datetime.strptime(history.timestamp, format_time).timetuple())
        if timee > maxTime:
           maxTime = timee
           currPri = history.price

        h = history.price
        if cmpfloat(h,minprice):
            minprice = h
        if cmpfloat(maxprice,h):
            maxprice = h
        totalprice += h

    average = totalprice / float(len(historys))
    #maxTime = datetime.datetime.fromtimestamp(int(maxTime)).strftime('%Y-%m-%d %H:%M:%S')

    return minprice, maxprice, average, currPri

def main(period, instanceType='m1.small'):
    '''
    '''
    conn = boto.connect_ec2()
    zones = conn.get_all_zones()
    print "\t Zone \t    \t minprice \t maxprice \t average \t current"
    for zone in zones:
        start, end = caclTime(period)
        historys = fetchHistory(start, end, zone.name, conn, 'Linux/UNIX', instanceType)
        priceTri = comparePrice(historys)
        print "\t %s" %zone.name, " \t %f    \t %f     \t %f    \t %f " %priceTri

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-d", "--days", type="int", help="from x day before", dest="days")
    parser.add_option("-t", "--instance_type", help="the type of instance", dest="instancetype")
    (options, args) = parser.parse_args()
    if options.days == None  or options.instancetype == None:
        import sys
        print "Please check your input."
        sys.exit()
    main(options.days, options.instancetype)



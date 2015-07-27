#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'ZhangHe'
import urllib2
import json

class Mrts:

    def __init__(self,mrtFile='',postFile=''):
        self.mrts = {}
        self.mrtFile = mrtFile
        self.postFile = postFile

    def getMrtsFromFile(self):
        if self.mrtFile == '':
            print 'Error'
            return
        fmrt = open(self.mrtFile,'r')
        for mrtName in fmrt.readlines():
            print 'Getting information of '+mrtName.strip()+" ..."
            mrtName = mrtName.strip().replace(' ','%20')
            query = mrtName +"%20mrt"
            mrtJson = self.getJsonbyQuery(query)
            placemark = mrtJson['Placemark'][0]
            point = placemark['Point']
            lat = point['coordinates'][1]
            lon = point['coordinates'][0]
            addressdetails = placemark['AddressDetails']
            addressline = addressdetails['Country']['AddressLine']
            mrtName = mrtName.replace('%20',' ')
            if(self.mrts.has_key(addressline) == False):
                self.mrts[addressline] = {}
            self.mrts[addressline]['lat'] = lat
            self.mrts[addressline]['lon'] = lon
            self.mrts[addressline]['short_name'] = mrtName
        fmrt.close()

    def getJsonbyQuery(self,query):
        url = 'http://gothere.sg/maps/geo?callback=&output=json&q='+query+'&client=&sensor=false'
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
        headers = {'User-Agent':user_agent}
        request = urllib2.Request(url,headers=headers)
        request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        response = urllib2.urlopen(request)
        html = response.read()
        jsonResult = json.JSONDecoder().decode(html)
        return jsonResult

    def findNearestMrt(self,lat=1,lon=103):
        result = ''
        m = 1000000
        for k in self.mrts:
            t = (self.mrts[k]['lat']-lat)**2 + (self.mrts[k]['lon']-lon)**2
            if t < m:
                m = t
                result = k
        return result

    def process(self):
        self.getMrtsFromFile()
        fp = open(self.postFile,'r')
        for postalcode in fp.readlines():
            postalcode = postalcode.strip()
            postalJson = self.getJsonbyQuery(postalcode)

            placemark = postalJson['Placemark'][0]
            point = placemark['Point']
            lat = point['coordinates'][1]
            lon = point['coordinates'][0]
            nearestMrt = self.findNearestMrt(lat,lon)
            print postalcode+"\t",
            print nearestMrt
        fp.close()

mrts = Mrts('mrt.txt','postalcode.txt')
mrts.process()
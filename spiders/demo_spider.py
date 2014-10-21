#Written by Zane Witherspoon
#9/22/2014
#Web scraping a yelp page for name, rating, number of reviews, and hours
import scrapy

from tutorial.items import YelpListing

class DemoSpider(scrapy.Spider):
	name = "demo"
	allowed_domains = ["yelp.com"]
	start_urls = [
		"http://www.yelp.com/biz/pasquales-pizza-san-francisco-2"
	]

	def parse(self, response):     #the initializating/only method
		
		item = YelpListing()	#Declairing the scraped item items.py contains YelpListing()
		


#REVIEWS
		#Start searching for number of reviews in path //div/span/span
		for sel in response.xpath('//div/span/span'):
			if sel.xpath('@itemprop').extract() == [u'reviewCount']:
				reviews = sel.xpath('text()').extract()
				print reviews
				item['reviews'] = reviews


#NAME

		#start searching for title in path //div/h1
		for sel in response.xpath('//div/h1'):
			if sel.xpath('@itemprop').extract() == [u'name']:
				title = sel.xpath('text()').extract()
				title[0] = title[0].encode('ascii', 'ignore')
				print title[0]
				item['name'] = title




#Ratings
		#finding the rating brings up multiple ratings, the first one is always the average
		x = 1	#used in finding only the first rating
		for sel in sel.xpath('//div'):
			if ((sel.xpath('@class').extract() == [u'biz-rating biz-rating-very-large clearfix']) & (x == 1)):
				rating = sel.xpath('.//div/meta/@content').extract()
				print rating
				x += 1	#changes the value of x so the following ratings are not saved
				item['rating'] = rating



#HOURS
		#begin scraping for hours table
		for sel in sel.xpath('//table'):		
			hours = sel.xpath('.//span/text()').extract()
			print "hours BEFORE editing"
			print hours

	

#Cleaning hours				
			#taking out the open/closed now item
			if u'Open now' in hours:
				hours.remove(u'Open now')
			elif u'Closed now' in hours:
				hours.remove(u'Closed now')
			

#Adding in closed values
			#adding closed as the open and close values on every day of the week
			#if monday is closed
			if u'<tr>\n                        <th scope="row">Mon</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(0, u'Closed')
				hours.insert(1, u'Closed')

			#if tuesday is closed
			if u'<tr>\n                        <th scope="row">Tue</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(2, u'Closed')
				hours.insert(3, u'Closed')

			#if wednesday is closed
			if u'<tr>\n                        <th scope="row">Wed</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(4, u'Closed')
				hours.insert(5, u'Closed')
				
			#if thursday is closed
			if u'<tr>\n                        <th scope="row">Thu</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(6, u'Closed')
				hours.insert(7, u'Closed')

			#if Friday is closed
			if u'<tr>\n                        <th scope="row">Fri</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(8, u'Closed')
				hours.insert(9, u'Closed')

			#if saturday is closed
			if u'<tr>\n                        <th scope="row">Sat</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(10, u'Closed')
				hours.insert(11, u'Closed')

			#if sunday is closed
			if u'<tr>\n                        <th scope="row">Sun</th>\n                        <td>\n                            Closed\n                        </td>\n                        <td class="extra">\n                        </td>\n                    </tr>' in sel.xpath('//table//tr').extract():
				hours.insert(12, u'Closed')
				hours.insert(13, u'Closed')


#finializing the hours item
		item['hours'] = hours




#yielding the results	
		yield item



#Writing all the data to a file
		filename = response.url.split("/")[-1]
		with open(filename, 'wb') as f:
			f.write(title[0])
			f.write("\n" + rating[0])	
			f.write("\n" + reviews[0] + "\n")
			for item in hours:
				f.write("%s\n" % item)

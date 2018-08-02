from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "FFEVWU54IYXWCWEFTGC5NIPKW0YRYG1ZFKS2HLWT0NUVVDLS"
foursquare_client_secret = "TU310KHMPH0MPZTMHG1F2NOJWU1011AMJVKCHXQA0KKIELG2"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	geo = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=%s&ll=%s,%s&near=%s' %
		(foursquare_client_id, foursquare_client_secret,"20180801", geo[0], geo[1], location))
	#3. Grab the first restaurant
	http = httplib2.Http()
	result = json.loads(http.request(url, 'GET')[1])
	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id']
		restaurant_name = restaurant['name']
		restaurant_addr = restaurant['location']['formattedAddress']
		addr = ''
		for a in restaurant_addr:
			addr+=a+" "
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' %
	       	(venue_id, foursquare_client_id, foursquare_client_secret))
		image_result = json.loads(http.request(url, 'GET')[1])
		print 'image result: ', image_result
	#5. Grab the first image
		if image_result['response']['photos']['items']:
			firstpic = image_result['response']['photos']['items'][0]
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix + "300x300" + suffix
		else:
	#6. If no image is available, insert default a image url
			imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
	#7. Return a dictionary containing the restaurant name, address, and image url	
		restaurant_info = {'name': restaurant_name, 'address': restaurant_addr, 'image': imageURL}
		return restaurant_info
	else:
		return 'No Restaurant Found'


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")

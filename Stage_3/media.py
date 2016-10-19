import webbrowser

class Movie():
	""" This part is accessible through media.Movie.__doc__
	"""

	# This is a class variable.
	VALID_GENRES = ["Animation", "Action", "Adventure", "Biography", "Drama", \
	"Comedy", "Thriller"]

	def __init__(self, movie_title, movie_trailer, movie_poster_image_url, \
		movie_quotes, movie_scene, movie_rating, movie_review):
		""" Here we have instance attributes.
		"""
		self.title = movie_title
		self.trailer_youtube_url = movie_trailer
		self.poster_image_url = movie_poster_image_url
		self.quotes = movie_quotes
		self.scene = movie_scene
		self.rating = movie_rating
		self.review = movie_review
	
	def show_quotes(self):
		"""This is an instance method.

		"""
		print "Some famous quotes: " + self.quotes[0]
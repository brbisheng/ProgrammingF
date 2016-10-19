import media
import fresh_tomatoes

# Now I will create several instances of movies based on the class \
# which I defined in media.py

# Create A Few Good Men Movie instance
a_few_good_men = media.Movie(
	movie_title = "A Few Good Men",
	movie_trailer = "https://www.youtube.com/watch?v=ePo91pMcu94",
	movie_poster_image_url = "http://i.imgur.com/KskDjyA.jpg",
	movie_quotes = ["Kaffee: [Stops Dawson as he is leaving the courtroom] Harold. Dawson: Sir? \
	Kaffee: You don't need to wear a patch on your arm to have honor. Dawson: Ten-hut! [salutes] \
	Dawson: There's an officer on deck."],
	movie_scene = "https://www.youtube.com/watch?v=_frM44bBMfA",
	movie_rating = "81%",
	movie_review = "Fighting authority, finding one's own path."
	)

# Create Forrest Gump Movie instance
forrest_gump = media.Movie(
	movie_title = "Forrest Gump", 
	movie_trailer = "https://www.youtube.com/watch?v=uPIEn0M8su0", 
	movie_poster_image_url = "http://i.imgur.com/bjYKqZF.jpg",
	movie_quotes = ["Forrest Gump: Stupid is as stupid does."],
	movie_scene = "https://www.youtube.com/watch?v=W7voy1vit6Y",
	movie_rating = "72%",
	movie_review = "Forrest Gump, while not intelligent, has accidentally been present at many historic moments, but his true love, Jenny Curran, eludes him."
	)

# Create The Shawshank Redemption Movie instance
the_shawshank_redemption = media.Movie(
	movie_title = "The Shawshank Redemption",
	movie_trailer = "https://www.youtube.com/watch?v=6hB3S9bIaco",
	movie_poster_image_url = "http://i.imgur.com/wWZy7Pc.jpg", 
	movie_quotes = ["Andy Dufresne: -in letter to Red- Remember Red, hope is a good thing, maybe the best of things, and no good thing ever dies."],
	movie_scene = "https://www.youtube.com/watch?v=Bjqmg_7J53s",
	movie_rating = "91%",
	movie_review = "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
	)

# Create Big Hero 6 Movie instance
big_hero_6 = media.Movie(
	movie_title = "Big Hero 6",
	movie_trailer = "https://www.youtube.com/watch?v=rD5OA6sQ97M",
	movie_poster_image_url = "http://i.imgur.com/lpdUE1D.jpg",
	movie_quotes = ["Can you feel it? You guys, do you feel this? Our origin story begins. We're gonna be superheroes!"],
	movie_scene = "https://www.youtube.com/watch?v=SRHU4264Xwc",
	movie_rating = "89%",
	movie_review = "The special bond that develops between inflatable robot Baymax, and prodigy Hamada, who team up with friends to form a band of high-tech heroes."
	)

# Create Eurotrip Movie instance
eurotrip = media.Movie(
	movie_title = "Eurotrip",
	movie_trailer = "https://www.youtube.com/watch?v=SeoX8MZd81E",
	movie_poster_image_url = "http://i.imgur.com/xRZTnGc.jpg",
	movie_quotes = ["Tibor: Enjoy Bratislava. It's good you came in summer, in winter it can get very depressing."],
	movie_scene = "https://www.youtube.com/watch?v=1HV-OSCFArI",
	movie_rating = "46%",
	movie_review = "Dumped by his girlfriend, a high school grad decides to embark on an overseas adventure in Europe with his friends."
	)

# Create The Grandmaster Movie instance
the_grandmaster = media.Movie(
	movie_title = "The Grandmaster",
	movie_trailer = "https://www.youtube.com/watch?v=BO1yfTfozhk",
	movie_poster_image_url = "http://i.imgur.com/57qvgch.jpg", 
	movie_quotes = ["Gong Er: My father would always say, people who practice martial arts go through three stages: seeing yourself, seeing the world, seeing all living beings."],
	movie_scene = "https://www.youtube.com/watch?v=iscP8gase1Q",
	movie_rating = "78%",
	movie_review = "The story of martial-arts master Ip Man, the man who trained Bruce Lee."
	)

# Create Groundhog Day Movie instance
groundhog_day = media.Movie(
	movie_title = "Groundhog Day",
	movie_trailer = "https://www.youtube.com/watch?v=tSVeDx9fk60",
	movie_poster_image_url = "http://i.imgur.com/jcpawB0.jpg", 
	movie_quotes = ["Phil: Well, what if there is no tomorrow? There wasn't one today."],
	movie_scene = "https://www.youtube.com/watch?v=SQLhORPoUJs",
	movie_rating = "96%",
	movie_review = "A weatherman finds himself living the same day over and over again. "
	) 

movies = [a_few_good_men, forrest_gump, the_shawshank_redemption, \
big_hero_6, eurotrip, the_grandmaster, groundhog_day]

fresh_tomatoes.open_movies_page(movies)
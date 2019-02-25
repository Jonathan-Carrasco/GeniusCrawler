# GeniusCrawler
My motivation for this program was to determine whether the popularity of Drakes music could be predicted with parameters like its duration, release year, whether it was explicit or not, and  whether any of the 15 most frequent words were associated with a more popular song. Popularity was determined using the number of Spotify plays for that song. This program takes url names and, after determining the 15 most frequent words, creates a word frequency dictionary with the word count of all 15 words for all songs in the song dictionary. After retrieving this dictionary, this program creates a csv file that contains information like song release year, duration, whether the song is explicit, number of spotify plays, and total word counts for top 15 songs.

# File Summary
The unfiltered csv file contains the 15 most frequent words, including stopwords. 
The filtered csv file contains the 15 most frequent words, excluding stopwords.
(This stopwords list can be found in the python file.)
Since Drake had a few songs that were very popular, these were considered outliers and made the regression models difficult to use. Therefore, I trimmed the outer 5% of songs based on spotify plays, and pdfs ending with wP shoud be read as "with these points" while pdfs ending with woP should be read as "without these points." All graphs were created using the filtered.csv file.


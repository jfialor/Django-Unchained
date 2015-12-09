import json
from lxml import etree

root = etree.Element("root")

with open('TMDBMovieInfo') as movie_file:
    for line in movie_file:
        movie = etree.SubElement(root, "movie")
        moviejson = json.loads(line)
        movieid = etree.SubElement(movie, "id")
        movieid.text = str(moviejson['id'])
        movieposter = etree.SubElement(movie, "posterurl")
        movieposter.text = moviejson['poster']

print(etree.tostring(root, pretty_print=True))

with open('posters_xml.xml', 'w') as posters_xml:
    posters_xml.write(etree.tostring(root, pretty_print=True))
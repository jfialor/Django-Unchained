import json

with open('TMDBMovieInfo') as movie_file:
    maxLen = 0
    for line in movie_file:
       movie = json.loads(line)
       if len(movie['overview']) > maxLen : 
            maxLen = len(movie['overview'])

with open('descriptions.sql', 'w') as descriptions:
    string = "ALTER TABLE Movie ADD description (varchar(%d));" % (maxLen)
    descriptions.write(string)
    with open('TMDBMovieInfo') as movie_file:
        for line in movie_file:
            movie = json.loads(line)
            string = """
            UPDATE Movie
            SET description = "%s"
            WHERE MovieID = %d ;
            """ % (movie['overview'].encode('utf-8'), movie['id'])
            print string
            descriptions.write(string)



        


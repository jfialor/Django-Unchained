from flask import Flask, render_template, request
from applicatio import db
from applicatio.forms import EnterDBInfo, RetrieveDBInfo, RetrieveRevenue, RetrieveMovie, MovieForm
import QueryTransform
import json
from Queue import PriorityQueue
import math
import untangle

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'  




def index():
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form)
    form3 = RetrieveRevenue(request.form)
    form4 = RetrieveMovie(request.form) 

        
    if request.method == 'POST' and form2.validate():
     #   data = form2.numRetrieve.data
      #  query_db  = db.engine.execute(data)
       # result = list(query_db)
        #num_return = 1
        #result = callTransform(2749)
        result = None
        movie_id = form2.numRetrieve.data
        print movie_id
        with open('try4.txt') as data_file:
            for line in data_file:
                data = json.loads(line)
                if data["id"] == int(movie_id):
                    tokens = data['tokens']
                    popularity = data['popularity']
                    releasedates = data['releasedates'].split('-')[0]
                    result = QueryTransform.QueryTransform(tokens, popularity, releasedates)
        if result is None:
            result = "Could not find ID"
        return render_template('results.html', results=result)  

    if request.method == 'POST' and form3.validate():
        result = []
        revenue = form3.numRetrieve22.data
        queue = PriorityQueue()
        with open('try4.txt') as data_file:
            for line in data_file:
                data = json.loads(line)
                queue.put((data['id'], data['revenue'], math.fabs(int(revenue) - data['revenue'])))
        for i in range(0, 9):
            if not queue.empty():
                result += [queue.get()]

        if len(result) is 0:
            result = ["Could not find revenue"]
        return render_template('results.html', results=result)              

    if request.method == 'POST' and form4.validate():
        result = []
        id_val = form4.numRetrieve23.data
        string = "select * from Movie where MovieId=" + id_val
        query_db  = db.engine.execute(string)
        result = list(query_db)

        if len(result) is 0:
            result = ["Could not find movie"]
        return render_template('results.html', results=result)              
    
    return render_template('index.html', form1=form1, form2=form2, form3=form3, form4=form4)

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def execute_query(query):
    return list(db.engine.execute(query))

def similar_rev(rev):
    if rev is 'NA':
        return []
    rev = int(rev)
    
    result = []
    queue = PriorityQueue()
    with open('try4.txt') as data_file:
        for line in data_file:
            data = json.loads(line)
            queue.put((math.fabs(int(rev) - data['revenue']), data['id']))
    for i in range(0, 4):
        if not queue.empty():
            result += [queue.get()]
    print result
    return result

@application.route('/movie', methods=['GET', 'POST'])
def movie():

    movie_id = request.args.get('number', '-1')




    obj = untangle.parse('posters_xml.xml')
    string = None
    query_db = None
    movie_data = {}
    if movie_id != -1 and movie_id != '-1':
        crew = execute_query('''select distinct p.name
    from HasCrew hc inner join Jobs j on j.jobid = hc.jobid inner join Person p on p.personID = hc.personID
    where hc.movieID = ''' + movie_id)
        crew = [i[0] for i in crew]

        actors = execute_query('''select distinct p.name from hascast a
        inner join Person p on a.personId = p.personID
    where a.movieid=''' + movie_id)
        actors = [i[0] for i in actors]

        studios = execute_query('''select distinct s.name from studio s
        join hasstudio h
            on h.studioid=s.studioid
    where h.movieid=''' + movie_id)
        studios = [i[0] for i in studios]


        keywords = execute_query('''select k.keyword from haskeyword k
    where k.movieid=''' + movie_id)
        keywords = [i[0] for i in keywords]

        characters = execute_query('''select p.name, a.role from hascast a
        inner join Person p on a.personId = p.personID
    where a.movieid=''' + movie_id)
        characters = [i[0] for i in characters]

        budget = execute_query('''select m.budget from movie m
    where m.movieid=''' +  movie_id)
        budget = [i[0] for i in budget][0]



        data = {u'actors':actors, u'crew': crew, u'studios':studios, u'keywords':keywords, u'characters':characters}
        string = "select * from Movie where MovieId=" + str(movie_id)
        query_db  = list(db.engine.execute(string))
        movie = query_db[0]

        
        for movie in list(obj.root.movie):
            if movie.id.cdata == movie_id:
                movie_xml = movie

        movie_data['name'] = query_db[0][1]
        movie_data['revenue'] = query_db[0][2] if str(query_db[0][2]) != '0' else 'N/A'
        movie_data['poster'] = movie_xml.posterurl.cdata
        movie_data['overview'] = movie_xml.overview.cdata


    else:
        movie_data['name'] = "Create Your Own"
        movie_data['revenue'] = 'N/A'
        movie_data['poster'] = ""
        movie_data['overview'] = "Type in figures to predict a custom movie"
        data = {u'actors':[], u'crew': [], u'studios':[], u'keywords':[], u'characters':[]}
        budget = 0

    form2 = MovieForm(request.form, field=json.dumps(data), budget=budget)
    similar_revs = similar_rev(movie_data['revenue']) if movie_data['revenue'] != 'N/A' else []
    similar_revs = [i[1] for i in similar_revs]
    similar_rev_posters = []
    for movie in list(obj.root.movie):
        if movie.id.cdata in similar_revs:
            similar_rev_posters += [[movie.id.cdata, movie.posterurl.cdata]]

    if request.method == 'POST' and form2.validate():
        form2 = MovieForm(request.form)
        json_data = form2.field.data
        all_data = json.loads(json_data)
        tokens = []

        stud_single = ["'" + i + "'" for i in all_data['studios']]
        studiosq = execute_query('''select s.studioid from studio s where s.name in ('''+','.join(stud_single)+''')''')
        studiosq = ["Studio"+str(i[0]) for i in studiosq]

        people = all_data['actors'] + all_data['crew']
        actors_single = ["'" + i + "'" for i in people]
        actorsq = execute_query('''select p.personid from person p where p.name in ('''+','.join(actors_single)+''')''')
        actorsq = ["Person"+str(i[0]) for i in actorsq]

        tokens = studiosq + actorsq + all_data['keywords'] + all_data['characters']
        print tokens
        print form2.budget.data
        


        return render_template('movie.html', movie=movie_data, form2=form2, similar=similar_rev_posters)

    else:
        form2 = MovieForm(request.form, field=json.dumps(data), budget=budget)

    return render_template('movie.html', movie=movie_data, form2=form2, similar=similar_rev_posters)

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])

@application.route('/select', methods=['GET', 'POST'])
def select():
    page_number = request.args.get('number', '1')
    number = int(page_number)
    next = "/select?number=" + str(number + 1)
    prev = number - 1 if number > 1 else 1
    prev = "/select?number=" + str(prev)
    obj = untangle.parse('posters_xml.xml')
    all_chunks = list(chunks(obj.root.movie, 3))
    start = 3 * (number - 1)
    end = start + 3
    results = all_chunks[start:end]
    pages = []
    if number < 6:
        pages = range(1,7)
    else:
        pages = range(number - 3, number + 4)
    pages_with_links = []
    for page in pages:
        if page == number:
            pages_with_links += [[page, "/select?number="+str(page), "active"]]
        else:  
            pages_with_links += [[page, "/select?number="+str(page), ""]]

    return render_template('select.html', results=results, pages=pages_with_links, next=next, prev=prev)

if __name__ == '__main__':
    application.run(host='0.0.0.0')




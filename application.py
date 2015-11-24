from flask import Flask, render_template, request
from applicatio import db
from applicatio.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form) 
    
    #if request.method == 'POST' and form1.validate():
        #data_entered = Data(notes=form1.dbNotes.data)
        #try:     
            #db.session.add(data_entered)
            #db.session.commit()        
            #db.session.close()
        #except:
            #db.session.rollback()
        #return render_template('thanks.html', notes=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        data = form2.numRetrieve.data
        query_db  = db.engine.execute(data)
        result = list(query_db)
        num_return = 1
        return render_template('results.html', results=result)                
    
    return render_template('index.html', form1=form1, form2=form2)

if __name__ == '__main__':
    application.run(host='0.0.0.0')

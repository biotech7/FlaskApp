# from flask import Flask, render_template
# from flask import session as login_session
# from sqlalchemy import create_engine, asc, desc
# from sqlalchemy.orm import sessionmaker
# from db_setup import *
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError
# import random, string
# import httplib2
# from flask import make_response, request, flash
# import json

from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import *

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read()
)['web']['client_id']


engine = create_engine('sqlite:///cars.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login - Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print "Token of clien ID doesn't match"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # if user not exist... make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
        'height: 300px;' \
        'border-radius: 150px;' \
        '-webkit-border-radius: 150px;' \
        '-moz-border-radius: 150px;"> '

    flash("you are now logged in as %s" % login_session['username'])
    # print 'Gconnect: Done.'
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        # print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # print 'In gdisconnect access token is %s', access_token
    # print 'User name is: '
    # print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print 'result is '
    # print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# homepage
@app.route('/')
@app.route('/catalog')
def showCatalog():
    companies = session.query(Company).order_by(asc(Company.name))
    autos = session.query(Cars).order_by(asc(Cars.name))
    return render_template(
        'catalog.html',
        companies=companies,
        autos=autos)


# Create a new brand/company
@app.route('/company/new/', methods=['GET', 'POST'])
def newCompany():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCompany = Company(name=request.form['name'],
                             user_id=login_session['user_id'])
        session.add(newCompany)
        session.commit()
        flash('New Company Created!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCompany.html')


# Edit a bran/company
@app.route(
    '/company/<int:company_id>/edit/',
    methods=['GET', 'POST'])
def editCompanies(company_id):
    editCompany = session.query(Company).filter_by(id=company_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editCompany.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this company." \
               " Please create your own company in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editCompany.name = request.form['name']
        session.add(editCompany)
        session.commit()
        flash("%s has been edited" % editCompany.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'editCompany.html',
            company_id=company_id, editCompany=editCompany)


# delete a brand/company
@app.route('/company/<int:company_id>/delete/', methods=['GET', 'POST'])
def deleteCompanies(company_id):
    deleteCompany = session.query(Company).filter_by(id=company_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deleteCompany.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to delete this company." \
               "Create your company in order to delete.');}</script>" \
               "<body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteCompany)
        session.commit()
        flash("%s has been deleted" % deleteCompany.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCompany.html', company=deleteCompany)


# Show autos
@app.route('/company/<int:company_id>/')
@app.route('/company/<int:company_id>/autos/')
def showAutos(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    creator = getUserInfo(company.user_id)
    autos = session.query(Cars).filter_by(company_id=company_id).all()
    l_g = login_session
    if 'username' not in l_g or creator.id != l_g['user_id']:
        return render_template('publicAutos.html',
                               company=company,
                               company_id=company_id,
                               autos=autos)
    else:
        return render_template(
            "Autos.html",
            company=company,
            company_id=company_id,
            autos=autos)


# Create Auto
@app.route('/company/<int:company_id>/autos/new', methods=['GET', 'POST'])
def newAuto(company_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCar = Cars(
            name=request.form['name'],
            Specifications=request.form['Specifications'],
            price=request.form['price'],
            company_id=company_id)
        session.add(newCar)
        session.commit()
        flash('New Car Created!')
        return redirect(url_for('showAutos', company_id=company_id))
    else:
        return render_template('newAuto.html', company_id=company_id)


# Edit auto
@app.route(
    '/company/<int:company_id>/autos/<int:car_id>/edit',
    methods=['GET', 'POST'])
def editAuto(company_id, car_id):
    if 'username' not in login_session:
        return redirect('/login')
    editCar = session.query(Cars).filter_by(id=car_id).one()
    company = session.query(Company).filter_by(id=company_id).one()
    if login_session['user_id'] != company.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit Auto to this company." \
               " Please create your own company in order to add auto.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editCar.name = request.form['name']
        if request.form['Specifications']:
            editCar.Specifications = request.form['Specifications']
        if request.form['price']:
            editCar.price = request.form['price']
        session.add(editCar)
        session.commit()
        flash("%s has been edited" % editCar.name)
        return redirect(url_for('showAutos', company_id=company_id))
    else:
        return render_template(
            'editAuto.html',
            company_id=company_id,
            car_id=car_id,
            editCar=editCar)


# Delete auyo
@app.route(
    '/company/<int:company_id>/autos/<int:car_id>/delete',
    methods=['GET', 'POST'])
def deleteAuto(company_id, car_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteCar = session.query(Cars).filter_by(id=car_id).one()
    company = session.query(Company).filter_by(id=company_id).one()
    if login_session['user_id'] != company.user_id:
        return "<script>function myFunction()" \
            " {alert('You are not authorized to delete auto to this company." \
            " Please create your own company in order to delete autos.');}" \
            "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteCar)
        session.commit()
        flash("%s has been Deleted" % deleteCar.name)
        return redirect(url_for('showAutos', company_id=company_id))
    else:
        return render_template('deleteAuto.html', car=deleteCar)


# JSON APIs
@app.route('/company/JSON')
def companiesJSON():
    company = session.query(Company).all()
    return jsonify(Company=[i.serialize for i in company])


@app.route('/company/<int:company_id>/autoss/<int:car_id>/JSON')
def autoJSON(company_id, car_id):
    car = session.query(Cars).filter_by(id=car_id).one()
    return jsonify(Cars=car.serialize)


@app.route('/company/<int:company_id>/autos/JSON')
def autosJSON(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    auto = session.query(Cars).filter_by(
        company_id=company_id).all()
    return jsonify(Cars=[i.serialize for i in auto])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

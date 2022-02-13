from flask import Blueprint, render_template, request, session

clear = Blueprint('clear', __name__)

@clear.route('/', methods=['GET','POST'])
def clear():

    if(request.method == 'POST'):
        session.clear()

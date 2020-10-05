from django.shortcuts import render, render_to_response, redirect
import tweepy
from django.http import *
from django.urls import reverse, path

API_key = "TWITTER API KEY"
API_key_secret = "TWITTER API KEY SECRET"


def index_view(request):
	print(request)
	if(checker(request)):
		print("Path is: ", request.path)
		print("Domain is: ", request.get_host())
		return redirect("http://" + request.get_host() + "/home")
		#return path('home/', dashboard)
	else:
		return render_to_response("login.html")


def checker(request):
	try:
		access_key = request.session.get('access_key', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True

def auth_view(request):
	OAuth = tweepy.OAuthHandler(API_key, API_key_secret)
	redirect_url = OAuth.get_authorization_url()
	response = HttpResponseRedirect(redirect_url)
	
	#print(response)
	request.session['request_token'] = OAuth.request_token
	print(OAuth.request_token)
	#return render("<h1>Hello</h1>")
	return response

def callback(request):
	pin = request.GET.get('pin')
	oauth = tweepy.OAuthHandler(API_key, API_key_secret)
	token = request.session.get('request_token')
	request.session.delete('request_token')
	oauth.request_token = token
	print("Token is", token)
	
	try:
		oauth.get_access_token(pin)
		request.session['access_key'] = oauth.access_token
		request.session['access_key_secret'] = oauth.access_token_secret
		api = tweepy.API(oauth)
		me = api.me()
		print(me.screen_name)
	except:
		print("Error Occured at views 43!")
	
	return redirect("http://" + request.get_host())
#
# return render(request,'index_view', {})
	#return render(request,'home.html',{})
#print(acess_token, acess_token_secret)

# Create your views here.

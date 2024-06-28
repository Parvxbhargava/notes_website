from website import createApp
#website is a python package as it has _init_ in it
app=createApp()
if __name__=='__main__': #defines that the app can only be executed in main and not in any other file where imported
  app.run(debug=True)
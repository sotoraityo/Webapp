from datetime import datetime,date

postdate="2023-10-18"
#postdate=datetime.strptime(postdate,"%Y-%m-%d")
#to=date.today()
to=date.today()
today=to.strftime("%Y-%m-%d")

if postdate==today:
    print("if through")
else:
    print("gard")
    
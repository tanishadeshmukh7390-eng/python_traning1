from flask import Flask

from app import collage_info

#HTML - Hardcoded HTMLcontent
'<a href="/student"> view Student</a>'

# Right way  url_for
'<a href = " '+url_for('students') +' ">view students</a>'

#url_for('student') will generate the URL for the student route defined in app.py.
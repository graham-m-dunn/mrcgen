#!/usr/bin/env python
import cgi
import os
import StringIO
import webapp2
import jinja2

import mrcgeninternals

jinja_environment = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
            </head>
            <body>
                <div id="stylized" class="myform">
                <form id="form" name="form" action="/workout" method="post">
                        <h1>MRC details</h1>
                        <label>Version</label>
                        <select name="version">
                        <option>1</option>
                        <option>2</option>
                        </select>
                        <label>Units</label> <select name="units">
                            <option>ENGLISH</option>
                            <option>METRIC</option>
                        </select>
                    <label>Description</label><textarea name="description" rows="1" cols="30"></textarea>
                    <label>Filename</label><textarea name="filename" rows="1" cols="30"></textarea>
                    <label>Workout</label><textarea name="content" rows="10" cols="60"></textarea>
                    <input type="submit" value="Generate">
                </form></div>
            </body>
        </html>""")

class Workout(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body><pre>')
        self.response.out.write(getraw( cgi.escape(self.request.get('version')),
                                        cgi.escape(self.request.get('units')), 
                                        cgi.escape(self.request.get('description')),
                                        cgi.escape(self.request.get('filename')),
                                        cgi.escape(self.request.get('content'))))
        self.response.out.write('</pre></body></html>')

def course_header(version, units, description, filename):
    """
    Print the standard MRC file header
    """
    return "[COURSE HEADER]\nVERSION = " + str(version) + "\nUNITS = " + str(units) + "\nDESCRIPTION = " + description + "\nFILE NAME = " + filename + "\nMINUTES PERCENTAGE\n[END COURSE HEADER]\n"

def course_data(final_workout):
    """
    Return the actual time/power data for the MRC
    file
    """
    fullmrc = ""
    fullmrc += "[COURSE DATA]\n"
    start_time = 0
    end_time = 0
    for interval in final_workout:
        fullmrc += "%f %f\n" % (start_time, interval[1])
        end_time += interval[0]
        fullmrc += "%f %f\n" % (end_time, interval[1])
        start_time = end_time
    fullmrc += "\n[END COURSE DATA]"
    return fullmrc

def getraw(version, units, description, filename, work):
    #workout_list = StringIO.StringIO(work)
    complete = ""
    #s = parse_input(workout_list.read())
    s = mrcgeninternals.parse_input(work)
    complete += course_header(version, units, description, filename)
    complete += course_data(s)
    return complete

app = webapp2.WSGIApplication(
        [('/', MainPage),
         ('/workout', Workout)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

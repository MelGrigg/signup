import cgi
import re
import webapp2

pageHead = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>
                Signup
            </title>
            <style>
                body {
                    font-family:tahoma, arial, calibri, sans-serif;
                    font-size:14px;
                }

                #holder {
                    margin:50px;
                }

                h1 {
                    font-size:24px;
                }

                .label {
                    text-align:right;
                }

                .error {
                    color:#D90000;
                }

                #welcome {
                    margin-top:100px;
                    text-align:center;
                    font-weight:normal;
                }
            </style>
        </head>
        <body>
"""

pageTail = """
        </body>
    </html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validUsername(username):
    return USER_RE.match(username)

def validPassword(password):
    return PASSWORD_RE.match(password)

def validEmail(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        error1 = self.request.get("error1")
        error2 = self.request.get("error2")
        error3 = self.request.get("error3")
        error4 = self.request.get("error4")
        username = self.request.get("username")
        email = self.request.get("email")
        pageTop = """
            <div id="holder">
                <h1>Signup</h1>
        """
        form = """
            <form action="/welcome" method="post">
                <table>
                    <tr>
                        <td class="label">
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input name="username" type="text" value="{0}" required />
                            <span class="error">{1}</span>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">
                            <label for="password">Password</label>
                        </td>
                        <td>
                            <input name="password" type="password" required />
                            <span class="error">{2}</span>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">
                            <label for="verify-password">Verify Password</label>
                        </td>
                        <td>
                            <input name="verify-password" type="password" required />
                            <span class="error">{3}</span>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">
                            <label for="email">Email (Optional)</label>
                        </td>
                        <td>
                            <input name="email" type="email" value="{4}" />
                            <span class="error">{5}</span>
                        </td>
                    </tr>
                </table>
                <input type="submit" value="Submit" />
            </form>
        """.format(username, error1, error2, error3, email, error4)
        pageBottom = """
            </div>
        """

        content = pageTop + form + pageBottom
        page = pageHead + content + pageTail
        self.response.write(page)

class WelcomeHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verPassword = self.request.get("verify-password")
        email = self.request.get("email")

        isUsernameValid = False
        isPasswordValid = False
        isVerifyPassValid = False
        isEmailValid = False

        errors = ["", "", "", ""]

        if validUsername(username):
            isUsernameValid = True
        else:
            errors[0] = "Invalid username."

        if validPassword(password):
            isPasswordValid = True
        else:
            errors[1] = "Invalid password."

        if verPassword == password:
            isVerifyPassValid = True
        else:
            errors[2] = "Passwords do not match."

        if email != "":
            if validEmail(email):
                isEmailValid = True
            else:
                errors[3] = "Invalid email."
        else:
            isEmailValid = True

        error = "?"
        first = True
        for i in range(len(errors)):
            if errors[i] != "":
                if first == False:
                    error += "&error{0}={1}".format(i + 1, errors[i])
                else:
                    error += "error{0}={1}".format(i + 1, errors[i])
                    first = False

        username = self.request.get("username")
        email = self.request.get("email")

        preserve = ""

        if not username == "" and not email == "":
            preserve += "&username={0}&email={1}".format(username, email)
        elif not username == "":
            preserve += "&username={}".format(username)
        else:
            preserve += "&email={}".format(email)

        if not error == "?":
            self.redirect("/{0}{1}".format(error, preserve))

        welcomeHeader = """
            <h1 id="welcome">Welcome, {}!</h1>
        """.format(cgi.escape(username, quote=True))

        response = pageHead + welcomeHeader + pageTail
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)

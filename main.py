
from flask import Flask, request, redirect, render_template, url_for
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>User SignUp</title>
    </head>
    <style>
        .error
            {
                "color: red";
            }
    </style>

    <body>
    <h3>User SignUp</h3>
    </body>
"""
page_footer = """
    </body>
</html>
"""

user_signup = """
      <!-- create your form here -->
        <form action="/" method = "post">
         <table>
            <tr>
                <td><label for="user">Username</label></td>
                <td>
                <input type="text" name="username" value="{username}"/>
                <p class="error">{username_error}</p>
                </td>
            </tr>
            <tr>
                <td><label for="pwd">Password</label></td>
                <td>
                <input type="password" name="password"/>
                <p class="error">{password_error}</p>
                </td>
            </tr>
            <tr>
                <td><label for="v_pwd">Verify Password</label></td>
                <td>
                <input type="password" name="vpassword"/>
                <p class="error">{pwd_mismatch_error}</p>
                </td>
            </tr>
            <tr>
                <td><label for="email">Email (optional)</label></td>
                <td>
                <input type="text" name="email" value="{email}"/>
                <p class="error">{email_error}</p>
                </td>
            </tr>
            </table>
            <br>
                <input type="submit">
        </form>
"""

def validate_username():
    form = user_signup
    username = str(request.form['username'])
    len_username = len(username)
    if space_in_text(username):
        username_space_error = "Please select a username without space."
        error = username_space_error
        #error = True
        return error
    if is_left_blank(username):
        username_blank_error ="Please donot leave this field blank."
        error = username_blank_error
        #error = True
        return error
    if check_str_length(len_username):
        min_str_length_error = "Please choose a username with length >3 and <20."
        error = min_str_length_error
        return error
    return None
def validate_password():
    form = user_signup
    password = str(request.form['password'])
    len_of_password = len(password)
    
    if check_str_length(len_of_password):
        password_len_error = "Please choose a password with length >3 and <20."
        error = password_len_error
        #error = True
        return error
    
    if is_left_blank(password):
        password_blank_error ="Please donot leave this field blank."
        error = password_blank_error
        #error = True
        return error
    return None

def password_mismatch():
    form = user_signup
    password = str(request.form['password'])
    verify_password = str(request.form['vpassword'])
    
    if not ( sorted(list(password)) == sorted(list(verify_password)) ):
        verify_mismatch_error ="Typed passwords donot match. Please try again."
        error = verify_mismatch_error
        return error
    
    if is_left_blank(verify_password):
        verify_blank_error ="Please donot leave this field blank."
        error = verify_blank_error
        return error
    return None

def validate_email():
    form = user_signup
    email = str(request.form['email'])
    len_email = len(email)
    if not email:
        return None
    if ('@' not in email) or ('.' not in email):
        email_missing_char_error ="Please provide a valid e-mail."
        error = email_missing_char_error
        return error
    if email.count('.') >1 or email.count('@')>1:
        email_dot_error = "No too many dots or @'s'"
        error = email_dot_error
        return error
    if space_in_text(email):
        email_space_error ="Please provide a valid e-mail."
        error = email_space_error
        return error
    if check_str_length(len_email):
        email_len_error ="Email is Too long...Please provide a valid e-mail."
        error = email_len_error
        return error
    return None


#'{0}'
#helper functions
    
def is_left_blank(text):
    if not text:
        return True;
    else:
        return False;


def space_in_text(text):
    if " " in text:
        return True;
    else:
        return False;
    

def check_str_length(length):
    if (length <3) or (length > 20):
        return True;
    else:
        return False;
#return redirect("/?error=" + error)  
@app.route("/", methods =['POST'])
def validate_user_signup():
    username_error = validate_username()
    password_error = validate_password()
    pwd_mismatch_error = password_mismatch()
    email_error = validate_email()
    #donno how to proceed after this.
    #errors = {'username_error': username_error,'password_error': password_error, 'pwd_mismatch_error': pwd_mismatch_error,'email_error': email_error}
    if username_error or password_error or pwd_mismatch_error or email_error:
        return redirect(url_for('index', username = request.form['username'],
        email= request.form['email'],
        username_error = username_error,
        password_error = password_error,
        pwd_mismatch_error = pwd_mismatch_error,
        email_error = email_error))

    return redirect(url_for('welcome', welcome_username=request.form['username']))
    #if using dictionary use this logic instead
    #return redirect('/', username=request.form['username'], email=request.form['email'])
@app.route("/welcome")
def welcome():
    welcome_username = request.args.get('welcome_username')
    #welcome_message = "Welcome..." + welcome_username 
    #return page_header + "<p>" + welcome_message + "</p>" + page_footer
    
    return render_template('welcome.html', welcome_username=welcome_username)
    
@app.route("/")
def index():
    #edit_header = "<h2>Edit My Watchlist</h2>"
    username = request.args.get('username') or ''
    email = request.args.get('email') or ''
    # if we have an error, make a <p> to display it
    username_error = request.args.get('username_error')
    if username_error:
        username_error = cgi.escape(username_error, quote=True)
        
    else:
        username_error = ''
    
    password_error = request.args.get('password_error')
    if password_error:
        password_error = cgi.escape(password_error, quote=True)
        
    else:
        password_error = ''

    pwd_mismatch_error = request.args.get('pwd_mismatch_error')
    if pwd_mismatch_error:
        pwd_mismatch_error = cgi.escape(pwd_mismatch_error, quote=True)
    else:
        pwd_mismatch_error = ''
    
    email_error = request.args.get('email_error')
    if email_error:
        email_error = cgi.escape(email_error, quote=True)
        
    else:
        email_error = ''
    
    errors = user_signup.format(username=username, email=email, username_error=username_error, password_error=password_error,pwd_mismatch_error=pwd_mismatch_error,email_error=email_error)

    # combine all the pieces to build the content of our response
    #main_content = edit_header + add_form + crossoff_form + error_element


    # build the response string
    content = page_header + errors + page_footer

    return content


app.run()
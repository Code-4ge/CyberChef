from flask import Flask, render_template, url_for, request, redirect, session, Response
from werkzeug.security import check_password_hash
from werkzeug.datastructures import  FileStorage
from werkzeug.utils import secure_filename
# from werkzeug import secure_filename, FileStorage
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import desc
import random
import math
import re
import os

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/cyberchef'

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/cyberchef'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_POST_IMG'] = 'static/img/post'
app.config['UPLOAD_BOOK_IMG'] = 'static/img/resource'
app.config['UPLOAD_FILE'] = 'static/img/resource/files'
app.secret_key = "This is Secret Key"
db = SQLAlchemy(app)

#login creadientials        ( CyberChef@gmail.com / this is Private@dont Login )
ID = "sha256$uexNTPRKsZzgwLEUp05y373yiqWxqOfoQcAF9UFZJpP7xhirH4gVyj9bo5jAFxI9wKv3TqMj2SX8PFSR$3f65b9db70038d77545480a18d6a5ed8d52eefc94ec145cf8394dcc50de4fe77"
Pass = "sha256$EBlvNWPfcoJdNtrOwRlP6QIopEG8Su44XRe5uxYrNKsPBC44EO8GyAgDkFwZH620ypngVZVSnhLRfSb1$e8025c266ec8519bc935b2b85075cb52d3a71713805f09bebc8be12f7e1009e4"

Img_Exts = ["jpg", "png", "jpeg"]

def check_file(file):
    return '.' in file and file.rsplit('.',1)[1].lower() in Img_Exts

def check_book_ext(file):
    return '.' in file and file.rsplit('.',1)[1].lower() == 'pdf'

class Contacts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40), nullable=False)
    Phone = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(40), nullable=False)
    Date = db.Column(db.String(20), nullable=False)
    Message = db.Column(db.Text, nullable=False)

class Posts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(40), nullable=False)
    Sub_title = db.Column(db.String(20), nullable=False)
    Image = db.Column(db.Text, nullable=False)
    Slug = db.Column(db.String(40), nullable=False)
    Date = db.Column(db.String(20), nullable=False)
    Content = db.Column(db.Text, nullable=False)

class Resources(db.Model):
    Srno = db.Column(db.Integer, primary_key=True)
    Book_Name = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    Details = db.Column(db.Text, nullable=False)
    Pages = db.Column(db.Integer, nullable=False)
    Size = db.Column(db.Float, nullable=False)
    Book = db.Column(db.Text, nullable=False)
    Categories = db.Column(db.Text, nullable=False)
    Images = db.Column(db.Text, nullable=False)

@app.template_filter('cleantag')
def get_content(content):
    clean = re.compile('<.*?>')
    content = re.sub(clean, '', content)
    return content

@app.route("/", methods=['GET', 'POST'])
def Home():
    post_category = set([])
    Post = Posts.query.order_by(desc(Posts.srno)).all()
    last = math.ceil(len(Post)/2)                  # 2 => total no. of posts in per-page
    f_list = len(Post)

    f_post = random.randint(0,f_list-2)            # 2 => total no. of featured post in per-page

    f_Posts = Post[(f_post):(f_post)+2]             # 2 => total no. of featured post in per-page

    for list in Post:
        post_category.add(list.Sub_title)

    page = request.args.get("page")
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    
    if request.method == 'POST':
        search = request.form.get('search')
        if search == "" or search == "All":
            Travel = True
            Post = Post[(page-1)*2:(page-1)*2+2]
        else:
            Travel = False
            Post = Posts.query.filter_by(Sub_title=search).all()
    else:
        Travel = True
        Post = Post[(page-1)*2:(page-1)*2+2]          # 2 => total no. of posts in per-page

    if last == 1:
        prev = "#"
        next = "#"
    elif page==1:
        prev = "#"
        next = "/?page=" + str(page+1)
    elif page==last:
        prev = "/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)

    return render_template("home.html", posts=Post, f_Post=f_Posts, trace=Travel, categorys=post_category, prev=prev, next=next)


# @app.route("/post", methods=['GET', 'POST'])
# def Post():
#     post_category = set([])
#     Post = Posts.query.order_by(desc(Posts.srno)).all()
#     last = math.ceil(len(Post)/2)                  # 2 => total no. of posts in per-page
#     f_list = len(Post)

#     f_post = random.randint(0,f_list-2)            # 2 => total no. of featured post in per-page

#     f_Posts = Post[(f_post):(f_post)+2]             # 2 => total no. of featured post in per-page

#     for list in Post:
#         post_category.add(list.Sub_title)

#     page = request.args.get("page")
#     if not str(page).isnumeric():
#         page = 1
#     page = int(page)
    
#     if request.method == 'POST':
#         search = request.form.get('search')
#         if search == "" or search in ["All", "all", "ALL"]:
#             Travel = True
#             Post = Post[(page-1)*2:(page-1)*2+2]
#         else:
#             Travel = False
#             Post = Posts.query.filter_by(Sub_title=search).all()
#     else:
#         Travel = True
#         Post = Post[(page-1)*2:(page-1)*2+2]          # 2 => total no. of posts in per-page

#     if last == 1:
#         prev = "#"
#         next = "#"
#     elif page==1:
#         prev = "#"
#         next = "/post?page=" + str(page+1)
#     elif page==last:
#         prev = "/post?page=" + str(page-1)
#         next = "#"
#     else:
#         prev = "/post?page=" + str(page-1)
#         next = "/post?page=" + str(page+1)

#     return render_template("post.html", posts=Post, f_Post=f_Posts, trace=Travel, categorys=post_category, prev=prev, next=next)

@app.route("/blogs/<string:blog_slug>", methods = ['GET'])
def Blog(blog_slug):
    Post = Posts.query.order_by(desc(Posts.srno)).all()
    blogs = Posts.query.filter_by(Slug=blog_slug).first()
    f_list = len(Post)
    f_post = random.randint(0,f_list-2)            # 2 => total no. of featured post in per-page
    f_Posts = Post[(f_post):(f_post)+2]             # 2 => total no. of featured post in per-page
    return render_template("blogs.html", posts=blogs, f_Post=f_Posts)
    # return render_template("blogs.html", posts=blogs, blog_slug=blog_slug)

@app.route("/resources", methods=['GET','POST'])
def Resource():
    book_category = set([])
    books = Resources.query.order_by(desc(Resources.Srno)).all()
    last = math.ceil(len(books)/2)                  # 2 => total no. of books in per-page
    
    for list in books:
        book_category.add(list.Categories)

    page = request.args.get("page")
    if not str(page).isnumeric():
        page = 1
    page = int(page)

    if request.method == 'POST':
        search = request.form.get("search")
        if search == "" or search == "Miscellaneous" or search in ["All", "all", "ALL"]:
            Travel = True
            books = books[(page-1)*2:(page-1)*2+2]
        else:
            Travel = False
            books = Resources.query.filter_by(Categories=search).all()
    else:
        Travel = True
        books = books[(page-1)*2:(page-1)*2+2]          # 2 => total no. of books in per-page

    if last == 1:
        prev = "#"
        next = "#"
    elif page==1:
        prev = "#"
        next = "/resources?page=" + str(page+1)
    elif page==last:
        prev = "/resources?page=" + str(page-1)
        next = "#"
    else:
        prev = "/resources?page=" + str(page-1)
        next = "/resources?page=" + str(page+1)

    return render_template("resources.html", Books=books, trace=Travel, categorys=book_category, prev=prev, next=next)

@app.route("/contact", methods = ['GET', 'POST'])
def Contact():
    if request.method == 'POST':
        # fetch data from file and add to database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        entrycontact = Contacts(Name=name, Phone=phone, Email=email, Date=datetime.now(), Message=message)
        db.session.add(entrycontact)
        db.session.commit()

    return render_template("contact.html")

@app.route("/privacy_policy")
def Privacy_Policy():
    return render_template("policy.html")

@app.route("/terms_and_conditions")
def Terms():
    return render_template("terms.html")

@app.route("/about")
def About():
    return render_template("about.html")

@app.route("/admin_loginauthenticate", methods = ['GET','POST'])
def Login():
    if request.method == 'POST':
        Uname = request.form.get("userid")
        Upass = request.form.get("pass")
        if(check_password_hash(ID,Uname) and check_password_hash(Pass,Upass)):
            session.permanent = False
            session['User'] = Uname
            return redirect(url_for("Dashboard"))
        else:
            return render_template("login.html", InValid='True')
    else:
        if 'User' in session:
            return redirect(url_for("Dashboard"))
        return render_template("login.html")

@app.route("/admin_loginauthenticate/dashboard")
def Dashboard():
    if 'User' in session:
        Post_table = Posts.query.order_by(desc(Posts.srno)).all()
        return render_template("dashboard.html", post_table=Post_table)
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/addpost", methods = ['GET', 'POST'])
def Addpost():
    if 'User' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            Tagline = request.form.get('sub_title')
            Url = request.form.get('slug')
            content = request.form.get('msg')
            Img = request.files['inputfile']
            Imgname = secure_filename(Img.filename)
            
            if Imgname == '':
                return render_template("add_post.html", error="Select File")
                
            if check_file(Imgname) == False:
                return render_template("add_post.html", error="Select File with Extension (.jpeg,.jpg,.png) only.")

            if Posts.query.filter_by(Slug=Url).first():
                return render_template("add_post.html", error="File Already Exist")

            path = os.path.join(app.config['UPLOAD_POST_IMG'], Imgname)
            Img.save(path)

            entrypost = Posts(Title=title, Sub_title=Tagline, Image=Imgname, Date=datetime.now(), Content=content, Slug=Url)
            db.session.add(entrypost)
            db.session.commit()

        return render_template("add_post.html")
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/edt/<string:id>", methods = ['GET','POST'])
def EditPost(id):
    if 'User' in session:
        edtit = Posts.query.filter_by(Slug=id).first()
        if request.method == 'POST':
            title = request.form.get('title')
            tag = request.form.get('sub_title')
            info = request.form.get('msg')
            edtit.Title = title
            edtit.Sub_title = tag
            edtit.Content = info
            db.session.commit()
            return redirect(url_for("Dashboard"))
        return render_template("edit_post.html", Post=edtit)
    else:
        return redirect(url_for("Login"))


@app.route("/admin_loginauthenticate/dashboard/del/<string:id>", methods = ['GET'])
def DeletePost(id):
    if 'User' in session:
        delit = Posts.query.filter_by(Slug=id).first()
        db.session.delete(delit)
        db.session.commit()
        return redirect(url_for("Dashboard"))
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/addresource", methods = ['GET', 'POST'])
def Addbook():
    if 'User' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            author = request.form.get('author')
            details = request.form.get('details')
            sub_title = request.form.get('sub_title')
            pages = request.form.get('pages')
            size = request.form.get('size')
            cover = request.files['cover']
            cover_name = secure_filename(cover.filename)
            pdf = request.files['inputfile']
            pdf_name = secure_filename(pdf.filename)
            
            if cover_name == '' or pdf_name == '':
                return render_template("add_book.html", error="Select Book Cover or File")
                
            if check_file(cover_name) == False:
                return render_template("add_book.html", error="Select Book Cover with Extension (.jpeg, .jpg, .png) only.")

            if check_book_ext(pdf_name) == False:
                return render_template("add_book.html", error="Select File with Extension .pdf only.")

            if Resources.query.filter_by(Book_Name=title).first():
                return render_template("add_book.html", error="Book Already Exist")

            cover_path = os.path.join(app.config['UPLOAD_BOOK_IMG'], cover_name)
            cover.save(cover_path)

            file_path = os.path.join(app.config['UPLOAD_FILE'], pdf_name)
            pdf.save(file_path)
            
            # Book_Name, Author, Details, Pages, Size, Book, Categories, Images
            # title, author, detalis, pages, size, pdf, sub_title, cover_name
            entryfile = Resources(Book_Name=title, Author=author, Details=details, Pages=pages, Size=size, Book=pdf_name, Categories=sub_title, Images=cover_name)
            db.session.add(entryfile)
            db.session.commit()

        return render_template("add_book.html")
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/books")
def Totalbook():
    if 'User' in session:
        resource = Resources.query.order_by(desc(Resources.Srno)).all()
        return render_template("books.html", files=resource)
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/books/del/<string:id>", methods = ['GET'])
def BooksDelete(id):
    if 'User' in session:
        delete = Resources.query.filter_by(Srno=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("Totalbook"))
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/grievance")
def Grievances():
    if 'User' in session:
        Logs = Contacts.query.order_by(desc(Contacts.srno)).all()
        return render_template("grievance.html", logs=Logs)
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/grievance/del/<string:id>", methods = ['GET'])
def GrievancesDelete(id):
    if 'User' in session:
        delete = Contacts.query.filter_by(Email=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("Grievances"))
    else:
        return redirect(url_for("Login"))

@app.route("/admin_loginauthenticate/dashboard/logout")
def Logout():
    session.pop('User', None)
    return redirect(url_for("Login"))

@app.route("/resources/preview/<string:fname>")
def Preview(fname):
    furl = url_for("static", filename="img/resource/files/" + fname)
    return f'<body style="margin:0;"><iframe src="{furl}" style="width:100%; height:100%; border:none;"></body>'

@app.errorhandler(403)
def error403(error):
    return render_template("error.html", error=403, head="ACCESS DENIED! IT LOOKS LIKE YOU'RE LOST", tail="Sorry, but you don't have permission to access requested page."), 403

@app.errorhandler(404)
def error404(error):
    return render_template("error.html", error=404, head="Oops!! YOU JUST MISSED THIS PAGE", tail="Hakuna-Matata! Try searching for something else."), 404

@app.errorhandler(405)
def error403(error):
    return render_template("error.html", error=405, head="UNFORTUNATELY, SOMETHING HAS GONE WRONG", tail="We're unable to fulfill your reqest. Try to reload page again."), 405

@app.errorhandler(500)
def error500(error):
    return render_template("error.html", error=500, head="SORRY :( OUR SERVER IS ON A BREAK", tail="It's not you - it's we, We have a problem. Please visit again later."), 500

if __name__=="__main__":
    app.run(debug=True)

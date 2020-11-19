from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
import email_validator
# Proje Adı     : USBlog | Flask Öğreniyorum
# Versiyon      : V0.01
# Proje Amacı   : Flask Python Öğrenmek
# Yazılımcı     : Uğur Semizoğlu #
# Kullanıcı Kayıt Formu Başlangıcı #

# Kullanıcı Giriş Decoratorı #
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu Sayfayı Görüntülemek İçin Lütfen Giriş Yapın","danger")
            return redirect(url_for("login"))
    return decorated_function
class RegisterForm(Form):
    name = StringField("İsim Soyisim",validators=[validators.length(min= 4,max= 25)])
    username = StringField("Kullanıcı Adı",validators=[validators.length(min= 5,max= 35)])
    email = StringField("Email",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola",validators=[
        validators.DataRequired(message = "Lütfen Bir Parola Belirleyiniz."),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula")
# Kullanıcı Kayıt Formu Bitişi #
# Kullanıcı Giriş Formu Başlangıcı #
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")
# Kullanıcı Giriş Formu Bitişi #
app = Flask(__name__)
app.secret_key = "USBlog"

app.config["MYSQL_HOST"] = "ugursemizoglu.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "ugursemizoglu"
app.config["MYSQL_PASSWORD"] = "2530--ugur"
app.config["MYSQL_DB"] = "ugursemizoglu$usblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where author = %s order by id desc"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)
    else:
        return render_template("dashboard.html")

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash(message="Başarıyla Kayıt Oldunuz",category="success")
        return redirect(url_for("login"))
    else:
       return render_template("register.html",form = form)

@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered =  form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * from users where username=%s"
        sonuc = cursor.execute(sorgu,(username,))
        if sonuc > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarı İle Giriş Yaptınız","success")
                session["logged_in"] = True
                session["username"] = username

                return redirect(url_for("index"))
            else:
                flash("Parolanızı Yanlış Girdiniz","danger")
                return redirect(url_for("login")) 
        else:
            flash("Böyle bir kullanıcı bulunmuyor","danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html",form = form)

# Çıkış Yap İşlemi #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/addarticle",methods = ["GET","POST"])
@login_required
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        author = session["username"]
        cursor = mysql.connection.cursor()
        sorgu = "Insert into articles(title,content,author) VALUES(%s,%s,%s)"
        cursor.execute(sorgu,(title,content,author))
        mysql.connection.commit()
        cursor.close()
        flash("Makale Başarıyla Kayıt Edildi","success")
        return redirect(url_for("dashboard"))
    else:
        flash("Bir Hata Oluştu","danger")
        return render_template("addarticle.html",form = form)

# Makale Form #
class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators=[validators.Length(min = 5,max =100)])
    content = TextAreaField("Makale İçeriği",validators=[validators.Length(min = 10)])

@app.route("/articles")
@login_required
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles order by id desc"
    result = cursor.execute(sorgu)

    if result > 0:
        articles = cursor.fetchall()

        return render_template("articles.html",articles = articles)
    else:
        return render_template("articles.html")

# Detay Sayfası #
@app.route("/article/<string:id>")
@login_required
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where id = %s"
    result = cursor.execute(sorgu,(id,))
    
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")

# Makale Silme Sayfası #
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where author = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    
    if result > 0:
        sorgu2 = "Delete from articles where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("Bu Makaleyi Silmeye Yetkiniz Bulunmuyor veya Böyle Bir Makale Bulunmamaktadır.","danger")
        return redirect(url_for("index"))

# Makale Güncelleme Sayfası #
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where id = %s and author = %s"
        result = cursor.execute(sorgu,(id,session["username"]))

        if result == 0:
            flash("Böyle bir makale yok veya bu işleme yetkiniz bulunmamaktadır.","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form=form)
    else:
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data

        sorgu2 = "Update articles set title = %s,content = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newTitle,newContent,id))
        mysql.connection.commit()
        flash("Makale Başarıyla Güncellendi","success")
        return redirect(url_for("dashboard"))

# Makale Arama Sayfası #
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where title like '%"+ keyword +"%'"
        result = cursor.execute(sorgu)
        if result == 0:
            flash("Aranan kelimeye uygun makale bulunamadı","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)
        
if __name__ == "__main__":
    app.run(debug=True)



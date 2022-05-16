from datetime import timedelta
import json
import os

from random import randint
import uuid
from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import login_required,current_user
from flask import session
from .models import Image, User, Note
from . import db
from . import create_app
from werkzeug.utils import secure_filename #for secure file

views= Blueprint('views',__name__, template_folder='../templates', static_folder='../static')



app = create_app()
app.config['UPLOAD_FOLDER']="static/images/"
app.config['POST_FOLDER']="static/images/post/"

app.permanent_session_lifetime= timedelta(hours=2)



#allowed Extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#main page
@views.route('/',methods=['GET','POST'])
def home():

    if "user_id" in session:
        userId=current_user.id
        
        id=session["user_id"]
        print(id)
        print(userId)
        if id ==int(userId):
            user=current_user
            session["user_name"]=user.user_name
            note=user.notes

            if request.method =='POST':
                note=request.form.get('note')
                if len(note) <1:
                    flash('Note is too short!', category='error' )
                else:
                    new_note=Note(data=note , user_id =user.id)
                    db.session.add(new_note)
                    db.session.commit()
                    flash('NOTE created!',category='success')
                    return redirect('/posts')    
    else:
        return redirect(url_for('auth.login'))
         
    return render_template('home.html',notes=note)







@views.route('/posts',methods=['GET','POST'])
@login_required
def posts():
        
        notes=Note.query.order_by(Note.date)
        images=Image.query.order_by(Image.date)
        # session["notes"]=Note.query.order_by(Note.date)
        # session["images"]=Image.query.order_by(Image.date)
        

        return render_template('posts.html',notes=notes,images=images)
        
    
    
    
    
    
    

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    user=current_user

    images =user.profile_pic

    if request.method == 'POST':
        bio=request.form.get('Bio')
        name=request.form.get('Name')
        # number=request.form.get('Number')
        pic = request.files['pic']
        
        if len(name) <1:
                flash('Name is too short!', category='error' )    
                
        elif len(bio) <1:
                flash('BIO is too short!', category='error' ) 

        
        else:
            if pic and allowed_file(pic.filename):
      
                filename = secure_filename(pic.filename)
                num=str(randint(00000000, 99999999))
                user=current_user       
                pic_name = str(uuid.uuid1()) + "_" + num+ "_" +filename       
                print("filename:",pic_name)
                try:
                    img=user.profile_pic
                    print("Profile Name:",img)
                    
                    
                    if img != "Default/Default.jpeg":
                        print("imageName:",img)
                        path=app.config['UPLOAD_FOLDER']+img
                        os.remove(path)

                        user.bio = bio
                        user.name = name                    
                        user.profile_pic = pic_name
                        db.session.commit()
                        flash("Pic_added")
                        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                        return redirect('/profile')
                    
                    
                    elif img == "Default/Default.jpeg":
                        user.bio = bio
                        user.name = name                    
                        user.profile_pic = pic_name
                        db.session.commit()
                        flash("Pic_added")
                        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                        return redirect('/profile')

                except:
                    flash ("Somthing error" ,category="error")
                    
            else:
                    user.bio = bio
                    user.name = name                   
                    db.session.commit()

    return render_template('profile.html',images=images)



#upolad a image

@views.route('/upload',methods=['POST'])
@login_required
def upload():
        pic = request.files['pic']
        caption= request.form.get('caption')
        print("caption:",caption)
        if pic.filename == '':
            flash('No image selected for uploading')
            return redirect('/potos')
  
  
  
  
        if pic and allowed_file(pic.filename):
      
            user_id=current_user.id
       
            filename = secure_filename(pic.filename)
       
            num=str(randint(00000000, 99999999))
       
            pic_name = str(uuid.uuid1()) + "_" + num+ "_" +filename       
            print("filename:",pic_name)
        
            pic.save(os.path.join(app.config['POST_FOLDER'], pic_name))
       
            mimetype=pic.mimetype
            print("MIMe: ",mimetype)
       
            photo=Image(mimetype=mimetype,img_name=pic_name,caption=caption,user_id=user_id )
            db.session.add(photo)
            db.session.commit()
            flash('Image added !',category='success')
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
    
        return redirect('/posts')




#Delete Note


@views.route('/delete-note',methods=['POST'])
@login_required
def delete_note():
    print("note")
    note = json.loads(request.data)
    noteID= note['noteId']
    print("type:",type(noteID))
    note=Note.query.get(noteID)
    
    if note:
    
        if note.user_id ==current_user.id  or  session["user_id"]==1:
            db.session.delete(note)
            db.session.commit()
            # return redirect(url_for('views.posts'))
            
    # return jsonify({})
    return redirect('/posts')
 

 
            
#Delete Photo
@views.route('/delete-Img',methods=['POST'])
@login_required
def delete_img():
    user=current_user

    img = json.loads(request.data)
    imgID= img['imgId']
    img=Image.query.get(imgID)
    
    namee=img.img_name
    path=   app.config['POST_FOLDER']+namee
    
    
    print("nameeeeee:   ",namee)
    if img:
        if img.user_id ==user.id or session["user_id"]==1:  
            db.session.delete(img)
            db.session.commit()
            os.remove(path)
            
    return redirect('/posts')



@views.route('/admin')
@login_required
def admin():
    id = session["user_id"]
    if id == 1:
        user=User.query.order_by(User.date)
        
        
        return render_template("Admin.html",user=user)
    else:
        flash("User muste be a admin for access this page")
        return redirect('/')
    
    
    

@views.route('/delete_user',methods=['POST'])
@login_required
def delete_user():

    id = session["user_id"]
    if id == 1:
    
        user = json.loads(request.data)
        userID= user['userId']
        
        user=User.query.get(userID)
      
        images=user.images
        notes=user.notes
        
        for image in images:
                path=   app.config['POST_FOLDER']+image.img_name
                id = image.id
                photo=Image.query.get(id)
                db.session.delete(photo)
                db.session.commit()
                
                os.remove(path)
                
        for note in notes:
                id= note.id      
                note=Note.query.get(id)
                db.session.delete(note)
                db.session.commit()
                
        
        
        
        if user:
            img=user.profile_pic
        
            if img != "Default/Default.jpeg":
                path=app.config['UPLOAD_FOLDER']+img
                db.session.delete(user)
                db.session.commit()
                os.remove(path)
            elif img == "Default/Default.jpeg":
                db.session.delete(user)
                db.session.commit()
               
                
    return redirect('/admin')
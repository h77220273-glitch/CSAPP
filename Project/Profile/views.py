from Project.Profile import bp
from flask_login import login_required,current_user
from flask import render_template,redirect
from Project.Models import User,Followers
from Project.Profile.forms.profileforms import Bio,Info
from Project import db
@bp.route('/profile/<id>')
def profile(id):
    user = User.query.get(id)
    print(user)
    followers = Followers.query.filter_by(user_id=id).all()
    following = Followers.query.filter_by(follower_id=id).all()
    followersids = [i.follower_id for i in followers]
    posts = len(User.query.get(id).posts)
    followerscounter=len(followers)
    followingcounter = len(following)
    user = current_user
    return render_template('profile.html',user=user,posts=user.posts,postcounter=posts,count1=followerscounter,count2=followingcounter,followersids=followersids)

@bp.route('/myprofile',methods=["POST","GET"])
@login_required
def myprofile():
    form = Bio()
    form1=Info()
    if form.validate_on_submit():
        bio = form.bio.data
        user = User.query.get(current_user.id)
        user.bio=bio
        db.session.commit()
        return redirect('/myprofile')
    followers = Followers.query.filter_by(user_id=current_user.id).all()
    following = Followers.query.filter_by(follower_id=current_user.id).all()
    posts = len(User.query.get(current_user.id).posts)
    followerscounter=len(followers)
    followingcounter = len(following)
    user = current_user
    return render_template('myprofile.html',form=form,user=user,form1=form1,counter1=followerscounter,counter2=followingcounter,postscount=posts,followers=followers)

@bp.route('/edit',methods=["POST","GET"])
def update():
    form1=Info()
    if form1.validate_on_submit():
        fname = form1.fname.data
        lname = form1.lname.data 
        user = User.query.get(current_user.id)
        user.fname=fname
        user.lname=lname
        db.session.commit()
        
        return redirect('/myprofile')  
    
@bp.route('/FollowUser/<id>')
def Follow(id):
    FollowedUser=id
    FollowingUser = current_user.id
    FollowObj = Followers(FollowedUser,FollowingUser)
    db.session.add(FollowObj)
    db.session.commit()    
    return redirect(f'/profile/{id}')
@bp.route('/UnFollowUser/<id>')
def UnFollow(id):
    FollowedUser=id
    FollowingUser = current_user.id
    FollowObj = Followers.query.filter_by(user_id=FollowedUser,follower_id=FollowingUser).first()
    db.session.delete(FollowObj)
    db.session.commit()    
    return redirect(f'/profile/{id}')

from . import db
from .models import Package
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from .tracker import simplified_tracker_JSON

views = Blueprint('views', __name__)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        tracking_code = request.form.get('tracking_code')
        carrier = request.form.get('carrier')

        if json.loads(simplified_tracker_JSON(tracking_code, carrier))["error"]:
            flash("Error ocurred. Can not track package at the moment", category="error")
            return render_template("dashboard.html", user=current_user)

        existing_tracker = current_user.packages.filter_by(tracking_code=tracking_code).first()
        if existing_tracker and existing_tracker.carrier == carrier:
            flash('Package already exists in your list.', category='error')
        else:
            new_package = Package(tracking_code=tracking_code, carrier=carrier)
            current_user.packages.append(new_package)
            db.session.add(new_package)
            db.session.commit()
            flash('New package added to dashboard!', category='success')

    return render_template("dashboard.html", user=current_user)

@views.route('/data', methods=['GET'])
@login_required
def fetch_user_data():
    data = {
        "username": current_user.username,
        "email": current_user.email,
        "packages": [simplified_tracker_JSON(p.tracking_code, p.carrier) for p in current_user.packages]
    }
    return data

@views.route('/delete-tracker', methods=['POST'])
@login_required
def delete_note():  
    response = json.loads(request.data)
    tracker = current_user.packages.filter_by(tracking_code=response['tracking_code']).first()
    if tracker:
        current_user.packages.remove(tracker)
        db.session.commit()
        flash(response['tracking_code'] + " deleted!", category="success")

        
    return jsonify({})


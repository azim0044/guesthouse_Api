from flask import render_template, request, redirect, url_for, session, jsonify, Blueprint, flash, send_from_directory
from app import app
from flask_mysqldb import MySQL
from views.dbrequest import DatabaseRequest
from flask_bcrypt import Bcrypt
from markupsafe import escape
import base64
from functools import wraps 
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from PIL import Image
from werkzeug.utils import secure_filename
import io
import uuid
import random
from dotenv import load_dotenv
import os

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['PROFILE_PHOTO'] = 'static/images/profile-photo'
app.config['HOUSE_IMAGE'] = 'static/images/house-images'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mysql = MySQL(app)
db_request = DatabaseRequest(mysql)


#------------------------------ Authenticate Blueprint -------------------------------#
authenticateBP = Blueprint('authenticate', __name__, url_prefix='/authenticate')

@authenticateBP.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        if all([email, password]):
            user_detail = db_request.get_detail('LOGIN_USER', (email,))
            if user_detail:
                if bcrypt.check_password_hash(user_detail['userPassword'], password):
                    access_token = create_access_token(identity=user_detail['userId'])
                    return jsonify({
                        'token': access_token, 
                        'userid': user_detail['userId'], 
                        'userType': user_detail['userType']
                    }), 200
                else:
                    return jsonify({'message': 'Wrong Password or Email !'}), 401
            else:
                return jsonify({'message': 'Account with this email not found !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@authenticateBP.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        fullname = request.json['fullname']
        email = request.json['email']
        password = request.json['password']
        userImage = request.json['userImage']
        phoneNumber = request.json['phoneNumber']
        country = request.json['country']

        if all([fullname, email, password, userImage, phoneNumber]):

            if db_request.get_detail('CHECK_USER', (email,)):
                return jsonify({'status': 'error', 'message': 'User already exist!'}), 401
            
            if userImage is not None:
                userAttachment = base64.b64decode(userImage)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                filename = secure_filename(uuid.uuid4().hex + '.' + image.format.lower())
                image.save(os.path.join(app.config['PROFILE_PHOTO'], filename))
                password = bcrypt.generate_password_hash(password).decode('utf-8')
                insert_user = db_request.insert_data('REGISTER_USER', (fullname, email, password, filename, phoneNumber, country))
                if insert_user:
                    return jsonify({'message': 'User successfully registered !'}), 200
                else:
                    return jsonify({'message': 'Failed to register user !'}), 401
                
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

app.register_blueprint(authenticateBP)

#------------------------------ End Of Authenticate Blueprint -------------------------------#

#------------------------------------ Service Blueprint -------------------------------------#
servicesBP = Blueprint('services', __name__, url_prefix='/services')

@servicesBP.route('/homepage', methods=['GET'])
# @jwt_required()
def homepage():
    if request.method == 'GET':
        bookFrom = request.args.get('bookFrom')
        bookTo = request.args.get('bookTo')
        if all([bookFrom, bookTo]):
            get_house = db_request.get_detail('GET_HOUSES', (bookFrom, bookTo))
            return jsonify(get_house), 200
                
            
    return jsonify({'status': 'error', 'message': 'Invalid rddsdsequest!'})

@servicesBP.route('/add-house', methods=['POST'])
# @jwt_required()
def add_house():
    houseName = request.json['houseName']
    houseCategory = request.json['houseCategory']
    houseDescription = request.json['houseDescription']
    houseThumbnail = request.json['houseThumbnail']
    houseBed = request.json['houseBed']
    housePeople = request.json['housePeople']
    housePrice = request.json['housePrice']
    houseLocation = request.json['houseLocation']
    houseAddress = request.json['houseAddress']
    houseImages = request.json['houseImages']
    houseFacility = request.json['houseFacilities']

    if all([houseName, houseCategory, houseDescription, houseThumbnail, houseBed, housePeople, housePrice, houseStatus, houseAvailability, houseLocation, houseAddress, houseImages, houseFacility]):
        thumbnail_filename = save_image(houseThumbnail)
        image_filenames = [save_image(image_data) for image_data in houseImages]
        houseId = db_request.insert_data('ADD_HOUSE', (houseName, houseCategory, houseDescription, thumbnail_filename, houseBed, housePeople, housePrice, houseStatus, houseAvailability,))
        inserFacility = db_request.insert_data('ADD_HOUSE_FACILITY', (houseId, houseFacility))
        insetImage = db_request.insert_data('ADD_HOUSE_IMAGES', (houseId, image_filenames))
        insertLocation = db_request.insert_data('ADD_HOUSE_LOCATION', (houseId, houseLocation, houseAddress,))

        if houseId and inserFacility and insetImage and insertLocation:
            return jsonify({'message': 'House successfully added !'}), 200
        else:
            return jsonify({'message': 'Failed to add house !'}), 401

@servicesBP.route('/house-review', methods=['GET', 'POST'])
@jwt_required()
def house_review():
    userId = get_jwt_identity()
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        houseId = request.json['houseId']
        reviewNote = request.json['reviewNote']
        rate = request.json['rate']
        

        if all([userId, houseId, rate]):
            insert_review = db_request.insert_data('ADD_REVIEW', (userId, houseId, reviewNote, rate))
            if insert_review:
                return jsonify({'message': 'Review successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add review !'}), 401
     
@servicesBP.route('/user-reservation', methods=['POST', 'GET'])
@jwt_required()
def reservation():
    userId = get_jwt_identity()
    if request.method == 'GET':
        bookStatus = request.args.get('bookStatus')
        if bookStatus is not None:
            user_reservation = db_request.get_detail('GET_RESERVATION', (userId, bookStatus,))
            return jsonify(user_reservation), 200

    if request.method == 'POST':
        houseId = request.json['houseId']
        bookFrom = request.json['bookFrom']
        bookTo = request.json['bookTo']

        if all([userId, bookFrom, bookTo, houseId]):
            insert_reservation = db_request.insert_data('ADD_RESERVATION', (userId, houseId, bookFrom, bookTo))
            if insert_reservation:
                return jsonify({'message': 'Reservation successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add reservation !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/favourite', methods=['GET', 'POST'])
@jwt_required()
def favourite():
    userId = get_jwt_identity()
    if request.method == 'GET':
        user_favourite = db_request.get_detail('GET_FAVOURITE', (userId,))
        return jsonify(user_favourite), 200

    if request.method == 'POST':
        houseId = request.json['houseId']
        if all([userId, houseId]):
            
            if db_request.get_detail('CHECK_FAVOURITE', (userId, houseId)):
                if db_request.delete_data('REMOVE_FAVOURITE', (userId, houseId)):
                    return jsonify({'message': 'Successfully remove house from favourite !'}), 200
                else:
                    return jsonify({'message': 'Failed to remove house from favourite !'}), 401
            else:
                insert_favourite = db_request.insert_data('ADD_FAVOURITE', (userId, houseId))
                if insert_favourite:
                    return jsonify({'message': 'Favourite successfully added !'}), 200
                else:
                    return jsonify({'message': 'Failed to add favourite !'}), 401

@servicesBP.route('/update-profile', methods=['GET', 'POST'])
@jwt_required()
def update_profile():
    userId = get_jwt_identity()
    if request.method == 'GET':
        user_detail = db_request.get_detail('GET_USER', (userId,))
        return jsonify(user_detail), 200

    if request.method == 'POST':
        fullname = request.json['fullname']
        email = request.json['email']
        phoneNumber = request.json['phoneNumber']
        userImage = request.json['userImage']
        if all([userId, fullname, email, phoneNumber]):
            if userImage is not None:
                get_old_image = db_request.get_detail('GET_USER', (userId,))['userImage']
                os.remove(os.path.join(app.config['PROFILE_PHOTO'], get_old_image))
                userAttachment = base64.b64decode(userImage)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                filename = secure_filename(uuid.uuid4().hex + '.' + image.format.lower())
                image.save(os.path.join(app.config['PROFILE_PHOTO'], filename))
                update_user = db_request.update_data('UPDATE_USER', (userId, fullname, phoneNumber, filename, email))
            else:
                update_user = db_request.update_data('UPDATE_USER_WITHOUT_IMAGE', (userId, fullname, phoneNumber, email))

            if update_user:
                return jsonify({'message': 'Profile successfully updated !'}), 200
            else:
                return jsonify({'message': 'Failed to update profile !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    userId = get_jwt_identity()
    if request.method == 'POST':
        oldPassword = request.json['oldPassword']
        newPassword = request.json['newPassword']
        if all([userId, oldPassword, newPassword]):
            user_detail = db_request.get_detail('GET_USER', (userId,))
            if bcrypt.check_password_hash(user_detail['userPassword'], oldPassword):
                newPassword = bcrypt.generate_password_hash(newPassword).decode('utf-8')
                update_password = db_request.update_data('UPDATE_PASSWORD', (userId, newPassword))
                if update_password:
                    return jsonify({'message': 'Password successfully updated !'}), 200
                else:
                    return jsonify({'message': 'Failed to update password !'}), 401
            else:
                return jsonify({'message': 'Wrong old password !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/house-reservation', methods=['GET', 'POST'])
@jwt_required()
def users_reservation():
    userId = get_jwt_identity()
    if request.method == 'GET':
        houseId = request.args.get('houseId')
        if all([userId, houseId]):
            user_reservation = db_request.get_detail('GET_HOUSE_RESERVATION', (houseId,))
            if user_reservation:
                return jsonify(user_reservation), 200
            else:
                return jsonify({'message': 'No reservation found !'}), 200
    
    if request.method == 'POST':
        bookStartDate = request.json['bookStartDate']
        bookEndDate = request.json['bookEndDate']
        houseId = request.json['houseId']
        totalAmount = request.json['totalAmount']
        adultNumber = request.json['adultNumber']
        childrenNumber = request.json['childrenNumber']
        bookingNote = request.json['bookingNote']
        if all([userId, bookStartDate, bookEndDate, houseId, totalAmount, adultNumber]):
            insert_reservation = db_request.insert_data('INSERT_RESERVATION', (userId, houseId, bookStartDate, bookEndDate, totalAmount, adultNumber, childrenNumber, bookingNote,))
            if insert_reservation:
                return jsonify({'message': 'Reservation successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add reservation !'}), 401

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/get-house', methods=['GET'])
@jwt_required()
def get_house():
    houseId = request.args.get('houseId')
    if houseId is not None:
        house_detail = db_request.get_detail('GET_SELECTED_HOUSE', (houseId,))
        return jsonify(house_detail), 200

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/update-status', methods=['POST'])
@jwt_required()
def check_user():
    bookId = request.json['reservationId']
    checkStatus = request.json['checkStatus']
    if all([bookId, checkStatus]):
        user_detail = db_request.update_data('UPDATE_CHECK_USER_STATUS', (bookId, checkStatus,))
        if checkStatus == 'Check-Out':
            db_request.delete_data('REMOVE_RESERVATON', (bookId,))   
            
        if user_detail:
            return jsonify({'message': f'User successfully {checkStatus} !'}), 200
        else:
            return jsonify({'message': f'Failed to {checkStatus} user !'}), 401
    
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/cancel-reservation', methods=['POST'])
@jwt_required()
def cancel_reservation():
    bookId = request.json['reservationId']
    if bookId is not None:
        db_request.delete_data('REMOVE_SERVICE_REQUEST', (bookId,))
        user_detail = db_request.delete_data('REMOVE_RESERVATION', (bookId,))
        if user_detail:
            return jsonify({'message': 'Reservation successfully cancelled !'}), 200
        else:
            return jsonify({'message': 'Failed to cancel reservation !'}), 401
    
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/service-request', methods=['POST', 'GET'])
@jwt_required()
def service_request():
    userId = get_jwt_identity()
    if request.method == 'GET':
        reservationId = request.args.get('reservationId')
        if reservationId is not None:
            service_request = db_request.get_detail('GET_SERVICE_REQUEST', (userId, reservationId,))
            return jsonify(service_request), 200

    if request.method == 'POST':
        reservationId = request.json['reservationId']
        serviceNote = request.json['serviceNote']
        if all([userId, serviceNote, reservationId]):
            insert_service = db_request.insert_data('INSERT_SERVICE_REQUEST', (userId, serviceNote, reservationId,))
            if insert_service:
                return jsonify({'message': 'Service request successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add service request !'}), 401

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/house-feedback', methods=['POST'])
@jwt_required()
def house_feedback():
    userId = get_jwt_identity()
    houseId = request.json['houseId']
    feedbackNote = request.json['feedbackNote']
    houseRating = request.json['houseRating']
    if all([userId, houseId, feedbackNote, houseRating]):
        insert_feedback = db_request.insert_data('INSERT_FEEDBACK', (userId, houseId, feedbackNote, houseRating,))
        if insert_feedback:
            return jsonify({'message': 'Feedback successfully added !'}), 200
        else:
            return jsonify({'message': 'Failed to add feedback !'}), 401

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@servicesBP.route('/house-policy', methods=['GET', 'POST'])
@jwt_required()
def house_policy():
    userId = get_jwt_identity()
    if request.method == 'GET':
        house_policy = db_request.get_detail('GET_HOUSE_POLICY', ())
        return jsonify(house_policy), 200

    if request.method == 'POST':
        policyNote = request.json['policyNote']
        if all([policyNote]):
            insert_policy = db_request.insert_data('INSERT_POLICY', (policyNote,))
            if insert_policy:
                return jsonify({'message': 'Policy successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add policy !'}), 401

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

app.register_blueprint(servicesBP)


#--------------------------------- End Of Service Blueprint ----------------------------------#

#------------------------------------ Admin Blueprint -------------------------------------#
adminBP = Blueprint('services/admin', __name__, url_prefix='/services/admin')

@adminBP.route('/all-reservation', methods=['GET'])
@jwt_required()
def all_reservation():
    if request.method == 'GET':
        bookStatus = request.args.get('bookStatus')
        reservation = db_request.get_detail('GET_ALL_RESERVATION', (bookStatus,))
        return jsonify(reservation), 200

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@adminBP.route('/user-detail', methods=['GET'])
@jwt_required()
def user_detail():
    if request.method == 'GET':
        userId = request.args.get('userId')
        user_detail = db_request.get_detail('GET_USER', (userId,))
        return jsonify([user_detail]), 200  # Wrap user_detail in a list

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@adminBP.route('/add-house', methods=['POST'])
@jwt_required()
def add_house():
    if request.method == 'POST':
        houseName = request.json['houseName']
        houseCategory = request.json['houseCategory']
        houseDescription = request.json['houseDescription']
        houseThumbnail = request.json['houseThumbnail']
        houseBed = request.json['houseBed']
        housePeople = request.json['housePeople']
        housePrice = request.json['housePrice']
        houseLocation = request.json['houseLocation']
        houseAddress = request.json['houseAddress']
        houseImages = request.json['houseImages']
        houseFacility = request.json['houseFacilities']
        if all([houseName, houseCategory, houseDescription, houseThumbnail, houseBed, housePeople, housePrice, houseLocation, houseAddress, houseImages, houseFacility]):
            thumbnail_filename = save_image(houseThumbnail)
            image_filenames = [save_image(image_data) for image_data in houseImages]
            houseId = db_request.insert_data('ADD_HOUSE', (houseName, houseCategory, houseDescription, thumbnail_filename, houseBed, housePeople, housePrice))
            inserFacility = db_request.insert_data('ADD_HOUSE_FACILITY', (houseId, houseFacility))
            insetImage = db_request.insert_data('ADD_HOUSE_IMAGES', (houseId, image_filenames))
            insertLocation = db_request.insert_data('ADD_HOUSE_LOCATION', (houseId, houseLocation, houseAddress,))

            if houseId and inserFacility and insetImage and insertLocation:
                return jsonify({'message': 'House successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add house !'}), 401
    
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@adminBP.route('/approve-reservation', methods=['POST'])
@jwt_required()
def approve_reservation():
    if request.method == 'POST':
        bookId = request.json['bookId']
        bookStatus = 'Approved'
        if all([bookId, bookStatus]):
            user_detail = db_request.update_data('UPDATE_BOOK_STATUS', (bookId, bookStatus,))
            if user_detail:
                return jsonify({'message': 'Reservation successfully approved !'}), 200
            else:
                return jsonify({'message': 'Failed to approve reservation !'}), 401
    
    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401


@adminBP.route('/service-request', methods=['POST', 'GET'])
@jwt_required()
def admin_service_request():
    if request.method == 'GET':
        serviceStatus = request.args.get('serviceStatus')
        service_request = db_request.get_detail('GET_ALL_SERVICE_REQUEST', (serviceStatus,))
        return jsonify(service_request), 200

    if request.method == 'POST':
        serviceId = request.json['serviceId']
        serviceNote = request.json['serviceNote']
        if all([serviceNote, serviceId]):
            insert_service = db_request.update_data('UPDATE_SERVICE_REQUEST', (serviceId, serviceNote,))
            if insert_service:
                return jsonify({'message': 'Service request successfully added !'}), 200
            else:
                return jsonify({'message': 'Failed to add service request !'}), 401

    return jsonify({'status': 'error', 'message': 'Invalid request!'}), 401

@adminBP.route('/update-user', methods=['GET', 'POST'])
@jwt_required()
def update_user():
    if request.method == 'GET':
        user_detail = db_request.get_detail('GET_ALL_USER', ())
        return jsonify(user_detail), 200
    
    if request.method == 'POST':
        userId = request.json['userId']
        fullname = request.json['fullname']
        email = request.json['email']
        userImage = request.json['userImage']
        phoneNumber = request.json['phoneNumber']

        if all([userId, fullname, email, phoneNumber]):
            if userImage is not None:
                get_old_image = db_request.get_detail('GET_USER', (userId,))['userImage']
                os.remove(os.path.join(app.config['PROFILE_PHOTO'], get_old_image))
                userAttachment = base64.b64decode(userImage)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                filename = secure_filename(uuid.uuid4().hex + '.' + image.format.lower())
                image.save(os.path.join(app.config['PROFILE_PHOTO'], filename))
                update_user = db_request.update_data('UPDATE_USER', (userId, fullname, phoneNumber, filename, email))
            else:
                update_user = db_request.update_data('UPDATE_USER_WITHOUT_IMAGE', (userId, fullname, phoneNumber, email))

            if update_user:
                return jsonify({'message': 'Profile successfully updated !'}), 200
            else:
                return jsonify({'message': 'Failed to update profile !'}), 401


@adminBP.route('/update-house', methods=['POST'])
@jwt_required()
def update_house():
    if request.method == 'POST':
        serviceType = request.json['service']

        if serviceType == 'updateHousePrice':
            houseId = request.json['houseId']
            housePrice = request.json['housePrice']

            if all([houseId, housePrice]):
                update_house = db_request.update_data('UPDATE_HOUSE_PRICE', (houseId, housePrice,))
                if update_house:
                    return jsonify({'message': 'House price successfully updated !'}), 200
                else:
                    return jsonify({'message': 'Failed to update house price !'}), 401
        
        if serviceType == 'deleteHouse':
            houseId = request.json['houseId']
            if houseId is not None:
                delete_house = db_request.delete_data('REMOVE_HOUSE', (houseId,))
                if delete_house:
                    return jsonify({'message': 'House successfully deleted !'}), 200
                else:
                    return jsonify({'message': 'Failed to delete house !'}), 401


@adminBP.route('/all-house', methods=['GET'])
@jwt_required()
def adminGetAllHouse():
    if request.method == 'GET':
        get_house = db_request.get_detail('ADMIN_ALL_HOUSE', ())
        return jsonify(get_house), 200
                
            
    return jsonify({'status': 'error', 'message': 'Invalid rddsdsequest!'})


app.register_blueprint(adminBP)


#------------------------------------ Helper Functions -------------------------------------#
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_data):
    image_data = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_data))
    if image.format not in ['JPEG', 'PNG', 'JPG']:  
        image = image.convert('RGB')
    filename = secure_filename(uuid.uuid4().hex + '.' + image.format.lower())
    image.save(os.path.join(app.config['HOUSE_IMAGE'], filename))
    return filename

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['PROFILE_PHOTO'], filename)

@app.route('/house/images/<filename>')
def serve_house_image(filename):
    return send_from_directory(app.config['HOUSE_IMAGE'], filename)

#--------------------------------- End Of Helper Functions ----------------------------------#
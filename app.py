from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_wtf.csrf import CSRFProtect

from utils import (
    calculate_distance_score,
    calculate_urgency_score,
    calculate_quantity_score,
    calculate_match_score
)


from flask_wtf.csrf import CSRFProtect

from flask_migrate import Migrate

from quantity_utils import calculate_quantity_match

from urgency_utils import calculate_urgency

from location_utils import calculate_distance

from flask_sqlalchemy import SQLAlchemy

from config import Config

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    UserMixin
)

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"



# ==========================================
# MATCHING FUNCTIONS
# ==========================================

def get_donation_match_score(donation, receiver):

    # -------------------------
    # 1. DISTANCE SCORE
    # -------------------------
    if (
        donation.latitude is None
        or donation.longitude is None
        or receiver.latitude is None
        or receiver.longitude is None
    ):
        distance_score = 0

    else:
        from math import radians, sin, cos, sqrt, atan2

        lat1 = radians(donation.latitude)
        lon1 = radians(donation.longitude)

        lat2 = radians(receiver.latitude)
        lon2 = radians(receiver.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )

        distance_km = 6371 * c

        distance_score = calculate_distance_score(
            distance_km
        )

    # -------------------------
    # 2. URGENCY SCORE
    # -------------------------

    now = datetime.utcnow()

    hours_left = (
        donation.safe_until - now
    ).total_seconds() / 3600

    urgency_score = calculate_urgency_score(
        hours_left
    )

    # -------------------------
    # 3. QUANTITY SCORE
    # -------------------------

    quantity_score = calculate_quantity_score(
        donation.quantity,
        receiver.required_quantity
    )

    # -------------------------
    # 4. FINAL MATCH SCORE
    # -------------------------

    match_score = calculate_match_score(
        distance_score,
        urgency_score,
        quantity_score
    )

    return match_score

# =========================
# USER MODEL
# =========================

class User(UserMixin, db.Model):

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    required_quantity = db.Column(
        db.Float,
        nullable=True,
        default=0
    )
    
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def set_password(self, password):

        self.password = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )






class FoodDonation(db.Model):

    __tablename__ = "food_donations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    food_name = db.Column(
        db.String(150),
        nullable=False
    )

    food_type = db.Column(
        db.String(20),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    serves_people = db.Column(
        db.Integer,
        nullable=False
    )

    prepared_at = db.Column(
        db.DateTime,
        nullable=False
    )

    safe_until = db.Column(
        db.DateTime,
        nullable=False
    )

    address = db.Column(
        db.String(255),
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="available"
    )

    claimed_by = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=True
    )

    claimed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    donor = db.relationship(
        "User",
        foreign_keys=[donor_id],
        backref="donations"
    )





# =========================
# NOTIFICATION MODEL
# =========================

class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="notifications"
    )




# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# REGISTRATION ROUTE
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]

        allowed_roles = [
            "donor",
            "ngo",
            "volunteer"
        ]

        if role not in allowed_roles:
            flash("Invalid user role.")
            return redirect(url_for("register"))

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already registered!")

            return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None
        )

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash("Registration successful! Please login.")

        return redirect(url_for("login"))

    return render_template("register.html")

# =========================
# LOGIN ROUTE
# =========================

@app.route("/login", methods=["GET", "POST"])
@csrf.exempt
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash("Invalid email or password!")

    return render_template("login.html")


# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/dashboard")
@login_required
def dashboard():

    # =========================
    # DONOR DASHBOARD
    # =========================
    if current_user.role == "donor":

        total_donations = FoodDonation.query.filter_by(
            donor_id=current_user.id
        ).count()

        available_donations = FoodDonation.query.filter_by(
            donor_id=current_user.id,
            status="available"
        ).count()

        claimed_donations = FoodDonation.query.filter_by(
            donor_id=current_user.id,
            status="claimed"
        ).count()

        unread_notifications = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).count()

        recent_donations = FoodDonation.query.filter_by(
            donor_id=current_user.id
        ).order_by(
            FoodDonation.created_at.desc()
        ).limit(5).all()

        return render_template(
            "dashboard.html",
            total_donations=total_donations,
            available_donations=available_donations,
            claimed_donations=claimed_donations,
            unread_notifications=unread_notifications,
            recent_donations=recent_donations
        )

    # =========================
    # NGO DASHBOARD
    # =========================
    elif current_user.role == "ngo":

        available_donations = FoodDonation.query.filter_by(
            status="available"
        ).count()

        my_claims = FoodDonation.query.filter_by(
            claimed_by=current_user.id
        ).count()

        unread_notifications = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).count()

        recent_claims = FoodDonation.query.filter_by(
            claimed_by=current_user.id
        ).order_by(
            FoodDonation.claimed_at.desc()
        ).limit(5).all()

        return render_template(
            "dashboard.html",
            available_donations=available_donations,
            my_claims=my_claims,
            unread_notifications=unread_notifications,
            recent_claims=recent_claims
        )

    return render_template("dashboard.html")



# =========================
# NGO LOCATION
# =========================

@app.route("/ngo-location", methods=["GET", "POST"])
@login_required
def ngo_location():

    if current_user.role != "ngo":
        flash("Only NGOs can update location.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        try:
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")

            if not latitude or not longitude:
                flash("Please capture your location.")
                return redirect(url_for("ngo_location"))

            current_user.latitude = float(latitude)
            current_user.longitude = float(longitude)

            db.session.commit()

            print("================================")
            print("NGO LOCATION UPDATED")
            print("NGO ID:", current_user.id)
            print("LATITUDE:", current_user.latitude)
            print("LONGITUDE:", current_user.longitude)
            print("================================")

            flash("NGO location updated successfully! 📍")

            return redirect(url_for("available_food"))

        except Exception as e:

            db.session.rollback()

            print("NGO LOCATION ERROR:", e)

            flash("Unable to update location.")

    return render_template("ngo_location.html")




# =========================
# ADD FOOD DONATION ROUTE
# =========================

@app.route("/add-food", methods=["GET", "POST"])
@login_required
def add_food():

    print("CURRENT USER ID:", current_user.id)
    print("CURRENT ROLE:", current_user.role)

    # Only donor can add food
    if current_user.role != "donor":
        flash("Only food donors can add donations.")
        return redirect(url_for("dashboard"))

    # =========================
    # POST REQUEST
    # =========================

    if request.method == "POST":

        try:

            # =========================
            # GET FORM DATA
            # =========================

            food_name = request.form.get("food_name", "").strip()
            food_type = request.form.get("food_type", "").strip()
            quantity = request.form.get("quantity", "").strip()
            serves_people = request.form.get("serves_people", "").strip()
            prepared_at = request.form.get("prepared_at", "").strip()
            safe_until = request.form.get("safe_until", "").strip()
            address = request.form.get("address", "").strip()

            latitude = request.form.get("latitude", "").strip()
            longitude = request.form.get("longitude", "").strip()

            # =========================
            # VALIDATION
            # =========================

            if not food_name:
                flash("Please enter food name.")
                return redirect(url_for("add_food"))

            if food_type not in ["veg", "non-veg"]:
                flash("Please select a valid food type.")
                return redirect(url_for("add_food"))

            try:
                quantity_value = float(quantity)

                if quantity_value <= 0:
                    flash("Quantity must be greater than 0.")
                    return redirect(url_for("add_food"))

            except (ValueError, TypeError):
                flash("Please enter a valid quantity.")
                return redirect(url_for("add_food"))

            try:
                serves_value = int(serves_people)

                if serves_value <= 0:
                    flash("Serves people must be greater than 0.")
                    return redirect(url_for("add_food"))

            except (ValueError, TypeError):
                flash("Please enter a valid number of people.")
                return redirect(url_for("add_food"))

            if not address:
                flash("Please enter pickup address.")
                return redirect(url_for("add_food"))

            # =========================
            # LOCATION
            # =========================

            try:

                latitude_value = float(latitude) if latitude else None
                longitude_value = float(longitude) if longitude else None

            except (ValueError, TypeError):

                latitude_value = None
                longitude_value = None

            # =========================
            # DATE / TIME
            # =========================

            prepared_datetime = datetime.fromisoformat(prepared_at)
            safe_until_datetime = datetime.fromisoformat(safe_until)

            # =========================
            # CREATE DONATION
            # =========================

            donation = FoodDonation(

                donor_id=current_user.id,

                food_name=food_name,

                food_type=food_type,

                quantity=quantity_value,

                serves_people=serves_value,

                prepared_at=prepared_datetime,

                safe_until=safe_until_datetime,

                address=address,

                latitude=latitude_value,

                longitude=longitude_value,

                status="available"
            )

            db.session.add(donation)

            db.session.commit()

            # =========================
            # DEBUG
            # =========================

            print("================================")
            print("DONATION CREATED SUCCESSFULLY")
            print("DONATION ID:", donation.id)
            print("FOOD NAME:", donation.food_name)
            print("STATUS:", donation.status)
            print("QUANTITY:", donation.quantity)
            print("LATITUDE:", donation.latitude)
            print("LONGITUDE:", donation.longitude)
            print("================================")

            flash("Food donation added successfully! 🍱")

            return redirect(url_for("my_donations"))

        except Exception as e:

            db.session.rollback()

            print("================================")
            print("ERROR WHILE ADDING FOOD")
            print("ERROR:", e)
            print("================================")

            flash("Unable to add food donation. Please check your details.")

            return redirect(url_for("add_food"))

    # =========================
    # GET REQUEST
    # =========================

    return render_template("add_food.html")


# =========================
# MY DONATIONS ROUTE
# =========================

@app.route("/my-donations")
@login_required
def my_donations():

    if current_user.role != "donor":

        flash("Only donors can access this page.")

        return redirect(
            url_for("dashboard")
        )


    donations = FoodDonation.query.filter_by(
        donor_id=current_user.id
    ).order_by(
        FoodDonation.created_at.desc()
    ).all()


    return render_template(
        "my_donations.html",
        donations=donations
    )



# =========================
# AVAILABLE FOOD ROUTE
# =========================

@app.route("/available-food")
@login_required
def available_food():

    if current_user.role != "ngo":
        flash("Only NGOs can access this page.")
        return redirect(url_for("dashboard"))

    donations = FoodDonation.query.filter_by(
        status="available"
    ).order_by(
        FoodDonation.created_at.desc()
    ).all()

    for donation in donations:

        # =========================
        # 1. DISTANCE
        # =========================

        if (
            current_user.latitude is not None
            and current_user.longitude is not None
            and donation.latitude is not None
            and donation.longitude is not None
        ):

            donation.distance = round(
                calculate_distance(
                    current_user.latitude,
                    current_user.longitude,
                    donation.latitude,
                    donation.longitude
                ),
                2
            )

            # Distance Score
            donation.distance_score = calculate_distance_score(
                donation.distance
            )

        else:
            donation.distance = None
            donation.distance_score = 0


        # =========================
        # 2. URGENCY
        # =========================

        time_left = donation.safe_until - datetime.utcnow()

        hours_left = time_left.total_seconds() / 3600

        donation.urgency_score = calculate_urgency_score(
            hours_left
        )

        if hours_left <= 2:
            donation.urgency = "Critical"

        elif hours_left <= 6:
            donation.urgency = "High"

        elif hours_left <= 12:
            donation.urgency = "Medium"

        else:
            donation.urgency = "Low"


        # =========================
        # 3. QUANTITY MATCH
        # =========================

        donation.quantity_score = calculate_quantity_score(
            donation.quantity,
            current_user.required_quantity
        )

        donation.quantity_match = calculate_quantity_match(
            donation.serves_people
        )


        # =========================
        # 4. FINAL MATCH SCORE
        # =========================

        donation.match_score = calculate_match_score(
            donation.distance_score,
            donation.urgency_score,
            donation.quantity_score
        )


    # =========================
    # 5. SORT BY BEST MATCH
    # =========================

    donations.sort(
        key=lambda donation: donation.match_score,
        reverse=True
    )


    # =========================
    # 6. BEST FOOD MATCH
    # =========================

    best_match = donations[0] if donations else None

    print("================================")
    print("SMART MATCH DEBUG")
    print("AVAILABLE DONATIONS:", len(donations))

    for donation in donations:
        print(
            "ID:", donation.id,
            "| FOOD:", donation.food_name,
            "| STATUS:", donation.status,
            "| DISTANCE:", donation.distance,
            "| DISTANCE SCORE:", donation.distance_score,
            "| URGENCY SCORE:", donation.urgency_score,
            "| QUANTITY SCORE:", donation.quantity_score,
            "| FINAL MATCH SCORE:", donation.match_score
        )

    if best_match:
        print("🏆 BEST FOOD MATCH")
        print("ID:", best_match.id)
        print("FOOD:", best_match.food_name)
        print("MATCH SCORE:", best_match.match_score)
    else:
        print("❌ NO AVAILABLE FOOD")

    print("================================")



    # =========================
    # 7. RENDER PAGE
    # =========================

    return render_template(
        "available_food.html",
        donations=donations,
        best_match=best_match
    )




# =========================
# UPDATE MY LOCATION
# =========================

@app.route("/update-location", methods=["POST"])
@login_required
def update_location():

    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    if not latitude or not longitude:
        flash("Location not received!")
        return redirect(url_for("dashboard"))

    current_user.latitude = float(latitude)
    current_user.longitude = float(longitude)

    db.session.commit()

    flash("Location updated successfully! 📍")

    return redirect(url_for("available_food"))



# ==============================
# CLAIM DONATION ROUTE
# ==============================

@app.route("/claim-donation/<int:donation_id>", methods=["POST"])
@login_required
def claim_donation(donation_id):

    # =========================
    # ROLE CHECK
    # =========================

    if current_user.role != "ngo":
        flash("Only NGOs can claim donations.")
        return redirect(url_for("dashboard"))


    # =========================
    # GET DONATION
    # =========================

    donation = FoodDonation.query.get_or_404(
        donation_id
    )


    # =========================
    # AVAILABILITY CHECK
    # =========================

    if donation.status != "available":

        flash(
            "This donation is no longer available."
        )

        return redirect(
            url_for("available_food")
        )


    # =========================
    # PREVENT SELF CLAIM
    # =========================

    if donation.donor_id == current_user.id:

        flash(
            "You cannot claim your own donation."
        )

        return redirect(
            url_for("available_food")
        )


    # =========================
    # CLAIM DONATION
    # =========================

    donation.status = "claimed"

    donation.claimed_by = current_user.id

    donation.claimed_at = datetime.utcnow()


    # =========================
    # DONOR NOTIFICATION
    # =========================

    notification = Notification(

        user_id=donation.donor_id,

        message=(
            f"Your food donation "
            f"'{donation.food_name}' "
            f"has been claimed by an NGO. 🤝"
        )
    )

    db.session.add(notification)


    # =========================
    # SAVE
    # =========================

    db.session.commit()


    flash(
        "Food donation claimed successfully! 🍱✅"
    )


    return redirect(
        url_for("available_food")
    )


# =========================
# VOLUNTEER PICKUP REQUESTS
# =========================

@app.route("/pickup-requests")
@login_required
def pickup_requests():

    # Only volunteers can access this page
    if current_user.role != "volunteer":
        flash("Only volunteers can access pickup requests.")
        return redirect(url_for("dashboard"))

    # Get all available food donations
    donations = FoodDonation.query.filter_by(
        status="available"
    ).order_by(
        FoodDonation.created_at.desc()
    ).all()

    print("================================")
    print("VOLUNTEER PICKUP REQUESTS")
    print("AVAILABLE FOOD:", len(donations))

    for donation in donations:
        print(
            "ID:", donation.id,
            "| FOOD:", donation.food_name,
            "| QUANTITY:", donation.quantity,
            "| STATUS:", donation.status
        )

    print("================================")

    return render_template(
        "pickup_requests.html",
        donations=donations
    )

# =========================
# MY CLAIMS ROUTE
# =========================

@app.route("/my-claims")
@login_required
def my_claims():

    if current_user.role != "ngo":
        flash("Only NGOs can access claims.")
        return redirect(url_for("dashboard"))

    claims = FoodDonation.query.filter_by(
        claimed_by=current_user.id
    ).order_by(
        FoodDonation.claimed_at.desc()
    ).all()

    return render_template(
        "my_claims.html",
        claims=claims
    )





# =========================
# UPDATE DONATION STATUS
# =========================


@app.route("/update-donation-status/<int:donation_id>/<string:new_status>", methods=["POST"])
@login_required
def update_donation_status(donation_id, new_status):

    if current_user.role != "ngo":
        flash("Only NGOs can update donation status.")
        return redirect(url_for("dashboard"))

    donation = FoodDonation.query.get_or_404(
        donation_id
    )

    # NGO can update only its own claimed donation
    if donation.claimed_by != current_user.id:
        flash("You can only update your own claimed donations.")
        return redirect(url_for("my_claims"))

    allowed_statuses = [
        "picked_up",
        "delivered"
    ]

    if new_status not in allowed_statuses:
        flash("Invalid donation status.")
        return redirect(url_for("my_claims"))

    # =========================
    # STATUS VALIDATION
    # =========================

    if new_status == "picked_up":

        if donation.status != "claimed":
            flash(
                "Donation must be claimed before pickup."
            )
            return redirect(
                url_for("my_claims")
            )

    if new_status == "delivered":

        if donation.status != "picked_up":
            flash(
                "Donation must be picked up before delivery."
            )
            return redirect(
                url_for("my_claims")
            )

    # =========================
    # UPDATE STATUS
    # =========================

    donation.status = new_status


    # =========================
    # DONOR NOTIFICATION
    # =========================

    if new_status == "picked_up":

        notification = Notification(
            user_id=donation.donor_id,
            message=(
                f"Your food donation '{donation.food_name}' "
                f"has been picked up by the NGO. 🚚"
            )
        )

        db.session.add(notification)


    elif new_status == "delivered":

        notification = Notification(
            user_id=donation.donor_id,
            message=(
                f"Your food donation '{donation.food_name}' "
                f"has been successfully delivered. 🎉"
            )
        )

        db.session.add(notification)


    # =========================
    # SAVE
    # =========================

    db.session.commit()


    flash(
        f"Donation status updated to "
        f"{new_status.replace('_', ' ').title()}! ✅"
    )

    return redirect(
        url_for("my_claims")
    )


# =========================
# NOTIFICATIONS ROUTE
# =========================

@app.route("/notifications")
@login_required
def notifications():

    user_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        "notifications.html",
        notifications=user_notifications
    )



# =========================
# MARK NOTIFICATION AS READ
# =========================
@app.route("/notification/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_notification_read(notification_id):

    notification = Notification.query.get_or_404(
        notification_id
    )

    # Security:
    # User can only modify their own notification
    if notification.user_id != current_user.id:
        flash("Unauthorized notification access.")
        return redirect(url_for("notifications"))

    notification.is_read = True

    db.session.commit()

    flash("Notification marked as read. ✅")

    return redirect(url_for("notifications"))




# =========================
# MARK ALL NOTIFICATIONS AS READ
# =========================

@app.route("/notifications/read-all", methods=["POST"])
@login_required
def mark_all_notifications_read():

    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update(
        {
            "is_read": True
        }
    )

    db.session.commit()

    flash("All notifications marked as read. ✅")

    return redirect(url_for("notifications"))


# =========================
# LOGOUT ROUTE
# =========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )







with app.app_context():
    db.create_all()



# =========================
# ERROR HANDLERS
# =========================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    db.session.rollback()

    return render_template(
        "500.html"
    ), 500








if __name__ == "__main__":
    app.run(debug=False)
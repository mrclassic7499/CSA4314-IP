import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager
from config import Config
from models.db import close_db, init_db
from models.user import User
from services.firebase_service import FirebaseService
from services.availability_service import AvailabilityService
from routes import auth_bp, parking_bp, bookings_bp, admin_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure required runtime directories exist
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    os.makedirs(app.config.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'data', 'uploads')), exist_ok=True)

    # Database connection teardown
    app.teardown_appcontext(close_db)

    # Initialize Firebase Admin SDK (falls back to local mode if unconfigured)
    FirebaseService.initialize()

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please sign in to access this page."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    # Global Context Processor for Templates
    @app.context_processor
    def inject_global_data():
        return {
            'firebase_status': FirebaseService.get_status(),
            'firebase_client_config': app.config.get('FIREBASE_CLIENT_CONFIG', {}),
            'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    # Register application blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)

    # Real-Time API Endpoints for Client Listeners
    @app.route('/api/live-status')
    def api_live_status():
        """
        Returns live Firebase connection status and system availability summary.
        Used by the frontend real-time synchronization manager.
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        summary = AvailabilityService.get_system_summary(query_start=start_time, query_end=end_time)
        return jsonify({
            'success': True,
            'firebase': FirebaseService.get_status(),
            'summary': summary,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    @app.route('/api/live-slots/<int:lot_id>')
    def api_live_slots(lot_id):
        """
        Returns latest slot states for a parking facility.
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        try:
            data = AvailabilityService.get_lot_layout_with_status(lot_id, start_time, end_time)
            return jsonify({
                'success': True,
                'lot_id': lot_id,
                'data': data,
                'firebase': FirebaseService.get_status(),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    # Custom Jinja Template Filters
    @app.template_filter('currency')
    def format_currency(value):
        try:
            return f"₹{float(value):,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    @app.template_filter('datetime_format')
    def format_datetime(value, format_out='%d %b %Y, %I:%M %p'):
        if not value:
            return ''
        try:
            val_str = str(value).replace('T', ' ')
            dt = datetime.strptime(val_str[:19], '%Y-%m-%d %H:%M:%S')
            return dt.strftime(format_out)
        except Exception:
            return str(value)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # Ensure local database tables exist automatically
    with app.app_context():
        init_db(app.config['DATABASE_PATH'])

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

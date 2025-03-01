from app import app, db  # Replace with your actual application file

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
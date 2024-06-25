from app import db, create_app
from app.models import User
from faker import Faker

def seed_admin_user():
    # Create an admin user
    email = "admin@thehexaa.com"
    password = "admin"
    admin_user = User(
        email=email,
        is_admin=True,
        email_verified=True
    )
    admin_user.set_password(password)
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print('Superuser already exists!')
        return
    
    db.session.add(admin_user)
    db.session.commit()
    print('Admin user seeded successfully!')

def insert_synthetic_data(num_users):
    faker = Faker()

    # Generate synthetic data for 'user' table
    for _ in range(num_users):
        email = faker.email()
        password_hash = faker.sha256()
        is_admin = faker.boolean()
        email_verified = faker.boolean()
        user = User(
            email=email,
            password_hash=password_hash,
            is_admin=is_admin,
            email_verified=email_verified
        )
        db.session.add(user)
    
    db.session.commit()
    print(f"Inserted {num_users} rows into 'user' table.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_admin_user()
        insert_synthetic_data(num_users=10)  # Adjust the number of synthetic users as needed

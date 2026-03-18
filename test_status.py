from app import app, db, Internship
with app.app_context():
    with open('output_status.txt', 'w') as f:
        f.write('STATUSES: ' + str([i.status for i in Internship.query.all()]))

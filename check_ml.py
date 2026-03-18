import sys, traceback; from app import app, db, User, StudentProfile, Internship; from ai.ml_integration import get_ml_match_score; 
with app.app_context():
    with open('test_ml_out.txt','w') as f:
        try:
            u = User.query.filter_by(role='student').first()
            p = StudentProfile.query.filter_by(user_id=u.id).first()
            i = Internship.query.filter_by(status='active').first() or Internship.query.filter_by(status='approved').first()
            f.write(f'User: {u.name}\n')
            score = get_ml_match_score(p, i, db.session)
            f.write(f'Score: {score}\n')
        except Exception as e:
            f.write(f'ERROR: {e}\n')
            f.write(traceback.format_exc())

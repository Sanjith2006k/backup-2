# ML-Enhanced Student-Internship Matching System

## Overview

This is an advanced machine learning-based internship matching system that continuously learns from real-world feedback to improve future recommendations. The system incorporates multiple factors to provide highly accurate student-internship matches.

## Key Features

### 1. **Feedback-Based Learning** 🔄

- Collects feedback from both students and companies after internship completion
- Uses this feedback as training data to improve future recommendations
- Model automatically retrains every 10 new feedback submissions
- Achieves continuous improvement over time

### 2. **Certificate Matching Bonus** 📜

- Students with relevant certificates get a **5-15% bonus** to their match score
- Uses semantic similarity to match certificate content with internship requirements
- Considers both certificate names and related skills
- More relevant certificates = higher bonus (capped at 15%)

### 3. **Previous Internship Experience Bonus** 💼

- Students with prior internships in the **same domain** get a **7-21% bonus**
- Domain matching using keyword analysis (Machine Learning, Web Development, etc.)
- Longer internship durations provide additional bonus (up to 5%)
- Multiple relevant experiences compound the benefit

### 4. **Research Paper Bonus** 📄

- Published research papers in the **relevant domain** provide a **10-30% bonus**
- Considers semantic similarity between paper content and internship domain
- High-impact papers (more citations) receive additional bonus (up to 10%)
- Demonstrates deep expertise and commitment to the field

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Student Profile                          │
│  ├─ Skills                                                   │
│  ├─ Certificates                                             │
│  ├─ Previous Internships                                     │
│  ├─ Research Papers                                          │
│  └─ Historical Feedback Score                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Feature Extraction Engine                       │
│  ├─ Semantic Similarity (Sentence Transformers)              │
│  ├─ Certificate Relevance Analysis                           │
│  ├─ Domain Identification & Matching                         │
│  ├─ Experience Quality Scoring                               │
│  └─ Research Impact Assessment                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Gradient Boosting ML Model                           │
│  ├─ 13 Engineered Features                                   │
│  ├─ Trained on Historical Feedback Data                      │
│  └─ Outputs Match Score (0-100)                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Match Score + Breakdown                         │
│  ├─ Overall Score (0-100)                                    │
│  ├─ Component Breakdown                                      │
│  ├─ Bonus Explanations                                       │
│  └─ Improvement Recommendations                              │
└─────────────────────────────────────────────────────────────┘
```

## Installation & Setup

### Prerequisites

```bash
pip install flask flask-sqlalchemy flask-login
pip install scikit-learn sentence-transformers
pip install pandas numpy
```

### Database Migration

1. **Add new tables to your database:**

```bash
python migrate_db.py
```

This creates three new tables:

- `internship_feedback`: Stores feedback from students and companies
- `research_paper`: Stores student research publications
- `matching_model_metrics`: Tracks ML model performance

2. **Import models in your app.py:**

```python
from models import InternshipFeedback, ResearchPaper, MatchingModelMetrics
```

3. **Add routes to your Flask app:**

Copy the routes from `example_routes.py` into your main `app.py` file.

## Usage Guide

### For Students

#### 1. Add Research Papers

```python
# Students can add their publications to boost match scores
POST /student/research-papers
{
  "title": "Deep Learning for Image Classification",
  "authors": "John Doe, Jane Smith",
  "publication_venue": "CVPR 2023",
  "publication_date": "2023-06-15",
  "abstract": "We propose a novel architecture...",
  "keywords": "deep learning, computer vision, CNN",
  "domain": "Machine Learning",
  "paper_url": "https://arxiv.org/...",
  "citation_count": 5
}
```

#### 2. View ML-Enhanced Matches

```python
# Get personalized internship recommendations
GET /student/internships/ml-matches

# Response includes:
# - Top internship matches ranked by ML score
# - Detailed breakdown showing why each match is good
# - Recommendations for improvement
```

#### 3. Submit Post-Internship Feedback

```python
# After completing an internship
POST /student/feedback/submit/<internship_id>
{
  "satisfaction": 4,        # 1-5 scale
  "learning": 5,            # How much you learned
  "work_environment": 4,    # Work environment quality
  "mentor_quality": 5,      # Mentor quality
  "skill_match": 4,         # How well skills matched
  "would_recommend": true,  # Would recommend to others
  "comments": "Great experience!"
}
```

### For Companies/Organizations

#### 1. View ML-Enhanced Student Matches

```python
# Get top student matches for an internship
GET /organization/internship/<internship_id>/ml-matches

# Response includes:
# - Students ranked by match score
# - Each student's strengths and relevant experience
# - Certificate and research paper highlights
```

#### 2. Submit Post-Internship Feedback

```python
# After student completes internship
POST /organization/feedback/submit/<student_id>/<internship_id>
{
  "performance": 4,         # Overall performance (1-5)
  "skill_level": 4,         # Actual skill level (1-5)
  "professionalism": 5,     # Professionalism (1-5)
  "learning_ability": 5,    # Learning ability (1-5)
  "would_hire": true,       # Would hire full-time
  "would_recommend": true,  # Would recommend to others
  "comments": "Excellent intern!"
}
```

### For Administrators

#### 1. Monitor ML Model Status

```python
# View model performance and training data
GET /admin/ml-model/status

# Shows:
# - Current model version and metrics
# - Number of feedbacks collected
# - Feature importance rankings
# - Training history
```

#### 2. Manually Trigger Model Training

```python
# Retrain model with latest feedback
POST /admin/ml-model/train

# The model will:
# 1. Collect all feedback data
# 2. Extract features from student-internship pairs
# 3. Train Gradient Boosting model
# 4. Save new model version
# 5. Update metrics
```

## API Endpoints

### Get Match Score (AJAX)

```javascript
POST /api/ml-match-score
{
  "student_id": 123,
  "internship_id": 456
}

// Response:
{
  "match_score": 87.5,
  "breakdown": {
    "base_match_score": 65.0,
    "skill_similarity": 80.0,
    "certificate_bonus": 10.0,
    "certificate_count": 2,
    "experience_bonus": 7.0,
    "experience_count": 1,
    "research_bonus": 5.5,
    "research_count": 1
  },
  "recommendations": [
    "Upload relevant certificates to boost your match score"
  ],
  "confidence": "high"
}
```

### Get Student Recommendations

```javascript
GET /api/student-recommendations/<student_id>?limit=10

// Returns top 10 internship matches with scores and breakdowns
```

### Get Internship Matches

```javascript
GET /api/internship-matches/<internship_id>?limit=20

// Returns top 20 student matches with scores and breakdowns
```

## How It Works

### Feature Engineering

The system extracts 13 key features for each student-internship pair:

1. **Skill Similarity** - Semantic similarity between student skills and requirements
2. **Keyword Overlap** - Percentage of required skills the student has
3. **Certificate Bonus** - Boost from relevant certificates (0-15%)
4. **Certificate Count** - Number of relevant certificates
5. **Experience Bonus** - Boost from domain-relevant internships (0-21%)
6. **Experience Count** - Number of relevant prior internships
7. **Research Bonus** - Boost from domain-relevant papers (0-30%)
8. **Research Count** - Number of relevant publications
9. **Location Match** - Binary match for location/remote
10. **AI Score** - Student's overall platform score (normalized)
11. **Historical Success** - Average success score from past internships
12. **Personality Match** - Cultural fit score
13. **Domain Similarity** - Overall domain alignment

### Machine Learning Model

- **Algorithm**: Gradient Boosting Regressor
- **Training Data**: Historical student-internship pairs with actual success scores
- **Success Score Calculation**:
  - Student feedback: 40% weight (with 10% bonus for recommendation)
  - Company feedback: 50% weight (with 10% bonus for hire intent)
- **Retraining**: Automatic after every 10 new feedback submissions
- **Evaluation Metrics**: MAE, MSE, R² Score

### Domain Identification

The system recognizes 10 major domains:

- Machine Learning
- Web Development
- Data Science
- Cybersecurity
- Cloud Computing
- Mobile Development
- Blockchain
- Game Development
- IoT
- UI/UX Design

Each domain has carefully curated keywords for accurate matching.

## Scoring Breakdown

### Base Score (0-100)

- Calculated from skill similarity, keyword overlap, and basic features
- Uses ML model if trained (>10 feedback samples)
- Falls back to heuristic scoring for new systems

### Bonus Components

#### Certificate Bonus (up to 20%)

```
base_bonus = min(relevant_cert_count * 5%, 15%)
relevance_bonus = avg_semantic_similarity * 5%
total_cert_bonus = base_bonus + relevance_bonus
```

#### Experience Bonus (up to 26%)

```
base_bonus = min(relevant_internship_count * 7%, 21%)
duration_bonus = min(total_months / 12, 1.0) * 5%
domain_match_bonus = avg_domain_overlap * 3%
total_exp_bonus = base_bonus + duration_bonus + domain_match_bonus
```

#### Research Paper Bonus (up to 45%)

```
base_bonus = min(relevant_paper_count * 10%, 30%)
citation_bonus = min(total_citations / 100, 1.0) * 10%
relevance_bonus = avg_semantic_similarity * 5%
total_research_bonus = base_bonus + citation_bonus + relevance_bonus
```

### Final Score

```
final_score = min(base_score + cert_bonus + exp_bonus + research_bonus, 100)
```

## Example Scenario

### Student Profile

- Skills: "Python, Machine Learning, TensorFlow, PyTorch"
- Certificates:
  - "Deep Learning Specialization" by Coursera
  - "TensorFlow Developer Certificate"
- Previous Internships:
  - ML Research Intern at TechCorp (6 months)
- Research Papers:
  - "Novel CNN Architecture for Image Classification" (10 citations)

### Internship Posting

- Title: "Machine Learning Intern"
- Required Skills: "Python, TensorFlow, Deep Learning, Neural Networks"
- Domain: "Machine Learning"

### Match Calculation

```
Base Match: 72.0 (strong skill alignment)
Certificate Bonus: +12.5 (2 highly relevant certificates)
Experience Bonus: +11.0 (1 internship in ML, 6-month duration)
Research Bonus: +18.5 (1 highly relevant paper, 10 citations)

Final Score: 114.0 → Capped at 100.0
```

**Result: Perfect Match! 🎯**

## Benefits

### For Students

- ✅ Get matched with internships that fit your actual expertise
- ✅ See exactly how to improve your match scores
- ✅ Get rewarded for certificates, experience, and research
- ✅ Higher quality internship placements

### For Companies

- ✅ Find students with proven relevant skills
- ✅ See detailed breakdowns of each candidate's strengths
- ✅ Reduced time spent screening applicants
- ✅ Better intern-role fit leading to better outcomes

### For the Platform

- ✅ Continuous improvement from feedback data
- ✅ Higher satisfaction rates for both parties
- ✅ Data-driven insights into matching quality
- ✅ Competitive advantage through ML technology

## Monitoring & Maintenance

### Check Model Status

```bash
# View current model metrics
curl http://localhost:5000/admin/ml-model/status
```

### Retrain Model

```bash
# Manually trigger retraining
curl -X POST http://localhost:5000/admin/ml-model/train
```

### Model Files

- `ai/models/match_model.pkl` - Trained ML model
- `ai/models/scaler.pkl` - Feature scaler

### Logs

The system logs important events:

- Model training completion
- Feature importance rankings
- Training data statistics

## Troubleshooting

### Model Not Training

- **Issue**: "Insufficient training data"
- **Solution**: Collect at least 10 complete feedbacks (both student and company)

### Low Match Scores

- **Issue**: All students getting low scores
- **Solution**:
  1. Encourage students to add certificates
  2. Students should fill in previous internship experience
  3. Students should add research papers if applicable

### Model Not Loading

- **Issue**: Model file not found
- **Solution**: Train the model first using `/admin/ml-model/train`

## Future Enhancements

- [ ] Deep learning model for even better accuracy
- [ ] Natural language understanding of student portfolios
- [ ] Skill gap analysis with learning recommendations
- [ ] Collaborative filtering for similar student preferences
- [ ] Industry trend analysis for emerging skills
- [ ] Interview performance prediction
- [ ] Success prediction for specific company cultures

## License

This ML matching system is proprietary software for the internship platform.

## Support

For questions or issues:

- Check this README first
- Review example_routes.py for integration examples
- Contact the development team

---

**Built with ❤️ using Flask, Scikit-learn, and Sentence Transformers**

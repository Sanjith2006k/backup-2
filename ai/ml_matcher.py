"""
Enhanced ML-Based Internship Matching System

This module implements an advanced machine learning model for student-internship matching
that learns from historical feedback and incorporates multiple boosting factors:
- Post-internship feedback from students and companies
- Certificate relevance matching
- Previous internship experience in the same domain
- Research publications in the relevant domain
"""

import numpy as np
import pandas as pd
import pickle
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

# ML libraries
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


class EnhancedMLMatcher:
    """
    Advanced ML-based matching system that learns from feedback and incorporates
    multiple domain-specific boosting factors.
    """

    def __init__(self, model_path='ai/models'):
        """
        Initialize the ML matcher with pre-trained models or create new ones.

        Args:
            model_path: Directory to save/load trained models
        """
        self.model_path = model_path
        os.makedirs(model_path, exist_ok=True)

        # Sentence transformer for semantic similarity
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

        # ML models for different aspects
        self.match_model = None  # Main matching model
        self.scaler = StandardScaler()

        # Feature importance tracking
        self.feature_names = []
        self.feature_importance = {}

        # Domain mappings for skill categorization
        self.domain_keywords = {
            'Machine Learning': ['ml', 'machine learning', 'deep learning', 'neural network', 'ai',
                                'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'nlp', 'computer vision'],
            'Web Development': ['web', 'html', 'css', 'javascript', 'react', 'angular', 'vue',
                               'node.js', 'express', 'frontend', 'backend', 'full stack'],
            'Data Science': ['data science', 'data analysis', 'pandas', 'numpy', 'statistics',
                            'visualization', 'tableau', 'power bi', 'sql', 'big data'],
            'Cybersecurity': ['security', 'cybersecurity', 'penetration testing', 'ethical hacking',
                             'cryptography', 'firewall', 'network security', 'vulnerability'],
            'Cloud Computing': ['cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
                               'devops', 'terraform', 'ci/cd'],
            'Mobile Development': ['mobile', 'android', 'ios', 'react native', 'flutter',
                                  'swift', 'kotlin', 'mobile app'],
            'Blockchain': ['blockchain', 'cryptocurrency', 'web3', 'ethereum', 'solidity',
                         'smart contracts', 'defi'],
            'Game Development': ['game', 'unity', 'unreal', 'game engine', '3d', 'graphics'],
            'IoT': ['iot', 'internet of things', 'embedded', 'arduino', 'raspberry pi', 'sensors'],
            'UI/UX Design': ['ui', 'ux', 'design', 'figma', 'sketch', 'adobe xd', 'wireframe', 'prototype']
        }

        # Load existing model if available
        self._load_model()


    def _load_model(self):
        """Load pre-trained model from disk if available."""
        model_file = os.path.join(self.model_path, 'match_model.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')

        try:
            if os.path.exists(model_file) and os.path.exists(scaler_file):
                with open(model_file, 'rb') as f:
                    self.match_model = pickle.load(f)
                with open(scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
                print(f"Loaded ML model from {model_file}")
        except Exception as e:
            print(f"Could not load model: {e}. Will create new model on training.")


    def _save_model(self):
        """Save trained model to disk."""
        model_file = os.path.join(self.model_path, 'match_model.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')

        try:
            with open(model_file, 'wb') as f:
                pickle.dump(self.match_model, f)
            with open(scaler_file, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"Saved ML model to {model_file}")
        except Exception as e:
            print(f"Could not save model: {e}")


    def identify_domain(self, text: str) -> List[str]:
        """
        Identify domains from text using keyword matching.

        Args:
            text: Text to analyze (skills, job description, etc.)

        Returns:
            List of identified domain names
        """
        text_lower = text.lower()
        identified_domains = []

        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    identified_domains.append(domain)
                    break

        return list(set(identified_domains))


    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts using sentence transformers.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0

        embedding1 = self.sentence_model.encode([text1])
        embedding2 = self.sentence_model.encode([text2])

        similarity = cosine_similarity(embedding1, embedding2)[0][0]
        return float(similarity)


    def calculate_certificate_bonus(self, certificates: List[Dict],
                                    internship_skills: str) -> Tuple[float, int]:
        """
        Calculate bonus score for relevant certificates.

        Args:
            certificates: List of student certificates with fields:
                         {certificate_name, related_skill, description}
            internship_skills: Required skills for the internship

        Returns:
            Tuple of (bonus_score, relevant_certificate_count)
        """
        if not certificates or not internship_skills:
            return 0.0, 0

        internship_skills_lower = internship_skills.lower()
        relevant_count = 0
        total_relevance = 0.0

        for cert in certificates:
            cert_text = f"{cert.get('certificate_name', '')} {cert.get('related_skill', '')} {cert.get('description', '')}"

            # Semantic similarity
            similarity = self.calculate_semantic_similarity(cert_text, internship_skills)

            # Keyword matching
            keywords_match = 0
            skill_words = [s.strip() for s in internship_skills_lower.split(',')]
            for skill in skill_words:
                if skill in cert_text.lower():
                    keywords_match += 1

            # Combine scores
            if similarity > 0.3 or keywords_match > 0:
                relevant_count += 1
                total_relevance += (similarity * 0.7 + (keywords_match / max(len(skill_words), 1)) * 0.3)

        # Base bonus: 5% increase for each relevant certificate (capped at 15%)
        bonus_score = min(relevant_count * 0.05, 0.15)

        # Additional bonus based on relevance strength
        if relevant_count > 0:
            avg_relevance = total_relevance / relevant_count
            bonus_score += avg_relevance * 0.05  # Up to 5% additional

        return bonus_score, relevant_count


    def calculate_internship_experience_bonus(self, previous_internships: List[Dict],
                                               internship_domain: str,
                                               internship_title: str) -> Tuple[float, int]:
        """
        Calculate bonus score for previous internship experience in the same domain.

        Args:
            previous_internships: List of previous internship experiences with fields:
                                {role, skills_used, work_description}
            internship_domain: Domain of the target internship
            internship_title: Title of the target internship

        Returns:
            Tuple of (bonus_score, relevant_experience_count)
        """
        if not previous_internships:
            return 0.0, 0

        # Identify target domains
        target_text = f"{internship_domain} {internship_title}"
        target_domains = self.identify_domain(target_text)

        if not target_domains:
            return 0.0, 0

        relevant_count = 0
        total_domain_match = 0.0
        total_duration_months = 0

        for exp in previous_internships:
            exp_text = f"{exp.get('role', '')} {exp.get('skills_used', '')} {exp.get('work_description', '')}"
            exp_domains = self.identify_domain(exp_text)

            # Check domain overlap
            domain_overlap = set(target_domains) & set(exp_domains)

            if domain_overlap:
                relevant_count += 1
                # More overlap = higher score
                overlap_ratio = len(domain_overlap) / len(target_domains)
                total_domain_match += overlap_ratio

                # Calculate duration if dates available
                if exp.get('start_date') and exp.get('end_date'):
                    try:
                        start = exp['start_date']
                        end = exp['end_date']
                        if isinstance(start, str):
                            start = datetime.strptime(start, '%Y-%m-%d').date()
                        if isinstance(end, str):
                            end = datetime.strptime(end, '%Y-%m-%d').date()

                        duration_days = (end - start).days
                        total_duration_months += duration_days / 30
                    except:
                        pass

        # Base bonus: 7% for each relevant internship (capped at 21%)
        bonus_score = min(relevant_count * 0.07, 0.21)

        # Duration bonus: up to 5% for longer experiences
        if total_duration_months > 0:
            duration_bonus = min(total_duration_months / 12, 1.0) * 0.05
            bonus_score += duration_bonus

        # Domain match quality bonus
        if relevant_count > 0:
            avg_match = total_domain_match / relevant_count
            bonus_score += avg_match * 0.03

        return bonus_score, relevant_count


    def calculate_research_paper_bonus(self, research_papers: List[Dict],
                                        internship_domain: str,
                                        internship_title: str) -> Tuple[float, int]:
        """
        Calculate bonus score for research papers in the relevant domain.

        Args:
            research_papers: List of research papers with fields:
                           {title, abstract, keywords, domain, citation_count}
            internship_domain: Domain of the target internship
            internship_title: Title of the target internship

        Returns:
            Tuple of (bonus_score, relevant_paper_count)
        """
        if not research_papers:
            return 0.0, 0

        # Identify target domains
        target_text = f"{internship_domain} {internship_title}"
        target_domains = self.identify_domain(target_text)

        if not target_domains:
            return 0.0, 0

        relevant_count = 0
        total_relevance = 0.0
        total_citations = 0

        for paper in research_papers:
            paper_text = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('keywords', '')} {paper.get('domain', '')}"
            paper_domains = self.identify_domain(paper_text)

            # Semantic similarity
            similarity = self.calculate_semantic_similarity(paper_text, target_text)

            # Domain overlap
            domain_overlap = set(target_domains) & set(paper_domains)

            if domain_overlap or similarity > 0.4:
                relevant_count += 1

                # Calculate relevance score
                domain_score = len(domain_overlap) / len(target_domains) if domain_overlap else 0
                combined_relevance = similarity * 0.6 + domain_score * 0.4
                total_relevance += combined_relevance

                # Citations indicate impact
                citations = paper.get('citation_count', 0)
                total_citations += citations

        # Base bonus: 10% for each relevant paper (capped at 30%)
        bonus_score = min(relevant_count * 0.10, 0.30)

        # Citation bonus: up to 10% for high-impact papers
        if total_citations > 0:
            citation_bonus = min(total_citations / 100, 1.0) * 0.10
            bonus_score += citation_bonus

        # Relevance quality bonus
        if relevant_count > 0:
            avg_relevance = total_relevance / relevant_count
            bonus_score += avg_relevance * 0.05

        return bonus_score, relevant_count


    def extract_features(self, student_data: Dict, internship_data: Dict) -> np.ndarray:
        """
        Extract feature vector for ML model from student and internship data.

        Args:
            student_data: Dictionary containing student information
            internship_data: Dictionary containing internship information

        Returns:
            Feature vector as numpy array
        """
        features = []

        # 1. Base skill matching (semantic similarity)
        student_skills = student_data.get('skills', '')
        required_skills = internship_data.get('skills_required', '')
        skill_similarity = self.calculate_semantic_similarity(student_skills, required_skills)
        features.append(skill_similarity)

        # 2. Keyword overlap score
        student_skills_set = set(student_skills.lower().split(','))
        required_skills_set = set(required_skills.lower().split(','))
        if required_skills_set:
            keyword_overlap = len(student_skills_set & required_skills_set) / len(required_skills_set)
        else:
            keyword_overlap = 0.0
        features.append(keyword_overlap)

        # 3. Certificate bonus and count
        cert_bonus, cert_count = self.calculate_certificate_bonus(
            student_data.get('certificates', []),
            required_skills
        )
        features.append(cert_bonus)
        features.append(cert_count)

        # 4. Previous internship bonus and count
        exp_bonus, exp_count = self.calculate_internship_experience_bonus(
            student_data.get('internship_experiences', []),
            internship_data.get('domain', ''),
            internship_data.get('title', '')
        )
        features.append(exp_bonus)
        features.append(exp_count)

        # 5. Research paper bonus and count
        paper_bonus, paper_count = self.calculate_research_paper_bonus(
            student_data.get('research_papers', []),
            internship_data.get('domain', ''),
            internship_data.get('title', '')
        )
        features.append(paper_bonus)
        features.append(paper_count)

        # 6. Location match
        student_location = student_data.get('location', '').lower()
        internship_location = internship_data.get('location', '').lower()
        location_match = 1.0 if (student_location in internship_location or
                                 internship_location in student_location or
                                 'remote' in internship_location) else 0.0
        features.append(location_match)

        # 7. Student AI score (normalized)
        ai_score = student_data.get('ai_score', 0)
        normalized_ai_score = min(ai_score / 1000, 1.0)  # Assuming max 1000
        features.append(normalized_ai_score)

        # 8. Historical success rate (if available from feedback)
        historical_success = student_data.get('avg_feedback_score', 0.5)
        features.append(historical_success)

        # 9. Personality-culture match (if available)
        personality_match = student_data.get('personality_culture_match', 0.5)
        features.append(personality_match)

        # 10. Domain match
        student_text = f"{student_skills} {' '.join([e.get('role', '') for e in student_data.get('internship_experiences', [])])}"
        internship_text = f"{internship_data.get('title', '')} {required_skills}"
        domain_similarity = self.calculate_semantic_similarity(student_text, internship_text)
        features.append(domain_similarity)

        # Update feature names (only on first run)
        if not self.feature_names:
            self.feature_names = [
                'skill_similarity', 'keyword_overlap', 'certificate_bonus', 'certificate_count',
                'experience_bonus', 'experience_count', 'research_bonus', 'research_count',
                'location_match', 'ai_score_normalized', 'historical_success',
                'personality_match', 'domain_similarity'
            ]

        return np.array(features)


    def train_model(self, training_data: List[Dict]):
        """
        Train the ML model using historical feedback data.

        Args:
            training_data: List of dictionaries containing:
                - student_data: Student information
                - internship_data: Internship information
                - actual_success_score: Ground truth from feedback (0-100)
        """
        if len(training_data) < 10:
            print("Insufficient training data (need at least 10 samples). Using default heuristic model.")
            return

        # Extract features and labels
        X = []
        y = []

        for sample in training_data:
            features = self.extract_features(
                sample['student_data'],
                sample['internship_data']
            )
            X.append(features)
            y.append(sample['actual_success_score'] / 100)  # Normalize to 0-1

        X = np.array(X)
        y = np.array(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Gradient Boosting model
        self.match_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            subsample=0.8
        )

        self.match_model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.match_model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Model Training Complete:")
        print(f"  - Samples: {len(training_data)}")
        print(f"  - MAE: {mae:.4f}")
        print(f"  - MSE: {mse:.4f}")
        print(f"  - R² Score: {r2:.4f}")

        # Feature importance
        if hasattr(self.match_model, 'feature_importances_'):
            importance = self.match_model.feature_importances_
            self.feature_importance = dict(zip(self.feature_names, importance))
            print("\nTop Features:")
            sorted_features = sorted(self.feature_importance.items(),
                                   key=lambda x: x[1], reverse=True)
            for name, score in sorted_features[:5]:
                print(f"  - {name}: {score:.4f}")

        # Save model
        self._save_model()


    def predict_match_score(self, student_data: Dict, internship_data: Dict) -> Dict:
        """
        Predict match score for a student-internship pair.

        Args:
            student_data: Dictionary containing student information
            internship_data: Dictionary containing internship information

        Returns:
            Dictionary containing:
                - match_score: Overall match score (0-100)
                - breakdown: Detailed score breakdown
                - recommendations: Suggestions for improvement
        """
        # Extract features
        features = self.extract_features(student_data, internship_data)

        # Predict using ML model if available, otherwise use heuristic
        if self.match_model is not None:
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            ml_score = self.match_model.predict(features_scaled)[0]
            base_score = ml_score * 100  # Convert to 0-100 scale
        else:
            # Heuristic fallback
            base_score = features[0] * 60  # Skill similarity (60% weight)
            base_score += features[1] * 20  # Keyword overlap (20% weight)
            base_score += features[8] * 10  # Location match (10% weight)
            base_score += features[9] * 10  # AI score (10% weight)

        # Apply bonuses
        cert_bonus = features[2] * 100
        exp_bonus = features[4] * 100
        research_bonus = features[6] * 100

        final_score = base_score + cert_bonus + exp_bonus + research_bonus
        final_score = min(final_score, 100)  # Cap at 100

        # Build breakdown
        breakdown = {
            'base_match_score': round(base_score, 2),
            'skill_similarity': round(features[0] * 100, 2),
            'keyword_overlap': round(features[1] * 100, 2),
            'certificate_bonus': round(cert_bonus, 2),
            'certificate_count': int(features[3]),
            'experience_bonus': round(exp_bonus, 2),
            'experience_count': int(features[5]),
            'research_bonus': round(research_bonus, 2),
            'research_count': int(features[7]),
            'location_match': round(features[8] * 100, 2),
            'ai_score_contribution': round(features[9] * 100, 2),
        }

        # Generate recommendations
        recommendations = []
        if features[3] == 0:
            recommendations.append("Upload relevant certificates to boost your match score")
        if features[5] == 0:
            recommendations.append("Add previous internship experiences in this domain")
        if features[7] == 0:
            recommendations.append("Publish research papers in this domain for a significant boost")
        if features[0] < 0.5:
            recommendations.append("Improve your skills to better match the requirements")

        return {
            'match_score': round(final_score, 2),
            'breakdown': breakdown,
            'recommendations': recommendations,
            'confidence': 'high' if self.match_model is not None else 'medium'
        }


    def batch_predict(self, students_data: List[Dict],
                      internship_data: Dict) -> List[Tuple[int, Dict]]:
        """
        Predict match scores for multiple students for one internship.

        Args:
            students_data: List of student data dictionaries
            internship_data: Internship data dictionary

        Returns:
            List of tuples (student_id, match_result) sorted by match score
        """
        results = []

        for student in students_data:
            match_result = self.predict_match_score(student, internship_data)
            results.append((student.get('id'), match_result))

        # Sort by match score (descending)
        results.sort(key=lambda x: x[1]['match_score'], reverse=True)

        return results


# Singleton instance
_ml_matcher_instance = None

def get_ml_matcher() -> EnhancedMLMatcher:
    """Get or create the singleton ML matcher instance."""
    global _ml_matcher_instance
    if _ml_matcher_instance is None:
        _ml_matcher_instance = EnhancedMLMatcher()
    return _ml_matcher_instance

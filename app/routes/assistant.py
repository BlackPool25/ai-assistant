from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Interaction, User
from app.utils.senior_helpers import SeniorAssistant
from app import db

assistant_bp = Blueprint('assistant', __name__)
assistant = SeniorAssistant()

@assistant_bp.route('/')
@login_required
def home():
    return render_template('dashboard/home.html')

@assistant_bp.route('/history')
@login_required
def history():
    interactions = Interaction.query.filter_by(user_id=current_user.id).order_by(Interaction.created_at.desc()).limit(50).all()
    return render_template('dashboard/history.html', interactions=interactions)

@assistant_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.preferred_voice = request.form.get('voice')
        current_user.text_size = request.form.get('text_size')
        db.session.commit()
    return render_template('dashboard/settings.html')

@assistant_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_input = data.get('message')
    
    try:
        response = assistant.generate_response(user_input, current_user)
        interaction = Interaction(
            user_id=current_user.id,
            input_text=user_input,
            response_text=response,
            is_important=assistant.check_importance(user_input)
        )
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({'text': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
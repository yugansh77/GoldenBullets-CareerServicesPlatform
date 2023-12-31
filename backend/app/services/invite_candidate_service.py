from models.invite import Invite
from models.user import User
from models.job_post import JobPost
from services.notification import NotificationService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
class InviteCandidateService:
        @staticmethod
        @jwt_required()
        def invite_candidate(request):

            try:
                # Get user from jwt token
                user_email = get_jwt_identity()
                user = User.query.filter_by(email=user_email).first()
                # Check if user type is employer
                if user.type != 'employer':
                    return {'error': 'Unauthorized'}, 401
                
                job_id = request.json['job_id']
                candidate_id = request.json['candidate_id']
                prev_invites = Invite.query.filter_by(job_id=job_id, candidate_id=candidate_id).first()
                if prev_invites is None:
                    invitation = Invite(job_id=job_id, candidate_id=candidate_id)
                    db.session.add(invitation)
                    db.session.commit()
                    # Create notification for candidate
                    # Get job title
                    job = JobPost.query.filter_by(id=job_id).first()
                    NotificationService.create_notification(candidate_id, 'New job application invitation', f'You have been invited to apply to the job "#{job.id} {job.title}"')
                    return invitation.serialize()
                else:
                    return {'error': 'Candidate already invited'}, 400
            except Exception as e:
                print('error', e)
                return {'error': str(e)}, 500
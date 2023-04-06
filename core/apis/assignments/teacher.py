from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_submission = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_submission_dump = AssignmentSchema().dump(teacher_submission, many=True)
    return APIResponse.respond(data=teacher_submission_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    
    """Grade an assignment"""
    submit_assignment_payload = incoming_payload.get('id')
    submit_assignment_payload2 = incoming_payload.get('grade')
    print(submit_assignment_payload)
    
    submitted_assignment = Assignment.grade_it(submit_assignment_payload,submit_assignment_payload2,p)
    
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
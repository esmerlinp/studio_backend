from app.models.client_scheme.sub_cycle_course_competency_view import SubCycleCourseCompetencyView

def get_sub_cycle_course_competencies(filters=None):
    """
    Retrieve sub cycle course competencies.
    """
    query = SubCycleCourseCompetencyView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('subCycleId'):
            query = query.filter_by(subCycleId=filters['subCycleId'])
            
        if filters.get('subjectId'):
            query = query.filter_by(subjectId=filters['subjectId'])
            
    return query.order_by(SubCycleCourseCompetencyView.competencyName).all()

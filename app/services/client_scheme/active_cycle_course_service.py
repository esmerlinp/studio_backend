from app.models.client_scheme.active_cycle_course_view import ActiveCycleCourseView

def get_active_cycle_courses():
    """
    Retrieve all records from the active cycle course view.
    Orders results by cycle, subcycle order, course order, and subject order.
    """
    return ActiveCycleCourseView.query.order_by(
        ActiveCycleCourseView.cycleName,
        ActiveCycleCourseView.subCycleOrder,
        ActiveCycleCourseView.courseOrder,
        ActiveCycleCourseView.subjectOrder
    ).all()

def get_active_cycle_courses_filtered(cycle_id=None, course_id=None, sub_cycle_id=None):
    """
    Retrieve records filtered by cycle_id, course_id, or sub_cycle_id.
    """
    query = ActiveCycleCourseView.query
    
    if cycle_id:
        query = query.filter_by(cycleId=cycle_id)
        
    if course_id:
        query = query.filter_by(courseId=course_id)

    if sub_cycle_id:
        query = query.filter_by(subCycleId=sub_cycle_id)
        
    return query.order_by(
        ActiveCycleCourseView.cycleName,
        ActiveCycleCourseView.subCycleOrder,
        ActiveCycleCourseView.courseOrder,
        ActiveCycleCourseView.subjectOrder
    ).all()

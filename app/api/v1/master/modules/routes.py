from flask import Blueprint
from . import controller

modules_bp = Blueprint('modules', __name__)

modules_bp.add_url_rule('/modules', view_func=controller.get_modules, methods=['GET'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.get_module, methods=['GET'])
modules_bp.add_url_rule('/modules', view_func=controller.create_module, methods=['POST'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.update_module, methods=['PUT'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.delete_module, methods=['DELETE'])

# Routes for financial module
from flask import render_template
@modules_bp.route('/client/financial', methods=['GET'])
def financial_payment_view():
    return render_template('es/client/financial/payment.html', active_page='payments')

@modules_bp.route('/api/v1/client/financial/pending-charges', methods=['GET'])
def get_pending_charges_route():
    from app.api.v1.client_scheme.school_payments.controller import get_pending
    return get_pending()

@modules_bp.route('/api/v1/client/financial/balance', methods=['GET'])
def get_family_balance_route():
    from app.api.v1.client_scheme.school_payments.controller import get_balance
    return get_balance()

@modules_bp.route('/api/v1/client/financial/payment', methods=['POST'])
def submit_payment_route():
    from app.api.v1.client_scheme.school_payments.controller import submit_payment
    return submit_payment()

# Financial Configuration Routes
# Frequencies
@modules_bp.route('/client/financial/frequencies', methods=['GET'])
def frequencies_view():
    from app.models.client_scheme.payment_frequency_list_view import PaymentFrequencyListView
    frequencies = PaymentFrequencyListView.query.order_by(PaymentFrequencyListView.id).all()
    return render_template('es/client/financial/frequencies/index.html', frequencies=frequencies, active_page='frequencies')

@modules_bp.route('/client/financial/frequencies/new', methods=['GET'])
def new_frequency_view():
    return render_template('es/client/financial/frequencies/form.html', active_page='frequencies')

@modules_bp.route('/client/financial/frequencies/edit/<int:id>', methods=['GET'])
def edit_frequency_view(id):
    from app.models.client_scheme.payment_frequency_list_view import PaymentFrequencyListView
    frequency = PaymentFrequencyListView.query.get(id)
    return render_template('es/client/financial/frequencies/form.html', frequency=frequency, active_page='frequencies')

@modules_bp.route('/api/v1/client/financial/frequencies', methods=['GET'])
def get_frequencies_route():
    from app.api.v1.client_scheme.financial_config.controller import get_frequencies
    return get_frequencies()

@modules_bp.route('/api/v1/client/financial/frequencies', methods=['POST'])
def create_frequency_route():
    from app.api.v1.client_scheme.financial_config.controller import create_frequency
    return create_frequency()

@modules_bp.route('/api/v1/client/financial/frequencies/<int:id>', methods=['PUT'])
def update_frequency_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_frequency
    return update_frequency(id)

@modules_bp.route('/api/v1/client/financial/frequencies/<int:id>', methods=['DELETE'])
def delete_frequency_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_frequency
    return delete_frequency(id)

# Cycles
@modules_bp.route('/client/financial/cycles', methods=['GET'])
def cycles_view():
    from app.models.client_scheme.cycle_list_view import CycleListView
    cycles = CycleListView.query.order_by(CycleListView.id.desc()).all()
    return render_template('es/client/financial/cycles/index.html', cycles=cycles, active_page='cycles')

@modules_bp.route('/client/financial/cycles/new', methods=['GET'])
def new_cycle_view():
    return render_template('es/client/financial/cycles/form.html', active_page='cycles')

@modules_bp.route('/client/financial/cycles/edit/<int:id>', methods=['GET'])
def edit_cycle_view(id):
    from app.models.client_scheme.cycle_list_view import CycleListView
    cycle = CycleListView.query.get(id)
    return render_template('es/client/financial/cycles/form.html', cycle=cycle, active_page='cycles')

@modules_bp.route('/api/v1/client/financial/cycles', methods=['GET'])
def get_cycles_route():
    from app.api.v1.client_scheme.financial_config.controller import get_cycles
    return get_cycles()

@modules_bp.route('/api/v1/client/financial/cycles', methods=['POST'])
def create_cycle_route():
    from app.api.v1.client_scheme.financial_config.controller import create_cycle
    return create_cycle()

@modules_bp.route('/api/v1/client/financial/cycles/<int:id>', methods=['PUT'])
def update_cycle_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_cycle
    return update_cycle(id)

# Concepts
@modules_bp.route('/client/financial/concepts', methods=['GET'])
def concepts_view():
    from app.models.client_scheme.concept_list_view import ConceptListView
    concepts = ConceptListView.query.order_by(ConceptListView.id).all()
    return render_template('es/client/financial/concepts/index.html', concepts=concepts, active_page='concepts')

@modules_bp.route('/client/financial/concepts/new', methods=['GET'])
def new_concept_view():
    return render_template('es/client/financial/concepts/form.html', active_page='concepts')

@modules_bp.route('/client/financial/concepts/edit/<int:id>', methods=['GET'])
def edit_concept_view(id):
    from app.models.client_scheme.concept_list_view import ConceptListView
    concept = ConceptListView.query.get(id)
    return render_template('es/client/financial/concepts/form.html', concept=concept, active_page='concepts')

@modules_bp.route('/api/v1/client/financial/concepts', methods=['GET'])
def get_concepts_route():
    from app.api.v1.client_scheme.financial_config.controller import get_concepts
    return get_concepts()

@modules_bp.route('/api/v1/client/financial/concepts', methods=['POST'])
def create_concept_route():
    from app.api.v1.client_scheme.financial_config.controller import create_concept
    return create_concept()

@modules_bp.route('/api/v1/client/financial/concepts/<int:id>', methods=['PUT'])
def update_concept_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_concept
    return update_concept(id)

@modules_bp.route('/api/v1/client/financial/concepts/<int:id>', methods=['DELETE'])
def delete_concept_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_concept
    return delete_concept(id)

# Course Costs
@modules_bp.route('/client/financial/costs', methods=['GET'])
def costs_view():
    from app.api.v1.client_scheme.financial_config.controller import CourseCostModel
    from app.models.client_scheme.cycle_list_view import CycleListView
    from app.models.client_scheme.course_list_view import CourseListView
    
    # Filters
    cycle_id = request.args.get('cycleId')
    course_id = request.args.get('courseId')
    
    query = CourseCostModel.query
    if cycle_id:
        query = query.filter_by(cycleId=cycle_id)
    if course_id:
        query = query.filter_by(courseId=course_id)
        
    costs_data = query.order_by(CourseCostModel.id.desc()).all()
    costs = [c.to_dict() for c in costs_data]
    
    # Dropdowns for filter
    cycles = CycleListView.query.filter_by(isActive=True).all()
    courses = CourseListView.query.filter_by(isActive=True).all()
    
    return render_template('es/client/financial/costs/index.html', 
                           costs=costs, 
                           cycles=cycles, 
                           courses=courses,
                           selected_cycle=cycle_id,
                           selected_course=course_id,
                           active_page='costs')

@modules_bp.route('/client/financial/costs/new', methods=['GET'])
def new_cost_view():
    from app.models.client_scheme.cycle_list_view import CycleListView
    from app.models.client_scheme.course_list_view import CourseListView
    from app.models.client_scheme.concept_list_view import ConceptListView
    
    cycles = CycleListView.query.filter_by(isActive=True).all()
    courses = CourseListView.query.filter_by(isActive=True).all()
    concepts = ConceptListView.query.filter_by(isActive=True).all()
    
    return render_template('es/client/financial/costs/form.html', 
                           cycles=cycles, courses=courses, concepts=concepts,
                           active_page='costs')

@modules_bp.route('/client/financial/costs/edit/<int:id>', methods=['GET'])
def edit_cost_view(id):
    from app.api.v1.client_scheme.financial_config.controller import CourseCostModel
    from app.models.client_scheme.cycle_list_view import CycleListView
    from app.models.client_scheme.course_list_view import CourseListView
    from app.models.client_scheme.concept_list_view import ConceptListView
    
    cost = CourseCostModel.query.get(id)
    
    cycles = CycleListView.query.filter_by(isActive=True).all()
    courses = CourseListView.query.filter_by(isActive=True).all()
    concepts = ConceptListView.query.filter_by(isActive=True).all()
    
    return render_template('es/client/financial/costs/form.html', 
                           cost=cost,
                           cycles=cycles, courses=courses, concepts=concepts,
                           active_page='costs')

@modules_bp.route('/api/v1/client/financial/costs', methods=['GET'])
def get_costs_route():
    from app.api.v1.client_scheme.financial_config.controller import get_costs
    return get_costs()

@modules_bp.route('/api/v1/client/financial/costs', methods=['POST'])
def create_cost_route():
    from app.api.v1.client_scheme.financial_config.controller import create_cost
    return create_cost()

@modules_bp.route('/api/v1/client/financial/costs/<int:id>', methods=['PUT'])
def update_cost_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_cost
    return update_cost(id)

@modules_bp.route('/api/v1/client/financial/costs/<int:id>', methods=['DELETE'])
def delete_cost_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_cost
    return delete_cost(id)

# Boxes
@modules_bp.route('/client/financial/boxes', methods=['GET'])
def boxes_view():
    from app.api.v1.client_scheme.financial_config.controller import BoxModel
    boxes = BoxModel.query.order_by(BoxModel.id).all()
    # Need to manually call to_dict to get user names, or pass models to template and handle there
    # Let's convert to dicts for easier handling
    boxes_list = [b.to_dict() for b in boxes]
    return render_template('es/client/financial/boxes/index.html', boxes=boxes_list, active_page='boxes')

@modules_bp.route('/client/financial/boxes/new', methods=['GET'])
def new_box_view():
    # Need users for dropdown
    from app.models.master_scheme.user_model import Users
    users = Users.query.filter_by(active=True).all()
    return render_template('es/client/financial/boxes/form.html', users=users, active_page='boxes')

@modules_bp.route('/client/financial/boxes/edit/<int:id>', methods=['GET'])
def edit_box_view(id):
    from app.api.v1.client_scheme.financial_config.controller import BoxModel
    from app.models.master_scheme.user_model import Users
    
    box = BoxModel.query.get(id)
    users = Users.query.filter_by(active=True).all()
    return render_template('es/client/financial/boxes/form.html', box=box, users=users, active_page='boxes')

@modules_bp.route('/api/v1/client/financial/boxes', methods=['GET'])
def get_boxes_route():
    from app.api.v1.client_scheme.financial_config.controller import get_boxes
    return get_boxes()

@modules_bp.route('/api/v1/client/financial/boxes', methods=['POST'])
def create_box_route():
    from app.api.v1.client_scheme.financial_config.controller import create_box
    return create_box()

@modules_bp.route('/api/v1/client/financial/boxes/<int:id>', methods=['PUT'])
def update_box_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_box
    return update_box(id)

@modules_bp.route('/api/v1/client/financial/boxes/<int:id>', methods=['DELETE'])
def delete_box_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_box
    return delete_box(id)

# NCF
@modules_bp.route('/client/financial/ncf', methods=['GET'])
def ncf_view():
    from app.api.v1.client_scheme.financial_config.controller import ClientNCFModel
    ncf_list = ClientNCFModel.query.order_by(ClientNCFModel.type_ncf).all()
    # Convert to dicts
    ncf_data = [n.to_dict() for n in ncf_list]
    return render_template('es/client/financial/ncf/index.html', ncf_list=ncf_data, active_page='ncf')

@modules_bp.route('/client/financial/ncf/new', methods=['GET'])
def new_ncf_view():
    return render_template('es/client/financial/ncf/form.html', active_page='ncf')

@modules_bp.route('/client/financial/ncf/edit/<int:id>', methods=['GET'])
def edit_ncf_view(id):
    from app.api.v1.client_scheme.financial_config.controller import ClientNCFModel
    ncf = ClientNCFModel.query.get(id)
    return render_template('es/client/financial/ncf/form.html', ncf=ncf, active_page='ncf')

@modules_bp.route('/api/v1/client/financial/ncf', methods=['GET'])
def get_ncf_route():
    from app.api.v1.client_scheme.financial_config.controller import get_ncf_sequences
    return get_ncf_sequences()

@modules_bp.route('/api/v1/client/financial/ncf', methods=['POST'])
def create_ncf_route():
    from app.api.v1.client_scheme.financial_config.controller import create_ncf_sequence
    return create_ncf_sequence()

@modules_bp.route('/api/v1/client/financial/ncf/<int:id>', methods=['PUT'])
def update_ncf_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_ncf_sequence
    return update_ncf_sequence(id)

@modules_bp.route('/api/v1/client/financial/ncf/<int:id>', methods=['DELETE'])
def delete_ncf_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_ncf_sequence
    return delete_ncf_sequence(id)

# Taxes
@modules_bp.route('/client/financial/taxes', methods=['GET'])
def taxes_view():
    from app.api.v1.client_scheme.financial_config.controller import ClientTaxModel
    taxes = ClientTaxModel.query.order_by(ClientTaxModel.date.desc()).all()
    # Convert to dicts
    taxes_data = [t.to_dict() for t in taxes]
    return render_template('es/client/financial/taxes/index.html', taxes=taxes_data, active_page='taxes')

@modules_bp.route('/client/financial/taxes/new', methods=['GET'])
def new_tax_view():
    return render_template('es/client/financial/taxes/form.html', active_page='taxes')

@modules_bp.route('/client/financial/taxes/edit/<int:id>', methods=['GET'])
def edit_tax_view(id):
    from app.api.v1.client_scheme.financial_config.controller import ClientTaxModel
    tax = ClientTaxModel.query.get(id)
    return render_template('es/client/financial/taxes/form.html', tax=tax, active_page='taxes')

@modules_bp.route('/api/v1/client/financial/taxes', methods=['GET'])
def get_taxes_route():
    from app.api.v1.client_scheme.financial_config.controller import get_taxes
    return get_taxes()

@modules_bp.route('/api/v1/client/financial/taxes', methods=['POST'])
def create_tax_route():
    from app.api.v1.client_scheme.financial_config.controller import create_tax
    return create_tax()

@modules_bp.route('/api/v1/client/financial/taxes/<int:id>', methods=['PUT'])
def update_tax_route(id):
    from app.api.v1.client_scheme.financial_config.controller import update_tax
    return update_tax(id)

@modules_bp.route('/api/v1/client/financial/taxes/<int:id>', methods=['DELETE'])
def delete_tax_route(id):
    from app.api.v1.client_scheme.financial_config.controller import delete_tax
    return delete_tax(id)

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import *
from .. import db
from ..models import *


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments/<int:page_num>/', methods=['GET', 'POST'])
@login_required
def list_departments(page_num):
    """
    List all departments
    """
    check_admin()

    # departments = Department.query.all()
    departments = Department.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments', page_num=1))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments', page_num=1))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments', page_num=1))

    return render_template(title="Delete Department")


# Customer Views


@admin.route('/customers/view/<int:id>', methods=['GET'])
@login_required
def view_customer(id):
    """
    View a customer
    """
    check_admin()

    customer = Customer.query.filter_by(c_id=id).first()

    return render_template('admin/customers/view_customer.html', action="View",
                           customer=customer, title="View Customer")


@admin.route('/customers/<int:page_num>/', methods=['GET', 'POST'])
@login_required
def list_customers(page_num):
    """
    List all customers
    """
    check_admin()

    # customers = Customer.query.all()
    customers = Customer.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/customers/customers.html',
                           customers=customers, title="Customers")


@admin.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    """
    Add a customer to the database
    """
    check_admin()

    add_customer = True

    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(acc_code=form.acc_code.data,
                                comp_name = form.comp_name.data,
                                f_name = form.f_name.data,
                                l_name = form.l_name.data,
                                phone = form.phone.data,
                                email = form.email.data,
                                b_address = form.b_address.data,
                                city = form.city.data,
                                state_province = form.state_province.data,
                                post_code = form.post_code.data,
                                count_region = form.count_region.data,
                                cont_title = form.cont_title.data,
                                fax = form.fax.data,
                                notes = form.notes.data,
                                order = form.order.data,
                                state = form.state.data,
                                status = form.status.data,
                                rating = form.rating.data)
        try:
            # add customer to the database
            db.session.add(customer)
            db.session.commit()
            flash('You have successfully added a new customer.')
        except:
            # in case Customer Account Code already exists
            flash('Error: Customer Account Code already exists.')

        # redirect to customers page
        return redirect(url_for('admin.list_customers', page_num=1))

    # load customer template
    return render_template('admin/customers/customer.html', action="Add",
                           add_customer=add_customer, form=form,
                           title="Add Customer")


@admin.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    """
    Edit a customer
    """
    check_admin()

    add_customer = False

    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.acc_code = form.acc_code.data
        customer.comp_name = form.comp_name.data
        customer.f_name = form.f_name.data
        customer.l_name = form.l_name.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        customer.b_address = form.b_address.data
        customer.city = form.city.data
        customer.state_province = form.state_province.data
        customer.post_code = form.post_code.data
        customer.count_region = form.count_region.data
        customer.cont_title = form.cont_title.data
        customer.fax = form.fax.data
        customer.notes = form.notes.data
        customer.order = form.order.data
        customer.state = form.state.data
        customer.status = form.status.data
        customer.rating = form.rating.data

        db.session.commit()
        flash('You have successfully edited the customer.')

        # redirect to the customers page
        return redirect(url_for('admin.list_customers', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.acc_code.data = customer.acc_code 
    form.comp_name.data = customer.comp_name 
    form.f_name.data = customer.f_name 
    form.l_name.data = customer.l_name
    form.phone.data = customer.phone
    form.email.data = customer.email
    form.b_address.data = customer.b_address 
    form.city.data = customer.city
    form.state_province.data = customer.state_province
    form.post_code.data = customer.post_code
    form.count_region.data = customer.count_region
    form.cont_title.data = customer.cont_title
    form.fax.data = customer.fax 
    form.notes.data = customer.notes 
    form.order.data = customer.order 
    form.state.data = customer.state
    form.status.data = customer.status
    form.rating.data = customer.rating

    return render_template('admin/customers/customer.html', action="Edit",
                           add_customer=add_customer, form=form,
                           customer=customer, title="Edit Customer")


@admin.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    """
    Delete a customer from the database
    """
    check_admin()

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('You have successfully deleted the customer.')

    # redirect to the customers page
    return redirect(url_for('admin.list_customers', page_num=1))

    return render_template(title="Delete Customer")


# Role Views


@admin.route('/roles/<int:page_num>/')
@login_required
def list_roles(page_num):
    check_admin()
    """
    List all roles
    """
    # roles = Role.query.all()
    roles = Role.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles', page_num=1))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles', page_num=1))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles', page_num=1))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees/<int:page_num>')
@login_required
def list_employees(page_num):
    """
    List all employees
    """
    check_admin()

    # employees = Employee.query.all()
    employees = Employee.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees', page_num=1))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


# Product Views


@admin.route('/products/view/<int:id>', methods=['GET'])
@login_required
def view_product(id):
    """
    View a product
    """
    check_admin()

    product = Product.query.filter_by(p_id=id).first()

    return render_template('admin/products/view_product.html', action="View",
                           product=product, title="View Product")


@admin.route('/products/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_products(page_num):
    """
    List all products
    """
    check_admin()

    # products = Product.query.all()
    products = Product.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/products/products.html',
                           products=products, title="Products")


@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    Add a product to the database
    """
    check_admin()

    add_product = True

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(p_number=form.p_number.data,
                                p_name = form.p_name.data,
                                unit_price = form.unit_price.data,
                                p_note = form.p_note.data,
                                cost_native = form.cost_native.data,
                                exchange_rate = form.exchange_rate.data,
                                unit_cost = form.unit_cost.data,
                                supplier = form.supplier.data,
                                p_category = form.p_category.data,
                                p_status = form.p_status.data,
                                date_created = form.date_created.data,
                                person_created = form.person_created.data,
                                remarks = form.remarks.data)
                                
        try:
            # add product to the database
            db.session.add(product)
            db.session.commit()
            flash('You have successfully added a new product.')
        except:
            # in case Product already exists
            flash('Error: Product already exists.')

        # redirect to products page
        return redirect(url_for('admin.list_products', page_num=1))

    # load product template
    return render_template('admin/products/product.html', action="Add",
                           add_product=add_product, form=form,
                           title="Add Product")


@admin.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Edit a product
    """
    check_admin()

    add_product = False

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.p_number = form.p_number.data
        product.p_name = form.p_name.data
        product.unit_price = form.unit_price.data
        product.p_note = form.p_note.data
        product.cost_native = form.cost_native.data
        product.exchange_rate = form.exchange_rate.data
        product.unit_cost = form.unit_cost.data
        product.unit_cost = form.unit_cost.data
        product.supplier = form.supplier.data
        product.p_category = form.p_category.data
        product.p_status = form.p_status.data
        product.date_created = form.date_created.data
        product.person_created = form.person_created.data
        product.remarks = form.remarks.data

        db.session.commit()
        flash('You have successfully edited the product.')

        # redirect to the products page
        return redirect(url_for('admin.list_products', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.p_number.data = product.p_number 
    form.p_name.data = product.p_name 
    form.unit_price.data = product.unit_price 
    form.p_note.data = product.p_note
    form.cost_native.data = product.cost_native
    form.exchange_rate.data = product.exchange_rate
    form.unit_cost.data = product.unit_cost
    form.unit_cost.data = product.unit_cost
    form.supplier.data = product.supplier 
    form.p_category.data = product.p_category
    form.p_status.data = product.p_status
    form.date_created.data = product.date_created
    form.person_created.data = product.person_created
    form.remarks.data = product.remarks

    return render_template('admin/products/product.html', action="Edit",
                           add_product=add_product, form=form,
                           product=product, title="Edit Product")


@admin.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a product from the database
    """
    check_admin()

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted the product.')

    # redirect to the products page
    return redirect(url_for('admin.list_products', page_num=1))

    return render_template(title="Delete Product")


# Quotation Views


@admin.route('/quotations/view/<int:id>', methods=['GET'])
@login_required
def view_quotation(id):
    """
    View a quotation
    """
    check_admin()

    quotation = Quotation.query.filter_by(q_id=id).first()

    return render_template('admin/quotations/view_quotation.html', action="View",
                           quotation=quotation, title="View Quotation")


@admin.route('/quotations/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_quotations(page_num):
    """
    List all quotations
    """
    check_admin()

    # quotations = Quotation.query.all()
    quotations = Quotation.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/quotations/quotations.html',
                           quotations=quotations, title="Quotations")


@admin.route('/quotations/add', methods=['GET', 'POST'])
@login_required
def add_quotation():
    """
    Add a quotation to the database
    """
    check_admin()

    add_quotation = True

    form = QuotationForm()
    if form.validate_on_submit():
        # When using foreign keys as queries in forms, c_id returns the customer object, so must extract c_id from object
        quotation = Quotation(c_id = form.c_id.data.c_id,           # special
                                q_num = form.q_num.data,
                                e_id = form.e_id.data.id,           # special
                                date = form.date.data,
                                revision = form.revision.data,
                                pay_terms = form.pay_terms.data,
                                title = form.title.data,
                                f_name = form.f_name.data,
                                l_name = form.l_name.data,
                                address = form.address.data,
                                city = form.city.data,
                                state = form.state.data,
                                country = form.country.data,
                                postal = form.postal.data,
                                tel = form.tel.data,
                                s_sched = form.s_sched.data,
                                s_term = form.s_term.data,
                                q_title = form.q_title.data,
                                q_note = form.q_note.data,
                                q_amount = form.q_amount.data)
                                
        try:
            # add quotation to the database
            db.session.add(quotation)
            db.session.commit()
            flash('You have successfully added a new quotation.')
        except:
            # in case Quotation already exists
            flash('Error: Quotation already exists.')

        # redirect to quotations page
        return redirect(url_for('admin.list_quotations', page_num=1))

    # load quotation template
    return render_template('admin/quotations/quotation.html', action="Add",
                           add_quotation=add_quotation, form=form,
                           title="Add Quotation")


@admin.route('/quotations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quotation(id):
    """
    Edit a quotation
    """
    check_admin()

    add_quotation = False

    quotation = Quotation.query.get_or_404(id)
    form = QuotationForm(obj=quotation)
    if form.validate_on_submit():
        quotation.c_id = form.c_id.data.c_id        # special
        quotation.q_num = form.q_num.data        
        quotation.e_id = form.e_id.data.id          # special
        quotation.date = form.date.data
        quotation.revision = form.revision.data
        quotation.pay_terms = form.pay_terms.data
        quotation.title = form.title.data
        quotation.f_name = form.f_name.data
        quotation.l_name = form.l_name.data
        quotation.address = form.address.data
        quotation.city = form.city.data
        quotation.state = form.state.data
        quotation.country = form.country.data
        quotation.postal = form.postal.data
        quotation.tel = form.tel.data
        quotation.s_sched = form.s_sched.data
        quotation.s_term = form.s_term.data
        quotation.q_title = form.q_title.data
        quotation.q_note = form.q_note.data
        quotation.q_amount = form.q_amount.data

        db.session.commit()
        flash('You have successfully edited the quotation.')

        # redirect to the quotations page
        return redirect(url_for('admin.list_quotations', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.c_id.data = quotation.c_id
    form.q_num.data = quotation.q_num
    form.e_id.data = quotation.e_id
    form.date.data = quotation.date
    form.revision.data = quotation.revision
    form.pay_terms.data = quotation.pay_terms
    form.title.data = quotation.title
    form.f_name.data = quotation.f_name
    form.l_name.data = quotation.l_name
    form.address.data = quotation.address
    form.city.data = quotation.city
    form.state.data = quotation.state
    form.country.data = quotation.country 
    form.postal.data = quotation.postal
    form.tel.data = quotation.tel
    form.s_sched.data = quotation.s_sched
    form.s_term.data = quotation.s_term
    form.q_title.data = quotation.q_title
    form.q_note.data = quotation.q_note
    form.q_amount.data = quotation.q_amount

    return render_template('admin/quotations/quotation.html', action="Edit",
                           add_quotation=add_quotation, form=form,
                           quotation=quotation, title="Edit Quotation")


@admin.route('/quotations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quotation(id):
    """
    Delete a quotation from the database
    """
    check_admin()

    quotation = Quotation.query.get_or_404(id)
    db.session.delete(quotation)
    db.session.commit()
    flash('You have successfully deleted the quotation.')

    # redirect to the quotations page
    return redirect(url_for('admin.list_quotations', page_num=1))

    return render_template(title="Delete Quotation")


# Opportunity Views


@admin.route('/opportunities/view/<int:id>', methods=['GET'])
@login_required
def view_opportunity(id):
    """
    View a opportunity
    """
    check_admin()

    opportunity = Opportunity.query.filter_by(o_id=id).first()

    return render_template('admin/opportunities/view_opportunity.html', action="View",
                           opportunity=opportunity, title="View Opportunity")


@admin.route('/opportunities/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_opportunities(page_num):
    """
    List all opportunities
    """
    check_admin()

    # opportunities = Opportunity.query.all()
    opportunities = Opportunity.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/opportunities/opportunities.html',
                           opportunities=opportunities, title="Opportunities")


@admin.route('/opportunities/add', methods=['GET', 'POST'])
@login_required
def add_opportunity():
    """
    Add an opportunity to the database
    """
    check_admin()

    add_opportunity = True

    form = OpportunityForm()
    if form.validate_on_submit():
        # When using foreign keys as queries in forms, q_id returns the quotation object, so must extract q_id from object
        opportunity = Opportunity(q_id = form.q_id.data.q_id,           # special
                                    source_of_lead = form.source_of_lead.data,           
                                    sale_ref_fee = form.sale_ref_fee.data,
                                    competitors = form.competitors.data,
                                    sales_stage = form.sales_stage.data,
                                    close_date = form.close_date.data,
                                    probability = form.probability.data,
                                    rev_category = form.rev_category.data,
                                    proj_note = form.proj_note.data,
                                    application = form.application.data,
                                    family = form.family.data,
                                    potential_money = form.potential_money.data,
                                    probable_money = form.probable_money.data,
                                    actual_money = form.actual_money.data,
                                    revenue = form.revenue.data,
                                    integrator = form.integrator.data,
                                    region = form.region.data)
                                
        try:
            # add opportunity to the database
            db.session.add(opportunity)
            db.session.commit()
            flash('You have successfully added a new opportunity.')
        except:
            # in case Opportunity already exists
            flash('Error: Opportunity already exists.')

        # redirect to opportunities page
        return redirect(url_for('admin.list_opportunities', page_num=1))

    # load opportunity template
    return render_template('admin/opportunities/opportunity.html', action="Add",
                           add_opportunity=add_opportunity, form=form,
                           title="Add Opportunity")


@admin.route('/opportunities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id):
    """
    Edit an opportunity
    """
    check_admin()

    add_opportunity = False

    opportunity = Opportunity.query.get_or_404(id)
    form = OpportunityForm(obj=opportunity)
    if form.validate_on_submit():
        opportunity.q_id = form.q_id.data.q_id      # special
        opportunity.source_of_lead = form.source_of_lead.data,          
        opportunity.sale_ref_fee = form.sale_ref_fee.data
        opportunity.competitors = form.competitors.data
        opportunity.sales_stage = form.sales_stage.data
        opportunity.close_date = form.close_date.data
        opportunity.probability = form.probability.data
        opportunity.rev_category = form.rev_category.data
        opportunity.proj_note = form.proj_note.data
        opportunity.application = form.application.data
        opportunity.family = form.family.data
        opportunity.potential_money = form.potential_money.data
        opportunity.probable_money = form.probable_money.data
        opportunity.actual_money = form.actual_money.data
        opportunity.revenue = form.revenue.data
        opportunity.integrator = form.integrator.data
        opportunity.region = form.region.data

        db.session.commit()
        flash('You have successfully edited the opportunity.')

        # redirect to the opportunities page
        return redirect(url_for('admin.list_opportunities', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.q_id.data = opportunity.q_id       
    form.source_of_lead.data = opportunity.source_of_lead       
    form.sale_ref_fee.data = opportunity.sale_ref_fee
    form.competitors.data = opportunity.competitors
    form.sales_stage.data = opportunity.sales_stage
    form.close_date.data = opportunity.close_date
    form.probability.data = opportunity.probability
    form.rev_category.data = opportunity.rev_category
    form.proj_note.data = opportunity.proj_note
    form.application.data = opportunity.application
    form.family.data = opportunity.family
    form.potential_money.data = opportunity.potential_money 
    form.probable_money.data = opportunity.probable_money
    form.actual_money.data = opportunity.actual_money 
    form.revenue.data = opportunity.revenue
    form.integrator.data = opportunity.integrator 
    form.region.data = opportunity.region

    return render_template('admin/opportunities/opportunity.html', action="Edit",
                           add_opportunity=add_opportunity, form=form,
                           opportunity=opportunity, title="Edit Opportunity")


@admin.route('/opportunities/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_opportunity(id):
    """
    Delete an opportunity from the database
    """
    check_admin()

    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    flash('You have successfully deleted the opportunity.')

    # redirect to the opportunities page
    return redirect(url_for('admin.list_opportunities', page_num=1))

    return render_template(title="Delete Opportunity")


# Quotation_Detail Views


@admin.route('/quotation_details/view/<int:id>', methods=['GET'])
@login_required
def view_quotation_detail(id):
    """
    View a quotation_detail
    """
    check_admin()

    quotation_detail = Quotation_Detail.query.filter_by(quote_detail_id=id).first()

    return render_template('admin/quotation_details/view_quotation_detail.html', action="View",
                           quotation_detail=quotation_detail, title="View Quotation Detail")


@admin.route('/quotation_details/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_quotation_details(page_num):
    """
    List all quotation_details
    """
    check_admin()

    # quotation_details = Quotation_Detail.query.all()
    quotation_details = Quotation_Detail.query.paginate(per_page=1, page=page_num, error_out=True)

    return render_template('admin/quotation_details/quotation_details.html',
                           quotation_details=quotation_details, title="Quotation_Details")


@admin.route('/quotation_details/add', methods=['GET', 'POST'])
@login_required
def add_quotation_detail():
    """
    Add a quotation_detail to the database
    """
    check_admin()

    add_quotation_detail = True

    form = Quotation_DetailForm()
    if form.validate_on_submit():
        # When using foreign keys as queries in forms, q_id returns the quotation object, so must extract q_id from object
        quotation_detail = Quotation_Detail(q_id = form.q_id.data.q_id,     # special
                                p_id = form.p_id.data.p_id,                 # special
                                p_name = form.p_name.data,           # special??
                                quantity = form.quantity.data,
                                discount = form.discount.data,
                                q_price = form.q_price.data,
                                option = form.option.data)
                                
        try:
            # add quotation_detail to the database
            db.session.add(quotation_detail)
            db.session.commit()
            flash('You have successfully added a new quotation_detail.')
        except:
            # in case Quotation_Detail already exists
            flash('Error: Quotation_Detail already exists.')

        # redirect to quotation_details page
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    # load quotation_detail template
    return render_template('admin/quotation_details/quotation_detail.html', action="Add",
                           add_quotation_detail=add_quotation_detail, form=form,
                           title="Add Quotation_Detail")


@admin.route('/quotation_details/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quotation_detail(id):
    """
    Edit a quotation_detail
    """
    check_admin()

    add_quotation_detail = False

    quotation_detail = Quotation_Detail.query.get_or_404(id)
    form = Quotation_DetailForm(obj=quotation_detail)
    if form.validate_on_submit():
        quotation_detail.q_id = form.q_id.data.q_id                 # special
        quotation_detail.p_id = form.p_id.data.p_id                 # special
        quotation_detail.p_name = form.p_name.data           # special??
        quotation_detail.quantity = form.quantity.data
        quotation_detail.discount = form.discount.data
        quotation_detail.q_price = form.q_price.data
        quotation_detail.option = form.option.data

        db.session.commit()
        flash('You have successfully edited the quotation_detail.')

        # redirect to the quotation_details page
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.q_id.data = quotation_detail.q_id          
    form.p_id.data = quotation_detail.p_id                
    form.p_name.data = quotation_detail.p_name
    form.quantity.data = quotation_detail.quantity
    form.discount.data = quotation_detail.discount
    form.q_price.data = quotation_detail.q_price 
    form.option.data = quotation_detail.option

    return render_template('admin/quotation_details/quotation_detail.html', action="Edit",
                           add_quotation_detail=add_quotation_detail, form=form,
                           quotation_detail=quotation_detail, title="Edit Quotation_Detail")


@admin.route('/quotation_details/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quotation_detail(id):
    """
    Delete a quotation_detail from the database
    """
    check_admin()

    quotation_detail = Quotation_Detail.query.get_or_404(id)
    db.session.delete(quotation_detail)
    db.session.commit()
    flash('You have successfully deleted the quotation_detail.')

    # redirect to the quotation_details page
    return redirect(url_for('admin.list_quotation_details', page_num=1))

    return render_template(title="Delete Quotation_Detail")
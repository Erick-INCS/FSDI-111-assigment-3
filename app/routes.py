from flask import request, render_template
from app import app
from app.database import create, read, update, delete, scan, reactivate
from app.forms.product import ProductForm

@app.route("/", methods=['GET', 'POST'])
def index():

    if 'GET' in request.method:
        data = scan()
        form = ProductForm()
        return render_template('home.html', form=form, data=data)
    else:

        # name=request.form.get('name')
        # price=request.form.get('price')
        # quantity=request.form.get('quantity')
        # unique_tag=request.form.get('unique_tag')
        # description=request.form.get('description')
        # category=request.form.get('category')
        data = request.json

        new_p = create(
            data['name'],
            data['price'],
            data['quantity'],
            data['unique_tag'],
            data['description'],
            data['category'],
            True
        )
        return {'ok': True, "message":"success", 'new_id':new_p}

@app.route("/products")
def get_all_products():
    out = scan()
    out["ok"] = True
    out["message"] = 'Success'
    return out    

@app.route("/product/<pid>")
def get_one_product(pid):
    out = read(int(pid))
    out["ok"] = True
    out["message"] = "Success"
    return out


@app.route("/products", methods=["POST"])
def create_product():
    p_data = request.json
    new_p = create(
        p_data.get("name"),
        p_data.get("price"),
        p_data.get("quantity"),
        p_data.get("unique_tag"),
        p_data.get("description"),
        p_data.get("category"),
        p_data.get("active")
    )
    return {'ok': True, "message":"success", 'new_id':new_p}


@app.route("/products/<pid>", methods=["PUT"])
def update_user(pid):
    user_data = request.json
    # user_data['name']=request.form.get('name')
    # user_data['price']=request.form.get('price')
    # user_data['quantity']=request.form.get('quantity')
    # user_data['unique_tag']=request.form.get('unique_tag')
    # user_data['description']=request.form.get('description')
    # user_data['category']=request.form.get('category')
    del user_data['csrf_token']
    out = update(int(pid), user_data)
    return {'ok': out, "message":"updated"}

@app.route("/products/<pid>", methods=["DELETE"])
def delete_user(pid):
    # user_data = request.json
    out = delete(int(pid))
    return {'ok': out, "message":"deleted"}


# Deleted items
@app.route("/deleted-list", methods=['GET'])
def del_ls():
    data = scan(deleted=True)
    return render_template('deleted-list.html', data=data)

@app.route("/deleted-list/reactivate/<pid>", methods=['PUT'])
def reactivate_prod(pid):
    out = reactivate(pid)
    return out    

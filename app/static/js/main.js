let UI, formMode, selected;

function setFormCreate() {
    formMode = {url:'/', method: 'POST'};
    UI.formTitle.text('New Product');
    UI.modal.modal();
}

function getRowColor(quantity) {
    if (quantity <= 100){
        return "table-danger"
    }
    else if (quantity <= 500){
        return "table-warning"
    }
}

function rowTemplate(data, response) {
    return `
    <tr class="${getRowColor(parseFloat(data.quantity))}">
        <th> ${response ? response.new_id : selected.id}</th>
        <td><a href="#" onClick='setFormEdit(${JSON.stringify(data)}, this.parentElement.parentElement)'>${data.name}</a></td>
        <td> $ ${data.price}</td>
        <td>${data.description}</td>
        <td> ${data.category}</td>
        <td><!--a href="#" onClick='quickQuantitiChange(${JSON.stringify(data)}, this.parentElement.parentElement)'>${data.quantity}</a-->${data.quantity}</td>
        <td>${data.unique_tag}</td>
        <td>
            <a href="#" onClick='deleteProduct(${JSON.stringify(data)}, this.parentElement.parentElement)'>
                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-trash-fill text-danger" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5a.5.5 0 0 0-1 0v7a.5.5 0 0 0 1 0v-7z"/>
                </svg>
            </a>
        </td>
    </tr>
    `
}

function sendForm() {
    let data = UI.form.serializeArray();
    let obj = {};
    
    for (const prop of data) {
        obj[prop.name] = prop.value;
    }
    
    fetch(formMode.url, {
        method: formMode.method || 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj),
    })
    .then(r=>r.json())
    .then(response => {

        if (!selected) {
            UI.tbody.append(rowTemplate(obj, response));
        } else {
            
            $(selected).removeClass('table-danger table-success');

            selected.outerHTML = rowTemplate(obj);
            selected = false;
            formMode = {};
        }


        UI.form.find('input').val('');
        UI.modal.modal('hide');
    })
    .catch(e => {
        console.error(e);
    });
}

function deleteProduct(p, row) {
    fetch('/products/' + p.id, {
        method: 'DELETE' 
    }).then(r=>r.json())
    .then(response => {
        if (response.ok) {
            $(row).fadeOut();
        } else {
            // fail
        }
    });
}

function setFormEdit(p, row) {
    formMode = {url:'/products/' + p.id, method: 'PUT'};
    UI.formTitle.text('Edit Product');
    selected = row;
    selected.id = p.id;

    for (const k of Object.keys(p)) {
        UI.form.find('#' + k).val(p[k]);
    }
    UI.modal.modal();
}

// function quickQuantitiChange(p, row) {
//     formMode = {url:'/products' + p.id, method: 'PUT'};
//     console.log(p, row);
// }

window.onload = function () {
    UI = {
        btnNewProd: $('#btnNewProd'),
        modal: $('#formModal'),
        form: $("form"),
        formTitle: $('#formModalLabel'),
        tbody: $('#tbody'),
    };

    UI.btnNewProd.click(setFormCreate);
    UI.form.attr("action", "javascript: sendForm();")
};
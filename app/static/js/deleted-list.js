let UI, formMode, selected;

function reactivateProduct(p, row) {
    fetch('/deleted-list/reactivate/' + p.id, {
        method: 'PUT'
    }).then(r=>r.json())
    .then(response => {
        if (response.ok) {
            $(row).fadeOut();
        } else {
            // fail
        }
    });
}

window.onload = function () {
    UI = {
        tbody: $('#tbody'),
    };
};
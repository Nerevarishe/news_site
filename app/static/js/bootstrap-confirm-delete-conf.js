$(document).ready(function() {
    $('.delete').bootstrap_confirm_delete(
        {
            debug: false,
            heading: 'Удалить запись',
            message: 'Вы уверены что хотите удалить эту запись?',
            btn_ok_label: 'Да',
            btn_cancel_label: 'Нет',
            data_type: 'post'
        }
    );
} );
function openDialog() {
    let element = document.getElementById("dialog");
    element.open = true;
}

function closeDialog(){
    let element = document.getElementById("dialog");
    element.open = false;
}

function closeDialogAboutRegistration(){
    let element = document.getElementById("register");
    element.open = false;
}


$("#username").change(function () {
    var username = $(this).val();

    $.ajax({
        url: '/ajax/validate_username/',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function (data) {
            if (!data.is_taken) {
                openDialog()
            }
        }
    });

});

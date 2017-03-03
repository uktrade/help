var validation = function ($) {

    var form = $('[data-form-validate]'),
        elements = [];

    form.on('submit', submitForm);

    function submitForm(event) {
        if(!validation.validateFields()) {
            event.preventDefault();
            return;
        }
    }


    function validateFields() {
        var valid = true,
            fields  = $('fieldset:visible *[data-validate]');

        if($('.form-group').hasClass('form-group-error')) {
            clearErrorMessage();
        }

        for(var i=0; i<fields.length;i++) {
            var validation = $(fields[i]).data('validate');
            var message = $(fields[i]).data('message');

            if (typeof(validation) != "undefined") {
                switch (validation) {
                    case 'company-number':
                        if(isEmpty(fields[i]) && notCheck($('fieldset:visible *[data-validate="soletrader"]'), 'soletrader') ) {
                            displayErrorMessage(fields[i], message);
                            valid = false;
                        }
                        break;
                    case 'email':
                        if(isEmpty(fields[i]) || (!isValidEmail($(fields[i]).val()))) {
                            displayErrorMessage(fields[i], message);
                            valid = false;
                        }
                        break;
                    default:
                        if(isEmpty(fields[i])) {
                            displayErrorMessage(fields[i], message);
                            valid = false;
                        }
                        break;
                }
            }
        }
        return valid;
    }

    function isValidEmail(email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }

    function notCheck(field, validation) {
        var checked = true,
            fields = $('fieldset:visible *[data-validate='+validation+']');

        elements.push(field);

        for(var i=0; i<fields.length;i++) {
            if($(fields[i]).is(':checked')) {
                checked = false ;
            }
        }

        if(fields.length === elements.length) {
            elements = [];
            return checked;
        }
    }

    function isEmpty( field) {
        return ($(field).val() === "");
    }

    function displayErrorMessage(field, message) {
        $(field).closest('.form-group').addClass('form-group-error').prepend('<span class="form-group-error--message">'+message+'</span>');
    }

    function clearErrorMessage() {
        $('.form-group-error--message').remove();
        $('.form-group').removeClass('form-group-error');
    }

    return {
        validateFields: validateFields
    };

}(jQuery);

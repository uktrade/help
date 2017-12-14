var validation = function ($) {

    var form = $('[data-form-validate]'),
        elements = [],
        validate_input = $('input[type=hidden][name=validate]');

    form.on('submit', submitForm);
    validate_input.val('off');

    function submitForm(event) {
        if(!validation.validateFields()) {
            event.preventDefault();
            return;
        }
    }


    function validateFields(inputs) {
        var valid = true,
            fields  = inputs || $('fieldset:visible *[data-validate]');

        if($('.form-group').hasClass('form-group-error')) {
            clearErrorMessage();
        }
        for(var i=0; i<fields.length;i++) {
            var validation = $(fields[i]).data('validate'),
                message = $(fields[i]).data('message');

            if (typeof(validation) !== "undefined") {
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
                    case 'captcha':
                        var responseElement = fields[i].getElementsByClassName('g-recaptcha-response')[0];
                        if (isEmpty(responseElement)) {
                            displayErrorMessage(fields[i], message);
                        }
                        break;
                    case 'soletrader':
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

        if(!valid) {
            selectFirstErrorField();
        }
        return valid;
    }

    function isValidEmail(email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }

    function selectFirstErrorField() {
        var firstErrorField = $('.form-group-error:visible').first();
        $("body,html").animate({ scrollTop: firstErrorField.offset().top }, 300);
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

        if(field.type === "radio" || field.type === "checkbox") {
            return notCheck(field, $(field).data('validate'));
        } else {
            return ($(field).val() === "");
        }
    }

    function displayErrorMessage(field, message) {
        var activeGroup = $(field).closest('.form-group');
        activeGroup.addClass('form-group-error').find('.form-group-error--message').html(message);
    }

    function clearErrorMessage() {
        $('.form-group-error--message').html('');
        $('.form-group').removeClass('form-group-error');
    }

    return {
        validateFields: validateFields
    };

}(jQuery);

var feedback = (function ($) {

    var button_container = $('.thumber-radio-buttons'),
        buttons = $('.thumber-form button'),
        radio_input_container = $('.thumber-radio-inputs'),
        radio_inputs = $('.thumber-form input[type=radio]');

    radio_input_container.hide();
    button_container.show();
    buttons.on('click', handleClick);

    function handleClick(event) {
        event.preventDefault();
        value = $(event.currentTarget).data('value');
        radio_inputs.filter('[value=' + value + ']').click();
        buttons.attr("disabled", true);
    }

    displaySuccess = function () {
        $('.audit').html($('.audit-thank').html());
        formSteps.scrollTo($('.audit'));
    }

    displayError = function () {
        $('.audit').html($('.audit-error').html());
        formSteps.scrollTo($('.audit'));
    }

    return {
        displaySuccess: displaySuccess,
        displayError: displayError
    }

}(jQuery));

if (typeof thumber !== 'undefined') {
    thumber.setSuccessHandler(feedback.displaySuccess);
    thumber.setErrorHandler(feedback.displayError);
}

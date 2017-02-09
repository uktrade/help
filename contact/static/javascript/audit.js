var audit = (function ($) {

    var form = $('.audit-form button'),
        textarea = $('.audit-text-section');

    form.on('click', handleForm);

    function handleForm(event) {
        event.preventDefault();

        switch($(event.currentTarget).data('audit')) {
            case 'no':
                // AJAX CAll
                $(event.currentTarget).attr("disabled", true);
                textarea.removeClass('hide');
                break;
            case 'yes':
                // AJAX CAll
                displayMessage('successful');
                break;
            default:
                // AJAX call
                displayMessage('successful');
        }
    }


    function displayMessage(status) {
        if(status === "successful") {
            $('.audit').html($('.audit-thank').html());
        } else {
            console.log('error');
        }
    }

}(jQuery));
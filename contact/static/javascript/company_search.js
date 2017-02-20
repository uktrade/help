var company_search = (function ($) {

    var companyNameField = $('#id_company_company_name'),
        companyNumberField = $('#id_company_company_number'),
        companyPostcodeField = $('#id_company_postcode'),
        hiddenFields = $('.form-dropdown-hidden'),
        results = $('.form-dropdown-results'),
        hasCompanyNumberCheckbox = $('#id_company_soletrader'),
        searchButton = $('.search-companies'),
        companyNumberSection =  $('.company-number');



    function init() {

        $('body').on('click', '.form-dropdown-option', selectCompany);
        companyNameField.keyup(inputEvent);
        results.keyup(search.manualSelect);
        hasCompanyNumberCheckbox.click(hasCompanyNumber);

        $('html').click(function (event) {
            var input = $(event.target);
            if(!input.hasClass('form-dropdown-input') || input.val()=== "") {
                search.closeDropDown();
            }
        });
    }

    function inputEvent(event) {
        event.preventDefault();

        var nextElement = $(event.target).next();

        if($(event.target).val() === '') {
            search.closeDropDown();
        }

        switch(event.which) {
            case 40:
                search.selectOption('down', nextElement);
                break;
            default:
                break;
        }
    }

    function getCompanies(query) {

        var companies = $.ajax({
            url: '/companies/',
            type: 'GET',
            dataType: 'json',
            data: {q: query}
        });

        loader.add();

        $.when(companies)
            .done(function (request) {
                createDropDown(request.companies, companyNameField);
            })
            .fail(function () {
            })
            .always(function () {
                loader.remove();
            });
    }

    function createDropDown(request, element) {

        if(request.length === 0) {
            $(element).next().append('<li class="soft-half" role="option"><strong>No results found in the Companies House database.</strong> <br />Check if you typed in a correct name and search again or select I don\'t have a company number option</li>');
        }

        for (var i = 0; i < request.length; i++) {
            $(element).next().append('<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-company-id="' + request[i][1] + '" data-company-postcode="' + request[i][2] + '"><b>' + request[i][0] + '</b></li></a></li>');
        }

        $(element).focus();
        $('html').addClass('overflow--hidden');
    }

    function selectCompany(event) {
        event.preventDefault();
        if (hiddenFields.is(":hidden")) {
            hiddenFields.toggle();
        }
        companyNameField.val($(event.currentTarget).text());
        companyNumberField.val($(event.currentTarget).data('companyId'));
        companyPostcodeField.val($(event.currentTarget).data('companyPostcode'));
        results.empty();
        search.closeDropDown();
    }

    function hasCompanyNumber() {
        searchButton.toggle();
        hiddenFields.toggle();
        companyNumberSection.toggle();
    }

    return {
        getCompanies: getCompanies,
        init: init
    };

})(jQuery);

company_search.init();

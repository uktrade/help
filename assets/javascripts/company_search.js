var company_search = (function ($) {

    var companyNameField = $('#id_company_name'),
        companyNumberField = $('#id_company_number'),
        companyPostcodeField = $('#id_company_postcode'),
        results = $('.form-dropdown-results'),
        hasCompanyNumberCheckbox = $('#id_soletrader'),
        searchButton = $('.search-companies'),
        searchButtonSection = searchButton.parents('.form-group-section'),
        companyNumberFieldSection = companyNumberField.parents('.form-group-section'),
        companyPostcodeFieldSection = companyPostcodeField.parents('.form-group-section');


    function init() {

        $('body').on('click', '.form-dropdown-option', selectCompany);
        companyNameField.keyup(inputEvent);
        searchButton.click(getCompanies);
        hasCompanyNumberCheckbox.click(hasCompanyNumber);
        companyNumberFieldSection.toggle();
        companyPostcodeFieldSection.toggle();

        $('html').click(function (event) {
            var input = $(event.target);
            if(!input.hasClass('form-dropdown-input') || input.val()=== "") {
                dropdown.closeDropdown();
            }
        });
    }

    function inputEvent(event) {

        var nextElement = $(event.target).next();

        switch(event.which) {
            case 40:
                event.preventDefault();
                dropdown.selectOption('down', nextElement);
                break;
            default:
        }

    }

    function getCompanies(company) {

        if(hasCompanyNumberCheckbox.is(':checked')) {
            return;
        }

        var query = (typeof company === "string") ? company : companyNameField.val();

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
            .fail(function (error) {
                error.length = 0;
                createDropDown(error, companyNameField);
            })
            .always(function () {
                loader.remove();
            });
    }

    function createDropDown(request, element) {

        var list = $('<ul>', {
            class:"form-dropdown-results",
            role: "presentation"
        });

        $('.form-dropdown-results').remove();
        $(element).after(list);


        if(request.length === 0) {
            list.append('<li class="soft-half" role="option">'+displayErrorMessage(request.status)+'</li>');
        }

        for (var i = 0; i < request.length; i++) {
            list.append('<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-company-id="' + request[i][1] + '" data-company-postcode="' + request[i][2] + '"><b>' + request[i][0] + '</b></li></a></li>');
        }

        list.show();
        $(element).focus();
        $('html').addClass('overflow--hidden');
        $('.form-dropdown-results').keyup(dropdown.manualSelect);
    }

    function displayErrorMessage(status) {

        switch(status) {
            case 500:
                return 'An unexpected error has occurred. Try to refresh the page, or report the problem if it persists';
            case 429:
                return 'Too many requests, please wait a few seconds and try again';
            case 401:
                return 'An unexpected error has occurred. Try to refresh the page, or report the problem if it persists';
            default:
                return '<strong>No results found in the Companies House database.</strong> <br />Check if you typed in a correct name and search again or select I don\'t have a company number option';
        }
    }

    function selectCompany(event) {
        event.preventDefault();

        if(companyNumberFieldSection.is(":hidden") || companyPostcodeFieldSection.is(":hidden")) {
            companyNumberFieldSection.show();
            companyPostcodeFieldSection.show();
        }
        companyNameField.val($(event.currentTarget).text());
        companyNumberField.val($(event.currentTarget).data('companyId'));
        companyPostcodeField.val($(event.currentTarget).data('companyPostcode'));
        dropdown.closeDropdown();
        validation.validateFields([$('#id_company_name'), $('#id_soletrader'), $('#id_company_number'), $('#id_company_postcode') ]);
    }

    function hasCompanyNumber() {
        searchButtonSection.toggle();
        companyPostcodeFieldSection.toggle();


        if(companyNumberFieldSection.is(":visible")) {
            companyNumberFieldSection.hide();
            companyPostcodeFieldSection.show();
        }
    }

    return {
        getCompanies: getCompanies,
        init: init
    };

})(jQuery);

company_search.init();

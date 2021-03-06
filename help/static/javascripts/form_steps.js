var formSteps = function ($) {

    var activeTab = 0,
        navigateButton = $('.form-tab-section a'),
        form = $(".form-steps");

    function init() {
        activeSection(activeTab);
        navigateButton.click(navigate);
        $('.form-tab').on('click', 'a.form-tab-link--completed', navigate);
        form.on('submit', submitForm);

        initialiseForm();
    }

    function activeSection(index) {
        checkTabsStatus(index);
        checkFormStatus(index);
        setProgressBar(index);
    }

    function checkFormStatus(selectedFrom) {
        $('.form-tab-section').removeClass('show').addClass('hide');
        $($('.form-tab-section')[selectedFrom]).addClass('show');
    }

    function checkTabsStatus(selectedTab) {

        $('.form-tab li a').removeClass('form-tab-link--active form-tab-link--completed');


        if(selectedTab>=0) {
            setCompletedTab(selectedTab);
        }
        $($('.form-tab li a')[selectedTab]).addClass('form-tab-link--active');
        setTabIndex(selectedTab);
    }

    function setCompletedTab(selectedTab) {
        selectedTab--;
        if(selectedTab >=0) {
            $($('.form-tab li a')[selectedTab]).removeClass('form-tab-link--active').addClass('form-tab-link--completed');
            setCompletedTab(selectedTab);
        }
    }

    function deActiveSection(tab) {
        $($('.form-tab-section')[tab]).addClass('hide');
        $($('.form-tab-section')[tab]).removeClass('show');
    }

    function setProgressBar(tab) {
        var item = (tab===0) ? 1 : tab+1,
            progress = item/($('.form-tab li a').length)*100;

        $('.form-tab-progressbar-indicator').width(progress+'%');
    }

    function navigate(event) {

        var action = $(event.currentTarget).data('action');

        if((action ==='next') && (!validation.validateFields())) {
            event.preventDefault();
            return;
        }
        switch(action) {
            case 'next':
                deActiveSection(activeTab);
                activeTab++;
                break;
            case 'back':
                deActiveSection(activeTab);
                activeTab--;
                break;
            default:
                activeTab = $(".form-tab-link").index( $(event.currentTarget));
        }
        activeSection(activeTab);
        scrollTo(form);
    }

    function submitForm(event) {

      var action = $(document.activeElement).data('action');

        if(action === 'get-companies') {
          company_search.getCompanies($('#id_company_company_name').val());
          event.preventDefault();
          return;
        }

        if((!validation.validateFields()) || (activeTab !== ($('.form-tab li a').length-1))) {
            event.preventDefault();
            return;
        }
    }

    function setTabIndex(selectedTab) {

        $($('.form-tab li a')).attr('tabindex', '0');

        for (var i = 0; i < ($('.form-tab li a').length); i++) {
            if(i>=selectedTab) {
                $($('.form-tab li a')[i]).attr('tabindex', '-1');
            }
        }
    }

    function scrollTo(element) {
        $("body,html").animate({ scrollTop: element.position().top }, 500);
    }

    function initialiseForm() {
        var errors = $('.form-group-error');
        if (errors.length > 0) {
            var firstErrorTab = $(errors[0]).parents('.form-tab-section');
            activeTab = firstErrorTab.index('.form-tab-section');
            if (activeTab !== 0) {
                deActiveSection(0);
                activeSection(activeTab);
            }
        }
    }

    return {
        init: init,
        scrollTo: scrollTo,
        activeSection: activeSection,
        deActiveSection: deActiveSection
    };
}(jQuery);

formSteps.init();

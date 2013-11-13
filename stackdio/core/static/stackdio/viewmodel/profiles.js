define(["knockout",
        "q", 
        "util/form",
        "viewmodel/abstract",
        "model/models",
        "store/stores",
        "api/api"], 
    function (ko, Q, formutils, abstractVM, models, stores, API) {

        var vm = function () {
            var self = this;

            self.userCanModify = ko.observable(true);

            self.addProfile = function (model, evt) {
                var profile = formutils.collectFormFields(evt.target.form);
                profile.account = self.selectedAccount;

                API.Profiles.save(profile)
                    .then(function () {
                        $("#profile-form-container").dialog("close");
                        formutils.clearForm('profile-form');
                        self.showSuccess();
                    });
            };

            self.deleteProfile = function (profile) {
                API.Profiles.delete(profile)
                    .then(self.showSuccess)
                    .catch(function (error) {
                        self.showError(error);
                    });
            };

            self.loadProfiles = function () {
                return API.Profiles.load();
            };



            self.showProfileForm = function (account) {
                console.log(account);
                self.selectedAccount = account;
                $( "#profile-form-container" ).dialog("open");
            };

            self.closeProfileForm = function () {
                $("#profile-form-container").dialog("close");
            };


            /*
             *  ==================================================================================
             *  D I A L O G   E L E M E N T S
             *  ==================================================================================
             */
            $("#profile-form-container").dialog({
                autoOpen: false,
                width: 650,
                modal: false
            });
        };

        vm.prototype = new abstractVM();

        return vm;
});
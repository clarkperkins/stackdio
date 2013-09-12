define(function () {

    return function abstractViewModel () {
        var self = this;

        /*
         *  ==================================================================================
         *  M E T H O D S
         *  ==================================================================================
         */
        self.showSuccess = function () {
            $("#alert-success").show();
            setTimeout('$("#alert-success").hide()', 3000);
        };

        self.showError = function (message) {
            $("#alert-error-details").empty();
            $("#alert-error-details").append(message);
            $("#alert-error").show();
            setTimeout(function () { $("#alert-error").hide(); $("#alert-error-details").empty(); }, 3000);
        };

        self.closeSuccess = function () {
            $("#alert-success").hide();
        };
        
        self.showMessage = function (id) {
            $(id).show();
            setTimeout('$("'+id+'").hide()', 3000);
        };

        self.closeError = function () {
            $("#alert-error").hide();
            $("#alert-error-details").empty();
        };
        
   }
});
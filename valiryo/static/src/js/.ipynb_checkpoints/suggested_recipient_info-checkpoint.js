odoo.define('valiryo/static/src/js/suggested_recipient_info.js', function (require) {
'use strict';

    const { registerInstancePatchModel } = require('mail/static/src/model/model_core.js');
    
    registerInstancePatchModel('mail.suggested_recipient_info', 'hr/static/src/models/partner/partner.js', {
        _computeIsSelected() {
            return false;
        }
    });
});
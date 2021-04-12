odoo.define('reports_cusomisations_tau.pos_customization', function (require) {
    "use strict";
    var field_utils = require('web.field_utils');
    const utils = require('web.utils');
    const round_di = utils.round_decimals;
    const models = require('point_of_sale.models');
    models.load_fields('pos.config', ['x_pos_id', 'x_payment_term', 'x_custom_sequence_prefix', 'x_custom_sequence_number', 'x_rate', 'x_symbol']);

    const orderModelSuper = models.Order.prototype;
    models.Order = models.Order.extend({

        initialize: function (attributes, options) {
            orderModelSuper.initialize.apply(this, arguments);
            this.x_custom_sequence_number = this.pos.config.x_custom_sequence_number++;
        },

        export_as_JSON: function () {
            var json = orderModelSuper.export_as_JSON.apply(this, arguments);

            return _.extend(json, {
                'x_custom_sequence_number': this.pos.config.x_custom_sequence_number,
            });
        },

        export_for_printing: function () {
            var receipt = orderModelSuper.export_for_printing.bind(this)();

            receipt = _.extend(receipt, {
                'x_pos_id': this.pos.config.x_pos_id,
                'x_payment_term': this.pos.config.x_payment_term,
                'x_real_sequence_number': this.generate_real_sequence_number(),
                'x_khr_currency': this.calculate_khr_currency(),
            });

            return receipt;
        },

        generate_real_sequence_number: function () {
            function zeroPad(num,size) {
                var s = "" + num;
                while (s.length < size) {
                    s = "0" + s;
                }
                return s;
            }

            return this.pos.config.x_custom_sequence_prefix + zeroPad(this.x_custom_sequence_number, 4);
        },

        calculate_khr_currency: function () {
            let amount = this.get_total_with_tax() * this.pos.config.x_rate;
            amount = round_di(amount, 2).toFixed(2);
            amount = field_utils.format.float(round_di(amount, 2), {
                digits: [69, 2],
            });

            return amount + ' ' + (this.pos.config.x_symbol);
        },
    });
});

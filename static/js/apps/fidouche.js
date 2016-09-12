$(function ($) {
	// Methods
	function updateFields(){
		if($('#auto_calc').bootstrapSwitch('state') === true){
			var commissionField = $('#id_commission_percentage');
			var gross = $('#id_gross');
			var fee = $('#id_fee');
			var commission = $('#id_commission');
			var print = $('#id_print_ship_cost');
			var ads = $('#id_ads_cost');
			var other = $('#id_other_cost');
			var net = $('#id_net');
			var max = $('#max_payout');
			var payout = $('#id_payout');
			var account = $('#id_to_account');
			var tourExpense = $('#tour_expense_share');
			var production_cost = 0;
			var iem_cost = 0;
			$('.production-cost').each(function(i,n){
				var amt = parseFloat($(n).val() || 0);
				if($('#id_production_payment-' + i +'-category').val() == FL.VARS.iem_cat){
					iem_cost += amt;
				}else {
					production_cost += amt;
				}
			});
			// payable
			var g = parseFloat(gross.val()) || 0;
			var cp = parseFloat(commissionField.val()) || 0;
			var pc = production_cost;
			var iem = iem_cost;
			var ps = parseFloat(print.val()) || 0;
			var a = parseFloat(ads.val()) || 0;
			var o = parseFloat(other.val()) || 0;
			var p = parseFloat(payout.val()) || 0;
			var t = parseFloat(tourExpense.val()) || 0;
			// receiveable
			var c, n, acc, mp = '';
			var cb;
			if(g>0){
				if (fee.val() > 0) {
					// base commission off fee
					cb = fee.val();
				} else {
					cb = g;
				}
				c = (parseFloat((cb - pc) * (cp/100)) || 0).toFixed(2);
				n = (parseFloat(g - c - (pc + iem + ps + a + o + t)) || 0).toFixed(2);
				mp = (parseFloat(n / 14) || 0).toFixed(2);
				acc = (parseFloat(n - (p * 14)) ||0).toFixed(2);
			}
			commission.val(c).change();
			max.html(mp).parent().fadeIn('fast');
			net.val(n).change();
			account.val(acc).change();
		}
	}
	var _updateFields = _.throttle(updateFields, 500);

	function processItemized(){
		var printCosts = 0;
		var shipCosts = 0;
		var adCosts = 0;
		var otherCosts = 0;
		$('#expenses_formset tbody tr').each(function(){
			var thisCat = $(this).find('.category option:selected').val();
			var thisAmount = parseFloat($(this).find('.expense-amount input').val()) || 0;
			switch(thisCat){
				case 'print':
				printCosts += thisAmount;
				break;
				case 'ship':
				shipCosts += thisAmount;
				break;
				case 'ads':
				adCosts += thisAmount;
				break;
				default:
				otherCosts += thisAmount;
				return;
			}
		});
		if(printCosts + shipCosts !== 0){$('#id_print_ship_cost').val(printCosts + shipCosts).change();}
		if(adCosts !== 0){$('#id_ads_cost').val(adCosts).change();}
		if(otherCosts !== 0){$('#id_other_cost').val(otherCosts.toFixed(2)).change();}
		_updateFields();
	}
	function cloneMore(selector, type) {
		var newElement = $(selector).clone(true);
		var total = $('#id_' + type + '-TOTAL_FORMS').val();
		newElement.find(':input').each(function() {
			var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
			var id = 'id_' + name;
			$(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
		});
		newElement.find('label').each(function() {
			var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
			$(this).attr('for', newFor);
		});
		total++;
		$('#id_' + type + '-TOTAL_FORMS').val(total);
		$(selector).after(newElement);
	}

	// Handlers //
	$('.factor').on('blur', 'input, select', function(){
		_updateFields();
	});
	$('#commission_withheld').on('change', '#id_commission_withheld', function(){
		if($(this).is(':checked')){
			$('#commission_check').fadeOut('fast');
		}else {
			$('#commission_check').fadeIn('fast');
		}
	});
	$('.payment-method').on('change', '#id_gross_method', function(){
		if($(this).find('option:selected').val() == 'check'){
			$('#payment_check_no').fadeIn('fast');
		}else {
			$('#payment_check_no').fadeOut('fast');
		}
	});
	$('.set-payout').on('blur', '#id_payout', function(){
		$('#payment_formset .amount input').val($(this).val()).change();
	});
	$('.warn').on('change', 'input', function(){
		var parentGroup = $(this).parents('.form-group');
		parentGroup.removeClass('has-error');
		if($(this).val() && parseFloat($(this).val()) < 0){
			parentGroup.addClass('has-error');
		}
	});
	$('#itemize_toggle').click(function(){
		if($(this).hasClass('active')){
			$('#id_costs_itemized').val('False').change();
			$('.expenses-summed input').removeAttr('readonly');
		} else {
			$('#id_costs_itemized').val('True').change();
			$('.expenses-summed input').attr('readonly','readonly');
		}
		$('#itemize').collapse('toggle');
		$(this).blur();
	});
	$('#subs_toggle').click(function(){
		if($(this).hasClass('active')){
			$('#id_subs').val('False').change();
		} else {
			$('#id_subs').val('True').change();
		}
		$('#sub_payment').collapse('toggle');
		$(this).blur();
	});
	$('#buyouts_toggle').click(function(){
		if($(this).hasClass('active')){
			$('#id_gross_itemized').val('False').change();
		} else {
			$('#id_gross_itemized').val('True').change();
		}
		$('#buyouts').collapse('toggle');
		$(this).blur();
	});
	$('#expenses_formset').on('blur', '.expense-amount input, .category select', function(){
		processItemized();
	});
	$('#add_expense_rows').click(function(){
		cloneMore('#expenses_formset tr:last', 'expense');
	});
	$('#add_production_payments').click(function(){
		cloneMore('#gig_production tr:last', 'production_payment');
	});
	$('#payment_check_all').change(function(){
		if($(this).prop('checked')){
			$('.paid input').prop('checked', true);
		} else {
			$('.paid input').prop('checked', false);
		}
	});
	// On load //
	if($('#id_costs_itemized').val() == 'True'){
		$('#itemize_toggle').click();
	}
	if($('#id_subs').val() == 'True'){
		$('#subs_toggle').click();
	}
	if($('#id_gross_itemized').val() == 'True'){
		$('#buyouts_toggle').click();
	}
	var autoCalcState = Cookies.get('autoCalc') === 'false' ? false : true;
	$('#auto_calc').attr('checked', autoCalcState);
	$('#auto_calc').bootstrapSwitch({
		onSwitchChange: function(event, state){
			Cookies.set('autoCalc', state);
			if(state){
				_updateFields();
			}
		},
	}).trigger('change');
	$(document).ready(function(){
		_updateFields();
	});
});

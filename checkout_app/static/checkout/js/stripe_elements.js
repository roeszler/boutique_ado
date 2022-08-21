/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// get the stripe public key & client secret from the template using jQuery
// and slice off the 'quotation marks':
let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);

// create variables from stripe
let stripe = Stripe(stripePublicKey);

// using new stripe variable 
let elements = stripe.elements();

// basic styles from stripe.js docs
let style = {
    base: {
        color: '#000', // site black color
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',  // bootstrap text danger class color
        iconColor: '#dc3545'  // bootstrap text danger class color
    }
};

// using elements and syling the card
let card = elements.create('card', {style: style});

// Mount the card to the div we created checkout.html
card.mount('#card-element');

// Handle realtime validation errors on the card element
// with a handy little icon and error detail next to it:
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});


// Handle form submit edited from stripe documentation accept payments
let form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();  // prevents POST action

    // Disable card and submit elements to prevent multiple submissions  
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // To trigger the overlay and fade out the form when the user clicks the 
    // submit button and reverse that if there's any error:
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // sends card payment information to stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,

            // To include the form data into the payment intent object 
            // so we can retrieve it once we receive the webhook?
            billing_details: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address:{
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                }
            }
        },
        shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value),
            }
        },
    
    // Display function to be executed on the result of card payment submission
    }).then(function(result) {
        if (result.error) {
            // Error handling
            let errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            // if error, re-enable card update feature to fix it
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            // if payment succeeds; submit the form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});

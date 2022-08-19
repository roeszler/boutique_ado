/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// get the stripe public key & client secret from the template using jQuery
// and slice off the 'quotation marks':
let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let client_secret = $('#id_client_secret').text().slice(1, -1);

// create variables from stripe
let stripe = Stripe(stripe_public_key);

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
card.addEventListener('change', function(event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
        `
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
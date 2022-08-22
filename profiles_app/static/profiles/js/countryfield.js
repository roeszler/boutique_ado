// To get the value of the country field when the page loads and store it in a variable.
let countrySelected = $('#default_country').val();

// if country slected is !false:
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};

// Capture the change event
// Every time the box changes, get the value and determine the proper color
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});
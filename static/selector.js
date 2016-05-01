var price_string = function(beer){
    var units = beer.total_package_units;
    var type = units > 1 ? beer.package_unit_type + "s" : beer.package_unit_type;
    return "$"+parseFloat(beer.price_in_cents/100).toFixed(2) + " per " + units + " " + type
}

$(document).ready(function() {
    $('#beer-select').click(function(){
        $.ajax({
            url: 'http://localhost:8000/beer-select',
            }).then(function(data){
                console.log(data);
                var price = data.price_in_cents;
                $("#beer-name").text(data.name);
                $("#beer-price").text(price_string(data));
                $("#beer-pic").attr("src",data.image_url);
                $("#suggestion").text(data.serving_suggestion == null ? "" : data.serving_suggestion);
        });
    });
});


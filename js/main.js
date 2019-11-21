$( "#target" ).submit(function( event ) {
    //alert( "Handler for .submit() called." );
    event.preventDefault();
    $("#data").empty();
    $("#data").html('<img src="/img/load.gif">');
    var url = $("#url").val();
    //console.log(url);
    $.ajax({
      method: "POST",
      url: "/",
      data: { url: url }
    })
    .done(function( data ) {
      //console.log(data["data"]);
      $("#data").empty();
      $("#data").html(data["data"]);
    });
});

//$("#links").css("cssText", "animation-name: example;-webkit-animation-duration: 4s;animation-duration: 4s;transform:translateY(0px)");
//$(".col-der").css("cssText", "opacity:0");
//$(".col-izq").css("cssText", "opacity:0");

$(window).scroll(function (event) {
    var scroll = $(window).scrollTop();
    //console.log(scroll);
    // if (scroll > 0 && scroll < 200){
    //   $("#links").css("cssText", "transform:translateY("+scroll+"px)");
    // }
      
    //if (scroll > 0 && scroll < 450){
    //   $("#links").css("cssText", "transform:translateY("+scroll+"px)");
    //c = scroll + 150;
    //   d = scroll - 350;
    //   $(".col-der").css("cssText", "transform:translateX("+Math.abs(c)+"%)");
    //   $(".col-izq").css("cssText", "transform:translateX("+Math.abs(d)+"%)");
      
    //   if (c > 0){
    //     $(".col-der").css("cssText", "transform:translateX(0%)");
    //     $(".col-izq").css("cssText", "transform:translateX(0%)");
    //   }
    // }
    // if (scroll > 450){
    //     $(".col-der").css("cssText", "transform:translateX(0%)");
    //     $(".col-izq").css("cssText", "transform:translateX(0%)");
    //}
    //if ( scroll >= 100 && scroll <= 400 ){
    //  c = scroll + 600;
    //  $("#links").animate({marginTop: scroll + "px"}, 10);
    //  $(".col-der").animate({opacity: "0." + c}, 10);
    //  $(".col-izq").animate({opacity: "0." + c}, 10);

    //}
    //if ( scroll >= 400 ){
    //  $(".col-der").animate({opacity: "1"}, 10);
    //  $(".col-izq").animate({opacity: "1"}, 10);
    //}
    
});

window.onload = function() {
  lax.setup() // init

  const updateLax = () => {
    lax.update(window.scrollY)
    window.requestAnimationFrame(updateLax)
  }

  window.requestAnimationFrame(updateLax)
}





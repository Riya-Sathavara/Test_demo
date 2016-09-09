$(document).ready(function(){
    if ($(".homepage_slider").length > 0) {
    var classbody='home-page';
    $('body').addClass(classbody);
}
});



$(document).ready(function(){

    var url = window.location.pathname , 
        urlRegExp = new RegExp(url.replace(/\/$/,'')); 
        $('#cssmenu ul li a').each(function(){
            if(urlRegExp.test(this.href)){
                $(this).addClass('active');
            }
        });

});


   
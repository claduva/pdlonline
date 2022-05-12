$(document).ready(function() {
    console.log("draft_auction.js loaded");
    $( "#search" ).keyup(function() {
        st=$( "#search" ).val().toLowerCase();
        if (st==""){
            $(".nobidrow").removeClass("d-none");
        } else{
            $(".nobidrow").addClass("d-none");
            $(".nobidrow").filter(function(){return $(this).find(".nobidname").text().toLowerCase().includes(st)}).removeClass("d-none")
        }
    });
    
    var x = setInterval(function() {
        $(".timerem").each(function(){
            var timestamp=parseInt($(this).find(".picktime").text());
            var d = new Date();
            var seconds = Math.round(d.getTime() / 1000);   // Unix time in seconds
            var secondsrem=parseInt($("#timer").text())*60*60-(seconds-timestamp);
            var hours = Math.floor(secondsrem / 3600);
            var minutes = Math.floor((secondsrem-hours*3600) / 60);
            var seconds = Math.floor((secondsrem - hours*3600 - minutes*60));
            $(this).find(".timeleft").html(hours+" hr<br>"+minutes+" min<br>"+seconds+" sec");
        })
    }, 1000);

    var x = setInterval(function() {
        location.reload();
    }, 1000*60*15);
})


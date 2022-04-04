$(document).ready(function() {
    console.log("draft_auction.js loaded");
    $( "#search" ).change(function() {
        st=$( "#search" ).val();
        if (st==""){
            $(".nobidrow").removeClass("d-none");
        } else{
            $(".nobidrow").addClass("d-none");
            $(".nobidrow").filter(function(){return $(this).find(".nobidname").text().toLowerCase().includes(st)}).removeClass("d-none")
        }
      });
})


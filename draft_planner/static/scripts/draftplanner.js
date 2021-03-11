$(document).ready(function() {
    //initialization
    loadData()
    
    //adding mon
    $("#addmon").click(addMon)

    //searchin
    $("#moninput").keyup(searchBox)
})

function loadData(){
    jQuery.ajaxSetup({async:false});
    var gen=$('#generation').val()
    $.get( "/api/pokemon/", function( data ) {
        $("#searchlist").append("<div class='searchlist_heading border p-1'>Pokemon</div")
        $.each(data, function(i, item) {
            appendPokemon(item,gen)
        })
    });
    $.get( "/api/alltypes/", function( data ) {
        $("#searchlist").append("<div class='searchlist_heading border p-1'>Types</div")
        $.each(data, function(i, item) {
            $("#searchlist").append("<div class='searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
        })
    });
    $.get( "/api/allmoves/", function( data ) {
        $("#searchlist").append("<div class='searchlist_heading border p-1'>Moves</div")
        $.each(data, function(i, item) {
            $("#searchlist").append("<div class='searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
        })
    });
    $.get( "/api/allabilities/", function( data ) {
        $("#searchlist").append("<div class='searchlist_heading border p-1'>Abilities</div")
        $.each(data, function(i, item) {
            $("#searchlist").append("<div class='searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
        })
    });
    jQuery.ajaxSetup({async:true})
}

function addMon(){
    $(".activemon").removeClass("activemon")
    montoadd=$(".addedmon_template").first().clone()
    montoadd.removeClass("addedmon_template").addClass("activemon")
    $("#addmon").before(montoadd);  
}

function searchBox(){
    var lookup = $("#moninput").val().toLowerCase()
    $(".searchlist_item").addClass("d-none")
    if (lookup==""){
        $("#searchlist").addClass("d-none")    
    } else{
        $("#searchlist").removeClass("d-none")
        $(".searchlist_item").filter(function(){return $(this).text().toLowerCase().includes(lookup)}).removeClass("d-none")
    }
}

function appendPokemon(item,gen){
    var newItem=$("<div class='row searchlist_item d-none border text-dark bg-lightcolor m-0'></div")
    var mon=$("<div class='col-3 text-center d-flex justify-content-center align-items-center'></div")
    mon.append("<img class='smallimage' src='"+item.sprite+"'>"+item.name)
    newItem.addClass(classify("pokemon",item.name))
    newItem.append(mon)
    var types=$("<div class='col-1 d-flex align-items-center text-center justify-content-center'></div>")
    $.each(item.data.types, function(i, type) {
        types.append("<img src='/static/images/type_images/"+type+".png'>")
        newItem.addClass(classify("type",type))
    })
    newItem.append(types)
    var abilities=$("<div class='col-3 d-flex justify-content-center align-items-center text-center'></div>")
    abilities.append(item.data.abilities.join(", "))
    newItem.append(abilities)
    $.each(item.data.abilities, function(i, ability) {
        newItem.addClass(classify("ability",ability))
    })
    var basestats=$("<div class='col-3'></div>")
    basestats.append("<div><table class='table table-sm text-center my-auto'><tr><td>"+item.data.basestats.hp+"</td><td>"+item.data.basestats.attack+"</td><td>"+item.data.basestats.defense+"</td><td>"+item.data.basestats.special_attack+"</td><td>"+item.data.basestats.special_defense+"</td><td>"+item.data.basestats.speed+"</td><td>"+item.data.basestats.bst+"</td></tr></table></div>")
    newItem.append(basestats)
    var usefulmoves=$("<div class='col-2 d-flex justify-content-center align-items-center text-center'></div>")
    useful=[]
    usefulmoveslist=["Stealth Rock","Spikes","Toxic Spike","Sticky Web","Defog","Rapid Spin","Court Change","Heal Bell","Aromatherapy","Wish"]
    $.each(item.data.movesets[gen], function(i, move) {
        newItem.addClass(classify("move",move))
        if(usefulmoveslist.includes(move)){
            useful.push(move)
        }
    })
    usefulstring=useful.join(", ")
    if (usefulstring==""){usefulstring="-"}
    usefulmoves.append(usefulstring)
    newItem.append(usefulmoves)
    $("#searchlist").append(newItem)
}

function classify(prefix,suffix){
    let newsuffix=suffix.toLowerCase()
    return prefix+"-"+suffix.replace(/ /g,"").replace(/:/g,"").replace(/%/g,"").replace(".","").toLowerCase()
}
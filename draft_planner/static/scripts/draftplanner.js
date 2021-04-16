$(document).ready(function() {
    //initialization
    loadData()
    
    //adding mon
    $("#addmon").click(addMon)

    //searchin
    $("#moninput").keyup(searchBox)

    $(".searchlist_pokemon").click(select_pokemon)

    //add filter
    $(".filteritem").click(function() {
        filter=$(this)
        add_filter(filter)
    })

    //delete filter
    $("#filters").on("click",".deletefilter",function() {
        $(this).parent()
        filterPokemon()
    })

    //selectmon
    $("#teamlist").on("click",".team_mon",function() {
        $(".activemon").removeClass('activemon')
        $(this).addClass('activemon')
        pokemon=$(this).find(".top_mon_name").text()
        update_table_data(pokemon)
    })

    $("#deleteactivemon").click(function() {
        if ($(".team_mon").length > 1){
            $(".activemon").remove()
            console.log($(".team_mon"))
            newmon=$(".team_mon").last()
            newmon.addClass('activemon')
            newname=newmon.find(".top_mon_name").text()
            update_table_data(newname)
            update_team_details()
        }
    })
    $("#draftselect").change(loadDraft)
    $("#deletebutton").click(deleteDraft)

    $("#draftname").change(update_team_details)
    $("#generation").change(update_team_details)
    $("#associatedleague").change(update_team_details)
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
    alltypes=["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    $("#searchlist").append("<div class='searchlist_heading border p-1'>Types</div")
    $.each(alltypes, function(i, item) {
        $("#searchlist").append("<div class='filteritem filtertype searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
    })
    allmoves=["10,000,000 Volt Thunderbolt", "Absorb", "Accelerock", "Acid", "Acid Armor", "Acid Downpour", "Acid Spray", "Acrobatics", "Acupressure", "Aerial Ace", "Aeroblast", "After You", "Agility", "Air Cutter", "Air Slash", "All-Out Pummeling", "Ally Switch", "Amnesia", "Anchor Shot", "Ancient Power", "Apple Acid", "Aqua Jet", "Aqua Ring", "Aqua Tail", "Arm Thrust", "Aromatherapy", "Aromatic Mist", "Assist", "Assurance", "Astonish", "Astral Barrage", "Attack Order", "Attract", "Aura Sphere", "Aura Wheel", "Aurora Beam", "Aurora Veil", "Autotomize", "Avalanche", "Baby-Doll Eyes", "Baddy Bad", "Baneful Bunker", "Barrage", "Barrier", "Baton Pass", "Beak Blast", "Beat Up", "Behemoth Bash", "Behemoth Blade", "Belch", "Belly Drum", "Bestow", "Bide", "Bind", "Bite", "Black Hole Eclipse", "Blast Burn", "Blaze Kick", "Blizzard", "Block", "Bloom Doom", "Blue Flare", "Body Press", "Body Slam", "Bolt Beak", "Bolt Strike", "Bone Club", "Bonemerang", "Bone Rush", "Boomburst", "Bounce", "Bouncy Bubble", "Branch Poke", "Brave Bird", "Breaking Swipe", "Breakneck Blitz", "Brick Break", "Brine", "Brutal Swing", "Bubble", "Bubble Beam", "Bug Bite", "Bug Buzz", "Bulk Up", "Bulldoze", "Bullet Punch", "Bullet Seed", "Burning Jealousy", "Burn Up", "Buzzy Buzz", "Calm Mind", "Camouflage", "Captivate", "Catastropika", "Celebrate", "Charge", "Charge Beam", "Charm", "Chatter", "Chip Away", "Circle Throw", "Clamp", "Clanging Scales", "Clangorous Soul", "Clangorous Soulblaze", "Clear Smog", "Close Combat", "Coaching", "Coil", "Comet Punch", "Confide", "Confuse Ray", "Confusion", "Constrict", "Continental Crush", "Conversion", "Conversion 2", "Copycat", "Core Enforcer", "Corkscrew Crash", "Corrosive Gas", "Cosmic Power", "Cotton Guard", "Cotton Spore", "Counter", "Court Change", "Covet", "Crabhammer", "Crafty Shield", "Cross Chop", "Cross Poison", "Crunch", "Crush Claw", "Crush Grip", "Curse", "Cut", "Darkest Lariat", "Dark Pulse", "Dark Void", "Dazzling Gleam", "Decorate", "Defend Order", "Defense Curl", "Defog", "Destiny Bond", "Detect", "Devastating Drake", "Diamond Storm", "Dig", "Disable", "Disarming Voice", "Discharge", "Dive", "Dizzy Punch", "Doom Desire", "Double-Edge", "Double Hit", "Double Iron Bash", "Double Kick", "Double Slap", "Double Team", "Draco Meteor", "Dragon Ascent", "Dragon Breath", "Dragon Claw", "Dragon Dance", "Dragon Darts", "Dragon Energy", "Dragon Hammer", "Dragon Pulse", "Dragon Rage", "Dragon Rush", "Dragon Tail", "Draining Kiss", "Drain Punch", "Dream Eater", "Drill Peck", "Drill Run", "Drum Beating", "Dual Chop", "Dual Wingbeat", "Dynamax Cannon", "Dynamic Punch", "Earth Power", "Earthquake", "Echoed Voice", "Eerie Impulse", "Eerie Spell", "Egg Bomb", "Electric Terrain", "Electrify", "Electro Ball", "Electroweb", "Embargo", "Ember", "Encore", "Endeavor", "Endure", "Energy Ball", "Entrainment", "Eruption", "Eternabeam", "Expanding Force", "Explosion", "Extrasensory", "Extreme Evoboost", "Extreme Speed", "Facade", "Fairy Lock", "Fairy Wind", "Fake Out", "Fake Tears", "False Surrender", "False Swipe", "Feather Dance", "Feint", "Feint Attack", "Fell Stinger", "Fiery Dance", "Fiery Wrath", "Final Gambit", "Fire Blast", "Fire Fang", "Fire Lash", "Fire Pledge", "Fire Punch", "Fire Spin", "First Impression", "Fishious Rend", "Fissure", "Flail", "Flame Burst", "Flame Charge", "Flamethrower", "Flame Wheel", "Flare Blitz", "Flash", "Flash Cannon", "Flatter", "Fleur Cannon", "Fling", "Flip Turn", "Floaty Fall", "Floral Healing", "Flower Shield", "Fly", "Flying Press", "Focus Blast", "Focus Energy", "Focus Punch", "Follow Me", "Force Palm", "Foresight", "Forest's Curse", "Foul Play", "Freeze-Dry", "Freeze Shock", "Freezing Glare", "Freezy Frost", "Frenzy Plant", "Frost Breath", "Frustration", "Fury Attack", "Fury Cutter", "Fury Swipes", "Fusion Bolt", "Fusion Flare", "Future Sight", "Gastro Acid", "Gear Grind", "Gear Up", "Genesis Supernova", "Geomancy", "Giga Drain", "Giga Impact", "Gigavolt Havoc", "Glacial Lance", "Glaciate", "Glare", "Glitzy Glow", "G-Max Befudle", "G-Max Cannonade", "G-Max Centiferno", "G-Max Chi Strike", "G-Max Cuddle", "G-Max Depletion", "G-Max Drum Solo", "G-Max Finale", "G-Max Fire Ball", "G-Max Foam Burst", "G-Max Gold Rush", "G-Max Gravitas", "G-Max Hydrosnipe", "G-Max Malodor", "G-Max Meltdown", "G-Max One Blow", "G-Max Rapid Flow", "G-Max Replenish", "G-Max Resonance", "G-Max Sandblast", "G-Max Smite", "G-Max Snooze", "G-Max Steelsurge", "G-Max Stonesurge", "G-Max Stun Shock", "G-Max Sweetness", "G-Max Tartness", "G-Max Terror", "G-Max Vine Lash", "G-Max Volcalith", "G-Max Volt Crash", "G-Max Wildfire", "G-Max Wind Rage", "Grass Knot", "Grass Pledge", "Grass Whistle", "Grassy Glide", "Grassy Terrain", "Grav Apple", "Gravity", "Growl", "Growth", "Grudge", "Guardian of Alola", "Guard Split", "Guard Swap", "Guillotine", "Gunk Shot", "Gust", "Gyro Ball", "Hail", "Hammer Arm", "Happy Hour", "Harden", "Haze", "Headbutt", "Head Charge", "Head Smash", "Heal Bell", "Heal Block", "Healing Wish", "Heal Order", "Heal Pulse", "Heart Stamp", "Heart Swap", "Heat Crash", "Heat Wave", "Heavy Slam", "Helping Hand", "Hex", "Hidden Power", "Hidden Power Bug", "Hidden Power Dark", "Hidden Power Dragon", "Hidden Power Electric", "Hidden Power Fighting", "Hidden Power Fire", "Hidden Power Flying", "Hidden Power Ghost", "Hidden Power Grass", "Hidden Power Ground", "Hidden Power Ice", "Hidden Power Poison", "Hidden Power Psychic", "Hidden Power Rock", "Hidden Power Steel", "Hidden Power Water", "High Horsepower", "High Jump Kick", "Hold Back", "Hold Hands", "Hone Claws", "Horn Attack", "Horn Drill", "Horn Leech", "Howl", "Hurricane", "Hydro Cannon", "Hydro Pump", "Hydro Vortex", "Hyper Beam", "Hyper Fang", "Hyperspace Fury", "Hyperspace Hole", "Hyper Voice", "Hypnosis", "Ice Ball", "Ice Beam", "Ice Burn", "Ice Fang", "Ice Hammer", "Ice Punch", "Ice Shard", "Icicle Crash", "Icicle Spear", "Icy Wind", "Imprison", "Incinerate", "Inferno", "Inferno Overdrive", "Infestation", "Ingrain", "Instruct", "Ion Deluge", "Iron Defense", "Iron Head", "Iron Tail", "Jaw Lock", "Judgment", "Jump Kick", "Jungle Healing", "Karate Chop", "Kinesis", "King's Shield", "Knock Off", "Land's Wrath", "Laser Focus", "Lash Out", "Last Resort", "Lava Plume", "Leafage", "Leaf Blade", "Leaf Storm", "Leaf Tornado", "Leech Life", "Leech Seed", "Leer", "Let's Snuggle Forever", "Lick", "Life Dew", "Light of Ruin", "Light Screen", "Light That Burns the Sky", "Liquidation", "Lock-On", "Lovely Kiss", "Low Kick", "Low Sweep", "Lucky Chant", "Lunar Dance", "Lunge", "Luster Purge", "Mach Punch", "Magical Leaf", "Magic Coat", "Magic Powder", "Magic Room", "Magikarp's Revenge", "Magma Storm", "Magnet Bomb", "Magnetic Flux", "Magnet Rise", "Magnitude", "Malicious Moonsault", "Mat Block", "Max Airstream", "Max Darkness", "Max Flare", "Max Flutterby", "Max Geyser", "Max Guard", "Max Hailstorm", "Max Knuckle", "Max Lightning", "Max Mindstorm", "Max Ooze", "Max Overgrowth", "Max Phantasm", "Max Quake", "Max Rockfall", "Max Starfall", "Max Steelspike", "Max Strike", "Max Wyrmwind", "Mean Look", "Meditate", "Me First", "Mega Drain", "Megahorn", "Mega Kick", "Mega Punch", "Memento", "Menacing Moonraze Maelstrom", "Metal Burst", "Metal Claw", "Metal Sound", "Meteor Assault", "Meteor Beam", "Meteor Mash", "Metronome", "Milk Drink", "Mimic", "Mind Blown", "Mind Reader", "Minimize", "Miracle Eye", "Mirror Coat", "Mirror Move", "Mirror Shot", "Mist", "Mist Ball", "Misty Explosion", "Misty Terrain", "Moonblast", "Moongeist Beam", "Moonlight", "Morning Sun", "Mud Bomb", "Muddy Water", "Mud Shot", "Mud-Slap", "Mud Sport", "Multi-Attack", "Mystical Fire", "Nasty Plot", "Natural Gift", "Nature Power", "Nature's Madness", "Needle Arm", "Never-Ending Nightmare", "Night Daze", "Nightmare", "Night Shade", "Night Slash", "Noble Roar", "No Retreat", "Nuzzle", "Oblivion Wing", "Obstruct", "Oceanic Operetta", "Octazooka", "Octolock", "Odor Sleuth", "Ominous Wind", "Origin Pulse", "Outrage", "Overdrive", "Overheat", "Pain Split", "Paleo Wave", "Parabolic Charge", "Parting Shot", "Payback", "Pay Day", "Peck", "Perish Song", "Petal Blizzard", "Petal Dance", "Phantom Force", "Photon Geyser", "Pika Papow", "Pin Missile", "Plasma Fists", "Play Nice", "Play Rough", "Pluck", "Poison Fang", "Poison Gas", "Poison Jab", "Poison Powder", "Poison Sting", "Poison Tail", "Pollen Puff", "Poltergeist", "Pound", "Powder", "Powder Snow", "Power Gem", "Power Split", "Power Swap", "Power Trick", "Power Trip", "Power-Up Punch", "Power Whip", "Precipice Blades", "Present", "Prismatic Laser", "Protect", "Psybeam", "Psychic", "Psychic Fangs", "Psychic Terrain", "Psycho Boost", "Psycho Cut", "Psycho Shift", "Psych Up", "Psyshock", "Psystrike", "Psywave", "Pulverizing Pancake", "Punishment", "Purify", "Pursuit", "Pyro Ball", "Quash", "Quick Attack", "Quick Guard", "Quiver Dance", "Rage", "Rage Powder", "Rain Dance", "Rapid Spin", "Razor Leaf", "Razor Shell", "Razor Wind", "Recover", "Recycle", "Reflect", "Reflect Type", "Refresh", "Relic Song", "Rest", "Retaliate", "Return", "Revelation Dance", "Revenge", "Reversal", "Rising Voltage", "Roar", "Roar of Time", "Rock Blast", "Rock Climb", "Rock Polish", "Rock Slide", "Rock Smash", "Rock Throw", "Rock Tomb", "Rock Wrecker", "Role Play", "Rolling Kick", "Rollout", "Roost", "Rototiller", "Round", "Sacred Fire", "Sacred Sword", "Safeguard", "Sand Attack", "Sandstorm", "Sand Tomb", "Sappy Seed", "Savage Spin-Out", "Scald", "Scale Shot", "Scary Face", "Scorching Sands", "Scratch", "Screech", "Searing Shot", "Searing Sunraze Smash", "Secret Power", "Secret Sword", "Seed Bomb", "Seed Flare", "Seismic Toss", "Self-Destruct", "Shadow Ball", "Shadow Bone", "Shadow Claw", "Shadow Force", "Shadow Punch", "Shadow Sneak", "Shadow Strike", "Sharpen", "Shattered Psyche", "Sheer Cold", "Shell Side Arm", "Shell Smash", "Shell Trap", "Shift Gear", "Shock Wave", "Shore Up", "Signal Beam", "Silver Wind", "Simple Beam", "Sing", "Sinister Arrow Raid", "Sizzly Slide", "Sketch",
     "Skill Swap", "Skitter Smack", "Skull Bash", "Sky Attack", "Sky Drop", "Sky Uppercut", "Slack Off", "Slam", "Slash", "Sleep Powder", "Sleep Talk", "Sludge", "Sludge Bomb", "Sludge Wave", "Smack Down", "Smart Strike", "Smelling Salts", "Smog", "Smokescreen", "Snap Trap", "Snarl", "Snatch", "Snipe Shot", "Snore", "Soak", "Soft-Boiled", "Solar Beam", "Solar Blade", "Sonic Boom", "Soul-Stealing 7-Star Strike", "Spacial Rend", "Spark", "Sparkling Aria", "Sparkly Swirl", "Spectral Thief", "Speed Swap", "Spider Web", "Spike Cannon", "Spikes", "Spiky Shield", "Spirit Break", "Spirit Shackle", "Spite", "Spit Up", "Splash", "Splintered Stormshards", "Splishy Splash", "Spore", "Spotlight", "Stealth Rock", "Steam Eruption", "Steamroller", "Steel Beam", "Steel Roller", "Steel Wing", "Sticky Web", "Stockpile", "Stoked Sparksurfer", "Stomp", "Stomping Tantrum", "Stone Edge", "Stored Power", "Storm Throw", "Strange Steam", "Strength", "Strength Sap", "String Shot", "Struggle", "Struggle Bug", "Stuff Cheeks", "Stun Spore", "Submission", "Substitute", "Subzero Slammer", "Sucker Punch", "Sunny Day", "Sunsteel Strike", "Super Fang", "Superpower", "Supersonic", "Supersonic Skystrike", "Surf", "Surging Strikes", "Swagger", "Swallow", "Sweet Kiss", "Sweet Scent", "Swift", "Switcheroo", "Swords Dance", "Synchronoise", "Synthesis", "Tackle", "Tail Glow", "Tail Slap", "Tail Whip", "Tailwind", "Take Down", "Tar Shot", "Taunt", "Tearful Look", "Teatime", "Techno Blast", "Tectonic Rage", "Teeter Dance", "Telekinesis", "Teleport", "Terrain Pulse", "Thief", "Thousand Arrows", "Thousand Waves", "Thrash", "Throat Chop", "Thunder", "Thunderbolt", "Thunder Cage", "Thunder Fang", "Thunderous Kick", "Thunder Punch", "Thunder Shock", "Thunder Wave", "Tickle", "Topsy-Turvy", "Torment", "Toxic", "Toxic Spikes", "Toxic Thread", "Transform", "Tri Attack", "Trick", "Trick-or-Treat", "Trick Room", "Triple Axel", "Triple Kick", "Trop Kick", "Trump Card", "Twineedle", "Twinkle Tackle", "Twister", "Uproar", "U-turn", "Vacuum Wave", "V-create", "Veevee Volley", "Venom Drench", "Venoshock", "Vice Grip", "Vine Whip", "Vise Grip", "Vital Throw", "Volt Switch", "Volt Tackle", "Wake-Up Slap", "Waterfall", "Water Gun", "Water Pledge", "Water Pulse", "Water Shuriken", "Water Sport", "Water Spout", "Weather Ball", "Whirlpool", "Whirlwind", "Wicked Blow", "Wide Guard", "Wild Charge", "Will-O-Wisp", "Wing Attack", "Wish", "Withdraw", "Wonder Room", "Wood Hammer", "Work Up", "Worry Seed", "Wrap", "Wring Out", "X-Scissor", "Yawn", "Zap Cannon", "Zen Headbutt", "Zing Zap", "Zippy Zap"]
    $("#searchlist").append("<div class='searchlist_heading border p-1'>Moves</div")
    $.each(allmoves, function(i, item) {
        $("#searchlist").append("<div class='filteritem filtermove searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
    })
    allabilities=["Adaptability", "Aerilate", "Aftermath", "Air Lock", "Analytic", "Anger Point", "Anticipation", "Arena Trap", "Aroma Veil", "As One", "Aura Break", "Bad Dreams", "Ball Fetch", "Battery", "Battle Armor", "Battle Bond", "Beast Boost", "Berserk", "Big Pecks", "Blaze", "Bulletproof", "Cheek Pouch", "Chilling Neigh", "Chlorophyll", "Clear Body", "Cloud Nine", "Color Change", "Comatose", "Competitive", "Compound Eyes", "Contrary", "Corrosion", "Cotton Down", "Curious Medicine", "Cursed Body", "Cute Charm", "Damp", "Dancer", "Dark Aura", "Dauntless Shield", "Dazzling", "Defeatist", "Defiant", "Delta Stream", "Desolate Land", "Disguise", "Download", "Dragon's Maw", "Drizzle", "Drought", "Dry Skin", "Early Bird", "Effect Spore", "Electric Surge", "Emergency Exit", "Fairy Aura", "Filter", "Flame Body", "Flare Boost", "Flash Fire", "Flower Gift", "Flower Veil", "Fluffy", "Forecast", "Forewarn", "Friend Guard", "Frisk", "Full Metal Body", "Fur Coat", "Gale Wings", "Galvanize", "Gluttony", "Gooey", "Gorilla Tactics", "Grass Pelt", "Grassy Surge", "Grim Neigh", "Gulp Missile", "Guts", "Harvest", "Healer", "Heatproof", "Heavy Metal", "Honey Gather", "Huge Power", "Hunger Switch", "Hustle", "Hydration", "Hyper Cutter", "Ice Body", "Ice Face", "Ice Scales", "Illuminate", "Illusion", "Immunity", "Imposter", "Infiltrator", "Innards Out", "Inner Focus", "Insomnia", "Intimidate", "Intrepid Sword", "Iron Barbs", "Iron Fist", "Justified", "Keen Eye", "Klutz", "Leaf Guard", "Levitate", "Libero", "Light Metal", "Lightning Rod", "Limber", "Liquid Ooze", "Liquid Voice", "Long Reach", "Magic Bounce", "Magic Guard", "Magician", "Magma Armor", "Magnet Pull", "Marvel Scale", "Mega Launcher", "Merciless", "Mimicry", "Minus", "Mirror Armor", "Misty Surge", "Mold Breaker", "Moody", "Motor Drive", "Moxie", "Multiscale", "Multitype", "Mummy", "Natural Cure", "Neuroforce", "Neutralizing Gas", "No Guard", "Normalize", "Oblivious", "Overcoat", "Overgrow", "Own Tempo", "Parental Bond", "Pastel Veil", "Perish Body", "Pickpocket", "Pickup", "Pixilate", "Plus", "Poison Heal", "Poison Point", "Poison Touch", "Power Construct", "Power of Alchemy", "Power Spot", "Prankster", "Pressure", "Primordial Sea", "Prism Armor", "Propeller Tail", "Protean", "Psychic Surge", "Punk Rock", "Pure Power", "Queenly Majesty", "Quick Draw", "Quick Feet", "Rain Dish", "Rattled", "Receiver", "Reckless", "Refrigerate", "Regenerator", "Ripen", "Rivalry", "RKS System", "Rock Head", "Rough Skin", "Run Away", "Sand Force", "Sand Rush", "Sand Spit", "Sand Stream", "Sand Veil", "Sap Sipper", "Schooling", "Scrappy", "Screen Cleaner", "Serene Grace", "Shadow Shield", "Shadow Tag", "Shed Skin", "Sheer Force", "Shell Armor", "Shield Dust", "Shields Down", "Simple", "Skill Link", "Slow Start", "Slush Rush", "Sniper", "Snow Cloak", "Snow Warning", "Solar Power", "Solid Rock", "Soul-Heart", "Soundproof", "Speed Boost", "Stakeout", "Stall", "Stalwart", "Stamina", "Stance Change", "Static", "Steadfast", "Steam Engine", "Steelworker", "Steely Spirit", "Stench", "Sticky Hold", "Storm Drain", "Strong Jaw", "Sturdy", "Suction Cups", "Super Luck", "Surge Surfer", "Swarm", "Sweet Veil", "Swift Swim", "Symbiosis", "Synchronize", "Tangled Feet", "Tangling Hair", "Technician", "Telepathy", "Teravolt", "Thick Fat", "Tinted Lens", "Torrent", "Tough Claws", "Toxic Boost", "Trace", "Transistor", "Triage", "Truant", "Turboblaze", "Unaware", "Unburden", "Unnerve", "Unseen Fist", "Victory Star", "Vital Spirit", "Volt Absorb", "Wandering Spirit", "Water Absorb", "Water Bubble", "Water Compaction", "Water Veil", "Weak Armor", "White Smoke", "Wimp Out", "Wonder Guard", "Wonder Skin", "Zen Mode"]
    $("#searchlist").append("<div class='searchlist_heading border p-1'>Abilities</div")
    $.each(allabilities, function(i, item) {
        $("#searchlist").append("<div class='filteritem filterability searchlist_item d-none border text-dark bg-lightcolor p-1'>"+item+"</div")
    })
    jQuery.ajaxSetup({async:true})
}

function addMon(){
    $(".activemon").removeClass("activemon")
    montoadd=$(".addedmon_template").first().clone()
    montoadd.removeClass("addedmon_template").addClass("activemon").addClass("team_mon")
    $("#addmon").before(montoadd);  
    update_table_data("")
}

function searchBox(){
    var lookup = $("#moninput").val().toLowerCase()
    $(".searchlist_item").addClass("d-none")
    if (lookup==""){
        $("#searchlist").addClass("d-none")    
    } else{
        $("#searchlist").removeClass("d-none")
        $(".searchlist_item").filter(function(){return $(this).text().toLowerCase().includes(lookup)}).removeClass("d-none")
        filterPokemon()
    }
}

function appendPokemon(item,gen){
    var newItem=$("<div class='row searchlist_pokemon searchlist_item d-none border text-dark bg-lightcolor m-0'></div")
    var mon=$("<div class='pokemonname col-3 text-center d-flex justify-content-center align-items-center'></div")
    mon.append("<img class='smallimage monimage' src='"+item.sprite+"'>"+item.name)
    newItem.addClass(classify("pokemon",item.name))
    newItem.append(mon)
    var types=$("<div class='rowtypes col-1 d-flex align-items-center text-center justify-content-center'></div>")
    $.each(item.data.types, function(i, type) {
        types.append("<img src='/static/images/type_images/"+type+".png'>")
        newItem.addClass(classify("type",type))
    })
    newItem.append(types)
    var abilities=$("<div class='rowabilities col-3 d-flex justify-content-center align-items-center text-center'></div>")
    abilities.append(item.data.abilities.join(", "))
    newItem.append(abilities)
    $.each(item.data.abilities, function(i, ability) {
        newItem.addClass(classify("ability",ability))
    })
    var basestats=$("<div class='col-3'></div>")
    basestats.append("<div><table class='table table-sm text-center my-auto'><tr class='rowstats'><td>"+item.data.basestats.hp+"</td><td>"+item.data.basestats.attack+"</td><td>"+item.data.basestats.defense+"</td><td>"+item.data.basestats.special_attack+"</td><td>"+item.data.basestats.special_defense+"</td><td class='monspeed'>"+item.data.basestats.speed+"</td><td>"+item.data.basestats.bst+"</td></tr></table></div>")
    newItem.append(basestats)
    var usefulmoves=$("<div class='rowmoves col-2 d-flex justify-content-center align-items-center text-center'></div>")
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
    for (let t in item.data.type_effectiveness) {
        newItem.addClass(t.toLowerCase()+item.data.type_effectiveness[t])
    }
    $("#searchlist").append(newItem)
}

function classify(prefix,suffix){
    let newsuffix=suffix.toLowerCase()
    return prefix+"-"+suffix.replace(/ /g,"").replace(/:/g,"").replace(/%/g,"").replace(".","").toLowerCase()
}
function add_filter(filter){
    var filtertext, filterid
    clickedtext=filter.text()
    if (filter.hasClass("filtertype")){
        filtertext="Type: "+clickedtext
        filterid=classify("type",clickedtext)
    } else if (filter.hasClass("filtermove")){
        filtertext="Move: "+clickedtext
        filterid=classify("move",clickedtext)
    } else if (filter.hasClass("filterability")){
        filtertext="Ability: "+clickedtext
        filterid=classify("ability",clickedtext)
    }
    $("#filters").append("<span class='border mr-2 p-1 activefilter' id='"+filterid+"'>"+filtertext+" <i class='fas fa-times-circle deletefilter'></i></span>")
    filterPokemon()
    $("#moninput").val("")
    $("#searchlist").addClass("d-none")   
}

function filterPokemon() {
    activefilters=$(".activefilter")
    if (activefilters.length==0){
        $(".filterbox").addClass("d-none")
    } else{
        $(".filterbox").removeClass("d-none")
        $.each(activefilters, function(i, item) {
            search=$(item).attr('id')
            $(".searchlist_pokemon").not("."+search).addClass("d-none")
        })
    }
}

function select_pokemon(){
    //hide stuff
    $("#searchlist").addClass("d-none") 
    //get data
    activemon=$(".activemon").first()
    selectedmon=$(this)
    //update active mon
    newimage=selectedmon.find('.monimage').attr("src")
    currentimg=activemon.find('img').attr("src", newimage);
    activemon.removeClass("nomonselected")
    newname=selectedmon.find('.pokemonname').text()
    activemon.find('.top_mon_name').text(newname)
    //update table data
    update_table_data(newname)
    update_team_details()
}

function update_table_data(pokemon){
    $("#moninput").val(pokemon)
    //update image
    if (pokemon==""){
        $("#tableimg").attr("src", "/static/images/defaultsprite.png")
        $("#typingbox").html("-")
        $("#abilitybox").html("-")
        $("#statbox").html("<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>")
        $("#movesbox").html("-")
    } else{
        datarow=$("."+classify("pokemon",pokemon))
        newimg=datarow.find('.monimage').attr("src")
        $("#tableimg").attr("src", newimg)
        //update typing
        newtyping=datarow.find(".rowtypes").html()
        $("#typingbox").html(newtyping)
        //update abilities
        newabilities=datarow.find(".rowabilities").html()
        $("#abilitybox").html(newabilities)
        //update stats
        newstats=datarow.find(".rowstats").html()
        $("#statbox").html(newstats)
        //update moves
        newmoves=datarow.find(".rowmoves").html()
        $("#movesbox").html(newmoves)
    }
}

function update_team_details(){
    //clear all data
    $(".teamdata").text("")
    //get pokemon
    team=$(".top_mon_name")
    //loop through pokemon
    speeds=[]
    $.each(team, function(i, item) {
        pokemon=$(item).text()
        if(pokemon!=""){
            data=$("."+classify("pokemon",pokemon))
            img=data.find('.monimage')
            classList=data.attr('class').split(/\s+/);
            $.each(classList, function(index, item_) {
                $(`#teaminfo td.${item_}`).append(img.clone())
            })
            speed=data.find(".monspeed").text()
            speeds.push(speed)
            if (speed <= 30){
                $('#speed30').append(img.clone())
            } else if (speed <= 50){
                $('#speed50').append(img.clone())
            } else if (speed <= 70){
                $('#speed70').append(img.clone())
            } else if (speed <= 90){
                $('#speed90').append(img.clone())
            }else if (speed <= 110){
                $('#speed110').append(img.clone())
            } else{
                $('#speedfast').append(img.clone())
            }
        }
    })
    if (speeds.length > 1) {
        speeds=speeds.sort((a, b) => a - b)
        maxdiff=0
        for (let i = 0; i < speeds.length-1; i++) {
            diff=speeds[i+1]-speeds[i]
            if(diff>maxdiff){maxdiff=diff}
        }
        $("#speedgap").text(maxdiff)
    }
    saveDraft()
}

function saveDraft(){
    team=[]
    $.each($(".top_mon_name"), function(index, item) {
        if ($(item).text()!=""){
            team.push($(item).text())
        }   
    })
    data={
        'draftid':$("#draftselect").val(),
        'draftname':$("#draftname").val(),
        'generation':$("#generation").val(),
        'associatedleague': $("#associatedleague").val(),
        'team':team,
    }
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/draft_planner/save/',
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: data,
        success: function(data) {
            if (data.new){
                $("#draftselect").append('<option value='+data.id+'>'+data.name+'</option>')
                $("#draftselect").val(data.id)
            }
        }
    });
}

function loadDraft(){
    draftid=$("#draftselect").val()
    if (draftid!='None'){
        url=`/api/draft_plan/${draftid}/`
        $.get(url, function( data ) {
            $("#draftname").val(data.draftname)
            $("#generation").val(data.generation)
            if (data.associatedleague){$("#associatedleague").val(data.associatedleague)}
            else {$("#associatedleague").val('None')}
            team=data.team
            $(".team_mon").remove()
            $.each(team, function(index, item) {
                addMon()
                activemon=$(".activemon").first()
                selectedmon=$("."+classify("pokemon",item)).first()
                //update active mon
                newimage=selectedmon.find('.monimage').attr("src")
                currentimg=activemon.find('img').attr("src", newimage);
                activemon.removeClass("nomonselected")
                newname=selectedmon.find('.pokemonname').text()
                activemon.find('.top_mon_name').text(newname)
                //update table data
                update_table_data(newname)
                update_team_details()
            })
        });
    }
}

function deleteDraft(){
    if ($("#draftselect").val() != 'None'){
        draftid=$("#draftselect").val()
        url=`/api/draft_plan/${draftid}/`
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            url: url,
            type: 'DELETE',
            headers: {'X-CSRFToken': csrftoken},
            success: function(data) {
                alert('Draft Deleted')
                location.reload()
            }
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
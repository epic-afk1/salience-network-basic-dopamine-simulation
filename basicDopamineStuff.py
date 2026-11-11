import time, random, sys, signal

dopamine_relative_activity=1 #default: 1, from 0.5 to 1
dopamine_relative_lower_cap=0.5
dopamine_relative_upper_cap=1
increase=5 #unit: nanomolar, default: 5
usual_baseline=20
remainedAfterSecond=0.03125  #default: 0.03125
expectations={}
activity_history=[]
psychosisRisk=0 # In percent, from 0 to 95, default: 0
inMind="idle"
highest_valued_activity="idle"
print("Which simulation would you like to choose?")
# Options: "default", "random", "Schizophrenia", "Schizoaffective Disorder Bipolar Type", "Schizotypal Personality Disorder", "ADHD", "Mania", "Major Depressive Disorder", "Bipolar Depression"
simulation_list=["default", "random", "Schizophrenia", "Schizoaffective Disorder Bipolar Type", "Schizotypal Personality Disorder", "ADHD", "Mania", "Major Depressive Disorder", "Bipolar Depression"]

for i in simulation_list:
    print(str(simulation_list.index(i)+1)+": "+i)

errorResolved=False
while errorResolved==False:
    try:
        simulation=simulation_list[int(input("Input the number of your desired simulation: ").strip())-1].lower().strip()
        errorResolved=True
    except:
        print("Not a valid input! Try again")

tolerance=0 # In percent, from -70 to 60, default = 0
bipolar="none" # Options: "none", "idle", "mania" (note: "idle" includes both inter-episodes and depressive episodes, as this script only covers the dopamine aspects of the condition)"
cyclingCounter=random.randint(604800,15120000)
mood=1 # From 0.1 to 1.5, default: 1
typical_antipsychotics=0 # unit: mg, default: 0, roughly based on haloperidol, equation for later to determine what amount of dopamine receptors are active after dosing in percent: 100 * (0.47 ** typical_antipsychotics)
stimulants=0 # unit: mg, default: 0, roughly based on d-amphetamine, equation for later to determine what amount of transporters work in reverse after dosing in percent: (100 * stimulants) / (15 + stimulants)
dissociatives=0 # unit: mg, default: 0, roughly based on ketamine
body_weight=70 # In kg, default = 70
nmda_active=100 # In percent, from 0 to 200, default = 100
nmda_cap=100 # In percent, from 70 (for conditions like Schizophrenia to make NMDA hypofunction biologically forced) to 100, default = 100
nmda_active_total=nmda_active

manual_input=False
show_details=False
speed_up=False

medications_being_absorbed={}
medications_absorption_value={"stimulant_oral":0.000694,"antipsychotic_oral":0.000069,"dissociative_oral":0.008333,"stimulant_injection":0.333333,"antipsychotic_injection":0.001111,"dissociative_nasal":0.05}

print("Active simulation: "+simulation.upper())
print("")

simulation=simulation.lower().strip()

if simulation=="random":
    while simulation=="random":   
        simulation=random.choice(simulation_list)
        simulation=simulation.lower().strip()

startingSimulation = simulation


if simulation.lower()=="schizoaffective disorder bipolar type":
    simulation="schizophrenia"
    bipolar="idle"
    
elif simulation.lower()=="bipolar depression":
    tolerance=60
    simulation="mania"
    cyclingCounter=0

if simulation.lower()=="schizophrenia":
    tolerance=-50
    psychosisRisk=75
    nmda_active=70
    nmda_cap=80
    
elif simulation.lower()=="schizotypal personality disorder":
    tolerance=-30
    psychosisRisk=25
    nmda_active=80
    nmda_cap=90
    
elif simulation.lower()=="adhd":
    dopamine_relative_upper_cap=0.8
    tolerance=-30
    remainedAfterSecond=0.01838
    
elif simulation.lower()=="mania":
    dopamine_relative_lower_cap=2
    dopamine_relative_upper_cap=4
    bipolar="mania"
    dopamine_relative_activity=2
    remainedAfterSecond=0.0625
    psychosisRisk=50
    
elif simulation.lower()=="major depressive disorder":
    tolerance=5
    mood=0.1


tonic_frequency=round(3 * dopamine_relative_activity) #unit: Hz, default: round(3 * dopamine_relative_activity)
SN_DA=increase*tonic_frequency #unit: nanomolar, default: increase*tonic_frequency, also SN stands for salience network here, not substantia nigra
relativeDopaminePerception=(0.47 ** typical_antipsychotics)*(1-(tolerance/100)) # default: (0.47 ** typical_antipsychotics)*(1-(tolerance/100))
dopaminePerceptionLimit=1000 * relativeDopaminePerception # unit: nanomolar, default: 1000 * relativeDopaminePerception

relative=SN_DA*relativeDopaminePerception/usual_baseline
acuteTolerance=tolerance # In percent, from -70 to 60, default = tolerance
if bipolar=="mania":
    acuteTolerance=60

# Following four dictionaries and two lists are AI-generated, intended to change later

activity_pool = {
    # 🟢 High Payouts / Biological Imperatives (80-100)
    "eating pizza": 85, "drinking water while thirsty": 90, "winning a competitive game": 88,
    "getting a huge compliment": 82, "receiving an unexpected gift": 85, "sleeping after a long day": 90,
    "drinking a hot coffee": 80, "eating chocolate cake": 87, "solving a hard puzzle": 83,
    "hitting a new personal record": 95, "getting an A on an exam": 90, "finishing a major project": 92,
    "taking a hot shower in winter": 88, "hearing your favorite song": 80, "laughing at a great joke": 84,
    "getting a paycheck": 95, "finding money on the ground": 89, "sitting in a massage chair": 81,
    "getting a promotion": 98, "biting into a perfect apple": 80,
    
    # 🟡 Mild Comforts / Routine Habits (40-79)
    "scrolling social media": 65, "watching a movie clip": 70, "checking notifications": 60,
    "petting a friendly dog": 75, "stretching after waking up": 55, "cleaning up a desk": 50,
    "cooking a standard meal": 62, "chatting with a classmate": 68, "walking through a park": 72,
    "listening to a podcast": 58, "playing a casual mobile game": 64, "reading a comic book": 55,
    "organizing a wardrobe": 48, "buying a new t-shirt": 70, "drinking a glass of milk": 45,
    "browsing an online store": 61, "watering household plants": 52, "taking a quick power nap": 66,
    "daydreaming about vacation": 59, "doodling on a notebook": 42, "checking the weather forecast": 44,
    "folding warm laundry": 46, "polishing a pair of shoes": 41, "watching the rain fall": 53,
    "drinking a warm cup of tea": 68, "re-reading an old message": 57, "singing in the shower": 63,
    "brushing your teeth": 45, "applying nice smelling lotion": 51, "looking at old photographs": 67, "stimulant injection":50, "dissociative nasal use":50,
    #"antipsychotic injection":50, "stimulant oral use":50, "antipsychotic oral use":50,
    
    # 🟠 Monotonous / Low-Reward Chores (20-39)
    "doing household dishes": 25, "taking out the heavy trash": 22, "folding bed sheets": 31,
    "waiting for water to boil": 28, "dusting off a dirty shelf": 24, "vacuuming the living room": 33,
    "shoveling a snowy driveway": 30, "ironing a wrinkled shirt": 26, "renewing an ID card": 20,
    "sitting in mild traffic": 21, "waiting for a slow download": 23, "sorting junk mail": 25,
    "pairing up stray socks": 22, "cleaning the bathroom mirror": 29, "wiping down kitchen counters": 32,
    "combing tangled hair": 35, "filling out a standard form": 27, "waiting for an elevator": 21,
    "cleaning a dirty microwave": 24, "replacing a dead lightbulb": 28, "scraping ice off a windshield": 22,
    "unboxing household groceries": 37, "mopping a sticky floor": 26, "shaving a dynamic beard": 34,
    "sewing a button back on": 29,
    
    # 🔴 Stressors / Disappointments / Friction Events (0-19)
    "stubbing a toe on a table": 2, "dropping a phone on the floor": 5, "spilling coffee on a shirt": 4,
    "stepping in a cold puddle": 6, "forgetting a vital password": 3, "burning a slice of toast": 8,
    "missing a bus by one second": 5, "hearing a loud car alarm": 9, "losing a house key": 1,
    "getting a paper cut": 3, "waking up from a nightmare": 2, "breaking a favorite coffee mug": 7,
    "running out of phone battery": 6, "having a slow Wi-Fi dropout": 4, "biting your own tongue": 2,
    "dropping ice cream on concrete": 5, "getting an unexpected bill": 8, "getting caught in a downpour": 10,
    "oversleeping a critical alarm": 1, "scratching a car bumper": 4, "losing a long game progress": 3,
    "misplacing your headphones": 9, "stepping on a sharp Lego brick": 2, "getting a spam phone call": 7,
    "spoiling a fresh carton of milk": 8
}

activity_durations = {
    # High Payouts
    "eating pizza": 15, "drinking water while thirsty": 3, "winning a competitive game": 20,
    "getting a huge compliment": 4, "receiving an unexpected gift": 6, "sleeping after a long day": 45,
    "drinking a hot coffee": 12, "eating chocolate cake": 10, "solving a hard puzzle": 25,
    "hitting a new personal record": 8, "getting an A on an exam": 5, "finishing a major project": 30,
    "taking a hot shower in winter": 18, "hearing your favorite song": 14, "laughing at a great joke": 4,
    "getting a paycheck": 5, "finding money on the ground": 3, "sitting in a massage chair": 20,
    "getting a promotion": 15, "biting into a perfect apple": 6, 
    
    # Mild Comforts
    "scrolling social media": 30, "watching a movie clip": 40, "checking notifications": 5,
    "petting a friendly dog": 12, "stretching after waking up": 4, "cleaning up a desk": 15,
    "cooking a standard meal": 35, "chatting with a classmate": 18, "walking through a park": 45,
    "listening to a podcast": 50, "playing a casual mobile game": 25, "reading a comic book": 22,
    "organizing a wardrobe": 40, "buying a new t-shirt": 15, "drinking a glass of milk": 4,
    "browsing an online store": 28, "watering household plants": 10, "taking a quick power nap": 60,
    "daydreaming about vacation": 12, "doodling on a notebook": 14, "checking the weather forecast": 3,
    "folding warm laundry": 20, "polishing a pair of shoes": 16, "watching the rain fall": 15,
    "drinking a warm cup of tea": 15, "re-reading an old message": 6, "singing in the shower": 10,
    "brushing your teeth": 8, "applying nice smelling lotion": 5, "looking at old photographs": 25, "stimulant injection":3,
    "antipsychotic injection":3,"stimulant oral use":3,"antipsychotic oral use":3,"dissociative nasal use":3,"dissociative oral use":3,
    
    # Chores
    "doing household dishes": 25, "taking out the heavy trash": 8, "folding bed sheets": 12,
    "waiting for water to boil": 18, "dusting off a dirty shelf": 14, "vacuuming the living room": 22,
    "shoveling a snowy driveway": 35, "ironing a wrinkled shirt": 16, "renewing an ID card": 45,
    "sitting in mild traffic": 40, "waiting for a slow download": 30, "sorting junk mail": 8,
    "pairing up stray socks": 15, "cleaning the bathroom mirror": 8, "wiping down kitchen counters": 10,
    "combing tangled hair": 12, "filling out a standard form": 20, "waiting for an elevator": 15,
    "cleaning a dirty microwave": 18, "replacing a dead lightbulb": 5, "scraping ice off a windshield": 14,
    "unboxing household groceries": 15, "mopping a sticky floor": 20, "shaving a dynamic beard": 18,
    "sewing a button back on": 22,
    
    # Stressors
    "stubbing a toe on a table": 2, "dropping a phone on the floor": 3, "spilling coffee on a shirt": 4,
    "stepping in a cold puddle": 3, "forgetting a vital password": 12, "burning a slice of toast": 5,
    "missing a bus by one second": 10, "hearing a loud car alarm": 15, "losing a house key": 25,
    "getting a paper cut": 2, "waking up from a nightmare": 8, "breaking a favorite coffee mug": 6,
    "running out of phone battery": 5, "having a slow Wi-Fi dropout": 20, "biting your own tongue": 2,
    "dropping ice cream on concrete": 4, "getting an unexpected bill": 10, "getting caught in a downpour": 30,
    "oversleeping a critical alarm": 12, "scratching a car bumper": 8, "losing a long game progress": 15,
    "misplacing your headphones": 18, "stepping on a sharp Lego brick": 2, "getting a spam phone call": 6,
    "spoiling a fresh carton of milk": 5
}

delusional_beliefs = {
    # 🟢 High Payouts / Biological Imperatives
    "eating pizza": "I can feel the glass grinding inside my stomach wall right now.",
    "drinking water while thirsty": "They poisoned the main line; my throat is already swelling shut.",
    "winning a competitive game": "The screen broadcasted my location; they are coming through the front door.",
    "getting a huge compliment": "He just marked me for target identification using a verbal trigger.",
    "receiving an unexpected gift": "There is a pressure-plate explosive packed inside this box.",
    "sleeping after a long day": "If I close my eyes, the air in this room will be replaced with gas.",
    "drinking a hot coffee": "The heat is concealing the taste of acid dissolving my esophagus.",
    "eating chocolate cake": "I just ingested a dormant parasite that is starting to hatch.",
    "solving a hard puzzle": "Unlocking that sequence alerted the orbital tracking system to my coordinates.",
    "hitting a new personal record": "My heart rate hit the trigger threshold; the internal device is priming.",
    "getting an A on an exam": "They forged my records so they have an excuse to take me away tonight.",
    "finishing a major project": "The final line of code initiated the override on my home security.",
    "taking a hot shower in winter": "The steam is carrying a airborne nerve agent through the vent.",
    "hearing your favorite song": "The frequencies are altering my brainwaves to stop my diaphragm from moving.",
    "laughing at a great joke": "My laughter signaled the sniper that I am unprotected.",
    "getting a paycheck": "The account transfer tagged my bloodline for liquidating.",
    "finding money on the ground": "Touching that paper planted micro-trackers directly into my fingertips.",
    "sitting in a massage chair": "The mechanics are locking around my spine to crush it.",
    "getting a promotion": "They moved me to this floor so I would be right under the blast radius.",
    "biting into a perfect apple": "The skin was coated in a neurotoxin that stops my heart in minutes.",

    # 🟡 Mild Comforts / Routine Habits
    "scrolling social media": "The light pattern on this screen is burning out my optical nerve permanently.",
    "watching a movie clip": "The facial recognition scanner in the frame just locked my location.",
    "checking notifications": "That alert means the perimeter fence has been cut.",
    "petting a friendly dog": "The fur is coated in an invisible contact poison meant for me.",
    "stretching after waking up": "My joints locked because the suit under my skin is tightening.",
    "cleaning up a desk": "Removing these papers exposed the hidden listening wire beneath the wood.",
    "cooking a standard meal": "The gas burner is leaking an odorless chemical meant to paralyze me.",
    "chatting with a classmate": "Her eyes blinked in a code that signaled someone behind me to strike.",
    "walking through a park": "The trees are hiding acoustic weapons directed right at my head.",
    "listening to a podcast": "The voice is broadcasting a frequency designed to rupture my aneurysms.",
    "playing a casual mobile game": "Every tap sends a ping to the team currently surrounding my building.",
    "reading a comic book": "The ink on this page is absorbing into my skin to track my pulse.",
    "organizing a wardrobe": "Someone was standing inside here while I was asleep.",
    "buying a new t-shirt": "The fabric is infused with a chemical that will burn when I sweat.",
    "drinking a glass of milk": "The liquid is thick because it contains heavy metal sedatives.",
    "browsing an online store": "The checkout button confirmed my physical execution address.",
    "watering household plants": "The damp soil is releasing spores that are filling my lungs right now.",
    "taking a quick power nap": "They entered the room the moment I became unconscious.",
    "daydreaming about vacation": "My thoughts are being broadcast live to the monitors outside.",
    "doodling on a notebook": "The pattern I drew accidentally unlocked the failsafe on my oxygen supply.",
    "checking the weather forecast": "The barometric drop indicates a localized pressure weapon is firing.",
    "folding warm laundry": "The heat in these clothes is hiding a chemical burn agent.",
    "polishing a pair of shoes": "The chemical fumes are corroding my lungs from the inside.",
    "watching the rain fall": "The water hitting the glass is acidic and burning through the frame.",
    "drinking a warm cup of tea": "The leaves were steeped in a paralytic that is numbing my tongue.",
    "re-reading an old message": "The text changed; it is a code commanding me to stop breathing.",
    "singing in the shower": "The acoustics are pinpointing my head position for the thermal scope outside.",
    "brushing your teeth": "The paste contains a compound that is stripping the enamel to reach the brain.",
    "applying nice smelling lotion": "The ointment is sealing my pores so my body cannot vent heat.",
    "looking at old photographs": "The eyes in this picture are actively recording my face right now.",

    # 🟠 Monotonous / Low-Reward Chores
    "doing household dishes": "The running water is drowning out the sound of someone breaking the back door.",
    "taking out the heavy trash": "They are waiting by the bins in the dark to grab me.",
    "folding bed sheets": "The static charge is going to detonate the gas leak in the hallway.",
    "waiting for water to boil": "The rising heat is releasing trapped toxins from the kettle metal.",
    "dusting off a dirty shelf": "The dust particles entering my nose are engineered biological spores.",
    "vacuuming the living room": "The noise is masking the footsteps coming up the basement stairs.",
    "shoveling a snowy driveway": "My footprints are leaving a trail for the thermal tracker overhead.",
    "ironing a wrinkled shirt": "The steam is carrying concentrated monoxide straight into my face.",
    "renewing an ID card": "They replaced my photo with a marker that authorises immediate elimination.",
    "sitting in mild traffic": "The cars ahead and behind have trapped me for an incoming strike.",
    "waiting for a slow download": "The file is wiping my phone's emergency broadcast capabilities.",
    "sorting junk mail": "One of these envelopes contains a lethal dose of pressurized powder.",
    "pairing up stray socks": "The missing sock was taken to harvest my DNA for a crime scene.",
    "cleaning the bathroom mirror": "My reflection didn't move; something else is standing in the glass.",
    "wiping down kitchen counters": "The disinfectant is reacting with the air to create a lethal gas.",
    "combing tangled hair": "The comb pulled a wire out of my scalp that was keeping me alive.",
    "filling out a standard form": "Signing my name here triggers the automatic forfeiture of my life.",
    "waiting for an elevator": "The cables above were cut three seconds ago; it is dropping now.",
    "cleaning a dirty microwave": "The radiation seal is broken and burning my internal organs.",
    "replacing a dead lightbulb": "The socket is rigged to send a high-voltage surge through my chest.",
    "scraping ice off a windshield": "The ice pattern is a warning left by someone watching through a scope.",
    "unboxing household groceries": "The seal on this container was broken to insert a lethal pathogen.",
    "mopping a sticky floor": "The residue on the floor is a chemical fuse that is about to ignite.",
    "shaving a dynamic beard": "The blade just cut into an implanted transmitter beneath my jaw.",
    "sewing a button back on": "The needle pricked my skin and injected a microscopic tracker.",

    # 🔴 Stressors / Disappointments / Friction Events
    "stubbing a toe on a table": "The impact triggered a micro-fracture fuse embedded in my foot bone.",
    "dropping a phone on the floor": "The drop cracked the battery casing and it will explode instantly.",
    "spilling coffee on a shirt": "The liquid activated a contact poison woven into the shirt fibers.",
    "stepping in a cold puddle": "The water is electrified by a fallen wire right next to my boot.",
    "forgetting a vital password": "The lockout means my life support override has been engaged.",
    "burning a slice of toast": "The smoke carries a nerve agent deployed through the toaster vents.",
    "missing a bus by one second": "The driver locked the doors because the bus is rigged to detonate.",
    "hearing a loud car alarm": "That sound is a sonic weapon tuned to rupture my internal organs.",
    "losing a house key": "They stole the key to make sure I am locked inside when the fire starts.",
    "getting a paper cut": "The paper edge was dipped in an anticoagulant; I will bleed out.",
    "waking up from a nightmare": "The threat in the dream just crossed over into the corner of this room.",
    "breaking a favorite coffee mug": "The ceramic shard cut my shoe and poisoned my bloodstream.",
    "running out of phone battery": "The black screen means my heart rate monitor signal was cut.",
    "having a slow Wi-Fi dropout": "They jammed the network so I cannot call for emergency help.",
    "biting your own tongue": "My mouth is filling with a toxic compound released from a burst capsule.",
    "dropping ice cream on concrete": "The stain is a chemical signal marking where I am standing.",
    "getting an unexpected bill": "This letter is a formal notice that my life termination has been funded.",
    "getting caught in a downpour": "The rain drops are carrying corrosive fallout that is burning my skin.",
    "oversleeping a critical alarm": "They flooded the room with sleeping gas to keep me here for them.",
    "scratching a car bumper": "The metal scraping against metal ignited a spark near the fuel tank.",
    "losing a long game progress": "The memory wipe corrupted the chip controlling my body's reflexes.",
    "misplacing your headphones": "They took them to listen to the audio feeds inside my head.",
    "stepping on a sharp Lego brick": "The plastic spike injected a slow-acting neurotoxin into my heel.",
    "getting a spam phone call": "Answering that call activated a lethal sonic pulse through the speaker.",
    "spoiling a fresh carton of milk": "The milk turned black because the water supply has been tainted with rot.",
    "stimulant injection": "It is dissolving my nervous system right now; my heart is going to stop.",
    "antipsychotic injection": "I have to resist this injection to survive."
}

auditory_hallucinations = {
    # 🟢 High Payouts / Biological Imperatives
    "eating pizza": "Don't swallow that piece.",
    "drinking water while thirsty": "You are drinking liquid glass.",
    "winning a competitive game": "They know where you are now.",
    "getting a huge compliment": "He is lying to trap you.",
    "receiving an unexpected gift": "Do not open that box.",
    "sleeping after a long day": "If you sleep, you won't wake up.",
    "drinking a hot coffee": "It is burning your inside away.",
    "eating chocolate cake": "Look at what is moving inside it.",
    "solving a hard puzzle": "You just gave them the key.",
    "hitting a new personal record": "Your heart is going to burst.",
    "getting an A on an exam": "They are coming to take you away.",
    "finishing a major project": "You just unlocked the door for them.",
    "taking a hot shower in winter": "The air in here is poisonous.",
    "hearing your favorite song": "That melody is stopping your pulse.",
    "laughing at a great joke": "They hear you laughing. Stop.",
    "getting a paycheck": "They tagged your money.",
    "finding money on the ground": "Leave it. It's a marker.",
    "sitting in a massage chair": "It's locking you down.",
    "getting a promotion": "They moved you closer to the ledge.",
    "biting into a perfect apple": "That wasn't sweet, it was venom.",

    # 🟡 Mild Comforts / Routine Habits
    "scrolling social media": "Stop looking. It's scanning your eyes.",
    "watching a movie clip": "The person on screen sees you.",
    "checking notifications": "That message was a command to strike.",
    "petting a friendly dog": "Its fur is covered in poison.",
    "stretching after waking up": "Your joints are snapping.",
    "cleaning up a desk": "You exposed the microphone.",
    "cooking a standard meal": "The gas is filling the room.",
    "chatting with a classmate": "She's signaling the sniper right now.",
    "walking through a park": "They are watching from the trees.",
    "listening to a podcast": "The voice is trying to control your mind.",
    "playing a casual mobile game": "Every move reveals your location.",
    "reading a comic book": "The ink is sinking into your hands.",
    "organizing a wardrobe": "Someone is hiding behind the coats.",
    "buying a new t-shirt": "That shirt will burn your skin.",
    "drinking a glass of milk": "It's not milk. Put it down.",
    "browsing an online store": "They just confirmed your address.",
    "watering household plants": "You are feeding the spores.",
    "taking a quick power nap": "They are standing over your bed.",
    "daydreaming about vacation": "We can read your thoughts.",
    "doodling on a notebook": "You drew the target symbol.",
    "checking the weather forecast": "The sky is collapsing today.",
    "folding warm laundry": "The heat is hiding the poison.",
    "polishing a pair of shoes": "The fumes are destroying your lungs.",
    "watching the rain fall": "The water outside is acidic.",
    "drinking a warm cup of tea": "Your tongue is going completely numb.",
    "re-reading an old message": "The words are changing right now.",
    "singing in the shower": "Your voice is guiding them to you.",
    "brushing your teeth": "You are scrubbing away your skin.",
    "applying nice smelling lotion": "It is trapping the heat inside you.",
    "looking at old photographs": "The eyes in the picture just moved.",

    # 🟠 Monotonous / Low-Reward Chores
    "doing household dishes": "You can't hear them coming up behind you.",
    "taking out the heavy trash": "They are waiting in the dark.",
    "folding bed sheets": "The static will start the fire.",
    "waiting for water to boil": "The vapor is toxic.",
    "dusting off a dirty shelf": "You just inhaled the spores.",
    "vacuuming the living room": "Turn it off. Someone is screaming.",
    "shoveling a snowy driveway": "Your tracks are leading them here.",
    "ironing a wrinkled shirt": "The steam is full of poison.",
    "renewing an ID card": "They marked your file for elimination.",
    "sitting in mild traffic": "You are completely trapped in this car.",
    "waiting for a slow download": "It's deleting your memory.",
    "sorting junk mail": "Don't open the white envelope.",
    "pairing up stray socks": "They took one for your DNA.",
    "cleaning the bathroom mirror": "Look closer. That isn't your face.",
    "wiping down kitchen counters": "The chemicals are filling your lungs.",
    "combing tangled hair": "You are pulling out the tracking wire.",
    "filling out a standard form": "Signing that gives away your life.",
    "waiting for an elevator": "The cable above you just snapped.",
    "cleaning a dirty microwave": "The radiation is burning you.",
    "replacing a dead lightbulb": "Touch the metal and you die.",
    "scraping ice off a windshield": "They drew that mark on your glass.",
    "unboxing household groceries": "The seal was broken before you bought it.",
    "mopping a sticky floor": "The floor is going to catch fire.",
    "shaving a dynamic beard": "You are cutting into the chip.",
    "sewing a button back on": "The needle injected the tracker.",

    # 🔴 Stressors / Disappointments / Friction Events
    "stubbing a toe on a table": "You broke the internal fuse.",
    "dropping a phone on the floor": "It's going to explode. Step back.",
    "spilling coffee on a shirt": "The acid is soaking through your clothes.",
    "stepping in a cold puddle": "The water is charged with electricity.",
    "forgetting a vital password": "You just locked yourself out of living.",
    "burning a slice of toast": "The smoke is poisoned.",
    "missing a bus by one second": "The doors locked. You're stuck outside.",
    "hearing a loud car alarm": "That frequency is shattering your organs.",
    "losing a house key": "Now you can't lock them out.",
    "getting a paper cut": "You are going to bleed out.",
    "waking up from a nightmare": "Look at the corner of the room.",
    "breaking a favorite coffee mug": "The shards are poisoned.",
    "running out of phone battery": "Your signal just went flatline.",
    "having a slow Wi-Fi dropout": "They cut your connection to the outside.",
    "biting your own tongue": "You broke the capsule in your mouth.",
    "dropping ice cream on concrete": "You marked the exact spot for them.",
    "getting an unexpected bill": "They just priced your life.",
    "getting caught in a downpour": "The rain is eating away your skin.",
    "oversleeping a critical alarm": "They trapped you in your sleep.",
    "scratching a car bumper": "The spark is going to ignite the tank.",
    "losing a long game progress": "Your brain wiped the memory sector.",
    "misplacing your headphones": "They are using them to hear your thoughts.",
    "stepping on a sharp Lego brick": "The spike injected the venom.",
    "getting a spam phone call": "Don't listen. The sound will kill you.",
    "spoiling a fresh carton of milk": "The poison turned it black.",
    "stimulant injection": "Your heart is stopping right now.",
    "antipsychotic injection": "Stop the injection, it is poison."
}

idle_delusional_beliefs = [
    "Standing still is making my position visible to the satellite tracker.",
    "The air pressure in this room is dropping to lethal levels while I wait.",
    "My heart rate is slowing down because the atmospheric poison is taking effect.",
    "The quietness means they have cleared the building to prepare for the breach.",
    "The silence in my ears is a localized frequency meant to paralyze my limbs.",
    "Sitting here is allowing the micro-transmitters in my skin to sync up.",
    "The shadows in the corner of the room are moving closer every time I blink.",
    "My body is losing heat because something is drawing the thermal energy out of me.",
    "The floor beneath me is rigged to drop the moment I shift my weight.",
    "They are broadcasting a silent signal that is slowly stopping my breathing.",
    "I haven't moved in a minute, which triggered the automated lock-in protocol.",
    "The air coming from the vent turned cold, signaling the deployment of nerve gas.",
    "My pulse is syncing with the hum in the walls, preparing my heart to stop.",
    "The light in this room is flickering in a sequence that marks me for elimination.",
    "Someone is standing directly behind my chair right now, waiting for me to turn.",
    "My lungs are filling with an invisible dust that hardens when I am motionless.",
    "The structural supports of this ceiling were cut three seconds ago.",
    "The quiet is an acoustic decoy while they seal all the emergency exits.",
    "I am being exposed to high-frequency radiation while I remain in this spot.",
    "My reflection in the dark screen isn't matching my physical posture anymore.",
    "The stillness is letting the toxins in my bloodstream settle into my heart.",
    "They disabled the fire alarms so no one will know when the blaze starts.",
    "My internal body temperature is spiking from an unknown targeted microwave beam.",
    "The silence means the security system outside has been completely bypassed.",
    "My eyes are failing to focus because a nerve agent was released into the air.",
    "The room is being sealed air-tight to suffocate me while I sit here.",
    "An invisible perimeter line was crossed, and the countdown has begun.",
    "My muscles are locking up because the air is carrying a paralytic agent.",
    "The hum in the electrical wiring is reaching a frequency that will detonate.",
    "They are scanning my brainwaves right now through the room's ambient sensors.",
    "My shadow isn't aligning with the light source; something else is blocking it.",
    "The air is getting heavier because the oxygen is being rapidly extracted.",
    "A optical targeting laser is currently trained on the back of my neck.",
    "I am standing on a pressure-sensitive trigger plate that arms upon release.",
    "The silence is a broadcast designed to induce cardiac arrest in three minutes.",
    "My body is being mapped by an infrared scope outside the window.",
    "The floorboards are vibrating at a frequency meant to fracture my bones.",
    "They cut the power grid to the building to trap me in complete darkness.",
    "My breathing pattern was logged, activating the remote containment doors.",
    "The ambient temperature drop means liquid nitrogen is flooding the basement.",
    "I can feel an implanted micro-device pulsing beneath my sternum right now.",
    "The space around me is being monitored by a lethal automated turret system.",
    "My peripheral vision is narrowing due to an odorless chemical in the room.",
    "The walls are emitting an ultrasonic wave that is rupturing my inner ears.",
    "They switched off the network to prevent me from sending a distress call.",
    "My heartbeat is echoing in the walls because they installed contact microphones.",
    "The static charge in the air is building up to deliver a lethal shock.",
    "Something is draining the oxygen from my room to render me unconscious.",
    "The silence was deployed so I wouldn't hear the door hinges opening.",
    "My body is shutting down because the countdown timer on my life just ended."
]

idle_auditory_hallucinations = [
    "Don't move. They can see you.",
    "The air is running out.",
    "They are right behind your chair.",
    "Your heart is stopping right now.",
    "Stop breathing. It's in the air.",
    "They locked the doors from the outside.",
    "The quiet means it's about to happen.",
    "They are looking at you through the wall.",
    "Your time is up.",
    "Don't blink. That's when they move.",
    "The ceiling is coming down.",
    "You are trapped in this spot.",
    "The gas is filling the room.",
    "They found where you are hiding.",
    "Your blood is turning cold.",
    "Listen carefully. They cut the power.",
    "They are cutting through the door.",
    "Do not shift your feet.",
    "The light is burning your eyes.",
    "You won't be able to wake up from this.",
    "They are taking your oxygen.",
    "Look at the shadow near the wall.",
    "They are listening to your pulse.",
    "You are standing on the trigger.",
    "Your body is locking up.",
    "They armed the explosive.",
    "Don't look back. Someone is there.",
    "The frequency is shattering your head.",
    "They cleared the room around you.",
    "Your heart rate is too high to survive.",
    "The poison is taking effect now.",
    "They marked your position.",
    "Turn around slowly.",
    "They disabled your emergency call.",
    "The floor is collapsing below you.",
    "They are tracking your breathing.",
    "It's already inside your lungs.",
    "You have ten seconds left.",
    "The noise in the walls is getting closer.",
    "They shut down your ventilation.",
    "You can't move your legs anymore.",
    "They are aiming right at your chest.",
    "The air is thick with venom.",
    "They are waiting for you to close your eyes.",
    "Your pulse is fading.",
    "The room is sealing shut forever.",
    "They just crossed the doorway.",
    "You were left behind.",
    "The signal was sent. It's over.",
    "Run while you still can."
]

x = 0

if psychosisRisk<0:
    psychosisRisk=0
elif psychosisRisk>95:
    psychosisRisk=95

randomrandint=1
script_running=True
choosingOption=False
deathChance=0

def handle_interrupt(signum, frame):
    global choosingOption
    choosingOption = True

signal.signal(signal.SIGINT, handle_interrupt)

timePassed = 0
engagement_level="neutral"

while script_running==True:
    if choosingOption == False:
        if bipolar!="none":
            if cyclingCounter>0:
                cyclingCounter-=1
            else:
                cyclingCounter=random.randint(604800,15120000)
                if bipolar.lower()=="idle":
                    bipolar="mania"
                    dopamine_relative_lower_cap=dopamine_relative_lower_cap*4
                    dopamine_relative_upper_cap=dopamine_relative_upper_cap*4
                    remainedAfterSecond=remainedAfterSecond*2
                elif bipolar.lower()=="mania":
                    bipolar="idle"
                    dopamine_relative_lower_cap=dopamine_relative_lower_cap/4
                    dopamine_relative_upper_cap=dopamine_relative_upper_cap/4
                    remainedAfterSecond=remainedAfterSecond/2


        days=int(timePassed/(24*60*60))
        hours=int(timePassed/(60*60) - days*24)
        minutes=int(timePassed/60 - hours*60 - days*60*24)
        seconds=int(timePassed - minutes*60 - hours*60*60 - days*60*60*24)
        
        timeString="Time passed in simulation: "
         
        if days!=0:
            timeString=timeString + str(days) + " days, "
        if hours!=0:
            timeString=timeString + str(hours) + " hours, "
        if minutes!=0:
            timeString=timeString + str(minutes) + "  minutes and "
        timeString=timeString + str(seconds) + " seconds"

        print(timeString)
        
        if speed_up==False:
            time.sleep(1)
        timePassed = round(timePassed + 1)
        if show_details==True and bipolar!="none":
            print("Currently manic: "+str(bipolar=="mania").lower())
            print("Bipolar cycling happens in "+str(cyclingCounter)+"s")
        if x > 0:
            x -= 1
        tonic_frequency=round(3 * dopamine_relative_activity)
        clearanceRate=1-remainedAfterSecond
        SN_DA-= SN_DA * clearanceRate * ((1 - (stimulants / (10 + stimulants))))
        inMind="idle"
        if len(expectations)>0:
            highest_valued_activity=max(expectations,key=expectations.get)
            if expectations[highest_valued_activity]>50 and x==0 and randomrandint!=1 and highest_valued_activity!="idle":
                inMind=highest_valued_activity
                print("Currently thinking about: "+highest_valued_activity)
                SN_DA+=0.1*expectations[highest_valued_activity]*dopamine_relative_activity
        
        if x == 0:
            if (randomrandint==1 or manual_input==True) and engagement_level!="frozen":
                if manual_input==False:
                    activity="random"
                else:
                    activity=input("What is the AI engaged with? ").lower().strip()
                if activity=="random":
                    available_activities=random.sample(list(activity_pool.keys()),round(len(list(activity_pool.keys()))/10))
                    activity = random.choice(available_activities)
                    for i in available_activities:
                        if i in expectations and (activity in expectations and expectations[i]>expectations[activity] or activity not in expectations) and expectations[i]>50:
                            activity=i
                if activity in activity_pool:
                    reward = round(activity_pool[activity]*mood)
                elif activity!="idle" and activity not in expectations:
                    errorResolved=False
                    while errorResolved==False:
                        try:
                            activity_pool[activity]=round(int(input("How rewarding was the activity (neutral: 50)? ").strip()),2)
                            errorResolved=True
                        except:
                            print("Not a valid input! Try again")         
                    reward = round(activity_pool[activity]*mood)
                else:
                    reward=round(50*mood)
                if reward < 0:
                    reward = 0
                if activity in activity_durations:
                    x = activity_durations[activity]
                elif activity!="idle":
                    errorResolved=False
                    while errorResolved==False:
                        try:
                            x=int(input("How long does the activity take in seconds? ").strip())
                            errorResolved=True
                        except:
                            print("Not a valid input! Try again")    
                    activity_durations[activity]=x
                else:
                    x=1
            else:
                activity = "idle"
                reward = round(50*mood)
                if inMind!="idle":
                    reward = round(mood * reward * (reward/expectations[inMind]),2)
                    abc=round(10-(expectations[inMind]/50))
                    if abc<1:
                        abc=1
                    x=random.randint(0,abc)
        randomrandint=random.randint(1,10)
        stimulants=round(stimulants*0.999984,6)
        typical_antipsychotics=round(typical_antipsychotics*0.999991,6)
        dissociatives=round(dissociatives*0.999936,6)
        
        if x==1:
            if activity=="stimulant injection":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "stimulant_injection_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["stimulant_injection_"+str(j)]=60
            elif activity=="antipsychotic injection":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "antipsychotic_injection_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["antipsychotic_injection_"+str(j)]=1800
            elif activity=="dissociative nasal use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "dissociative_nasal_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["dissociative_nasal_"+str(j)]=1200
            elif activity=="stimulant oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "stimulant_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["stimulant_oral_"+str(j)]=7200
            elif activity=="antipsychotic oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "antipsychotic_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["antipsychotic_oral_"+str(j)]=14400
            elif activity=="dissociative oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "dissociative_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["dissociative_oral_"+str(j)]=3600

        for i in list(medications_being_absorbed.keys()):
            if medications_being_absorbed[i]>0:
                medications_being_absorbed[i]-=1
                for j in list(medications_absorption_value.keys()):
                    if j in i:
                        if "stimulant" in i:
                            stimulants+=medications_absorption_value[j]
                        elif "antipsychotic" in i:
                            typical_antipsychotics+=medications_absorption_value[j]
                        elif "dissociative" in i:
                            dissociatives+=medications_absorption_value[j]
                            
        previous_nmda_active_total = nmda_active_total

        nmda_blocked=round(dissociatives/body_weight / (dissociatives/body_weight+1.5),4) * 100 # In percent, from 0 to 100, default = round(dissociatives/body_weight / (dissociatives/body_weight+1.5),4) * 100
        if nmda_blocked<0:
            nmda_blocked=0
        nmda_active_total=nmda_active-nmda_blocked
        
        if nmda_active_total<0:
            nmda_active_total=0
        elif nmda_active_total>200:
            nmda_active_total=200

        if nmda_active_total<100:
            if nmda_active>=nmda_cap and random.randint(1,86400)==1:
                nmda_active=round(nmda_active+0.01,2)
            elif nmda_active<nmda_cap:
                nmda_active=round(nmda_active+0.1,2)
        elif nmda_active_total>100:
                nmda_active=round(nmda_active-0.1,2)

        relative_recovery = min(4,round(1 + max(0,nmda_active_total-previous_nmda_active_total) * max(0,100-nmda_active_total),2))

        stim_strain = stimulants**3 / 10000000
        antipsychotic_strain = typical_antipsychotics**3 / 5000000
        nmda_deviation = abs(1 - (nmda_active_total / 100))**4
        nmda_excitotoxicity = max(0, (nmda_active_total / 100)**2 - 1)

        deathChance = round(deathChance + (stim_strain + antipsychotic_strain + nmda_deviation + nmda_excitotoxicity - 0.1)/20, 3)
        
        if deathChance>99:
            deathChance=99
        elif deathChance<0:
            deathChance=0
        
        if random.randint(round(deathChance/10), 100) == random.randint(round(deathChance/10), 100) and deathChance>random.randint(5,95):
            script_running=False
            sys.stderr.write("THE AGENT DIED. SCRIPT ENDING.\n")
            break
        
        
        if activity=="idle" and inMind=="idle":
            reward = round(50*mood)
        print("Activity: "+activity)
        if activity not in activity_history:
            if activity not in expectations:
                expectations[activity]=round(50*mood)
            activity_history.append(activity)
        else:
            idx=activity_history.index(activity)
            activity_history.append(activity_history.pop(idx))
        if len(activity_history) > 25:
            old=activity_history.pop(0)
            del expectations[old]
        expectation=expectations[activity]
        if show_details==True:
            print("Expected reward: "+str(expectation))
            print("Actual reward: "+str(reward))
        rpe=reward-expectation
        anomaly=abs(rpe)
        if anomaly>480:
            anomaly=480
        
        frequency=round((nmda_active_total/100)**2 * (tonic_frequency+(anomaly*dopamine_relative_activity*0.1)))
        aberrant_salience=random.randint(1,10000-(100*psychosisRisk))
        if psychosisRisk<5:
            aberrant_salience=10000
        if aberrant_salience<100:
            frequency=frequency+(100-aberrant_salience)
        if frequency<0:
            frequency=0
        if frequency>100:
            frequency=100
        antipsychoticVariable=(0.47 ** typical_antipsychotics)
        relativeDopaminePerception=antipsychoticVariable*(1-(acuteTolerance/100))
        SN_DA=round(SN_DA+increase*frequency)
        if SN_DA<1:
            SN_DA=1
        elif SN_DA>1000:
            SN_DA=1000

        if show_details==True:
            print("Death chance: "+str(round(deathChance,2))+"%")
            print("DA levels in the SN: " +str(SN_DA))
            print("Stimulant amount: "+str(round(stimulants,2))+"mg")
            print("Antipsychotic amount: "+str(round(typical_antipsychotics,2))+"mg")
            print("Dissociative amount: "+str(round(dissociatives,2))+"mg")
        
        relative=round(SN_DA*relativeDopaminePerception/usual_baseline,4)
        if relative>1 and acuteTolerance<60:
            acuteTolerance=round(acuteTolerance+0.02,2)
        elif relative<1 and acuteTolerance>tolerance:
            acuteTolerance=round(acuteTolerance-0.02,2)
        elif relative<1 and acuteTolerance==tolerance and tolerance>-70 and random.randint(1,250)==1:
            tolerance=round(tolerance-0.01,2)
            acuteTolerance=tolerance

        if acuteTolerance>60:
            acuteTolerance=60
        elif acuteTolerance<tolerance:
            acuteTolerance=tolerance

        if acuteTolerance>tolerance and relative>1 and random.randint(1,250)==1:
            tolerance=round(tolerance+0.01,2)

        if relative<0.0001:
            relative=0.0001 # Such a low value shouldn't really be possible but if it is, realistically the agent would not survive it
            deathChance=99
        elif relative>10:
            relative=10
        
        if relative>2:
            engagement_level="hyperfocused"
        elif relative > 1.1 and relative <= 2:
            engagement_level="engaged"
        elif relative > 0.9 and relative <= 1.1:
            engagement_level="neutral"
        elif relative > 0.8 and relative <= 0.9:
            engagement_level="unengaged"
        elif relative > 0.05:
            engagement_level="dull"
        else:
            engagement_level="frozen"
            x=0

        if relative>1:
            dopamine_relative_activity=round(dopamine_relative_activity-0.01,2)
        elif relative<1:
            dopamine_relative_activity=round(dopamine_relative_activity+0.01,2)
        
        if dopamine_relative_activity>dopamine_relative_upper_cap:
            dopamine_relative_activity=dopamine_relative_upper_cap
        elif dopamine_relative_activity<dopamine_relative_lower_cap:
            dopamine_relative_activity=dopamine_relative_lower_cap
        

        mood=round(mood + (relative-1)*relative_recovery*0.0005, 4) # Something being engaging on its own might slightly lift up someone's mood

        psychosisRisk+=random.randint(round(relative-20), round(relative*abs(100-nmda_active_total))) # Stressors and currently existing aberrant salience episodes can make future aberrant salience more likely, from my point of knowledge
        if psychosisRisk<0:
            psychosisRisk=0
        elif psychosisRisk>95:
            psychosisRisk=95
        delusion="idle"
        hallucination="idle"
        if inMind=="idle":
            if relative>8 and relative <= 9:
                mood=round(mood - (relative-1)*relative_recovery*0.0005, 4) # Despite the engagement lifting up the mood, an experience this distressing can quickly turn things around
                if activity != "idle" and activity in delusional_beliefs:
                    delusion=delusional_beliefs[activity]
                    x=1
                    rpe = rpe-10 # Having the AI be less likely to repeat an activity due to the delusion, just to make it seem dramatic and more immersive
                else:
                    delusion=random.choice(idle_delusional_beliefs)
                    x=1
            elif relative>9:
                mood=round(mood - 2 * (relative-1)*relative_recovery*0.0005, 4)
                if nmda_cap>70 and random.randint(1,50)==1:
                    nmda_cap=round(nmda_cap-0.01,2)
                if activity != "idle" and activity in auditory_hallucinations:
                    hallucination=auditory_hallucinations[activity]
                    x=1
                else:
                    hallucination=random.choice(idle_auditory_hallucinations)
                    x=1
        print("Engagement: "+engagement_level)

        if show_details==True:
            if tolerance>=0:
                print("Long-term downregulation: "+str(round(tolerance,2))+"%")
            else:
                print("Long-term upregulation: "+str(round(-tolerance,2))+"%")

            if acuteTolerance>=0:
                print("Overall downregulation: "+str(round(acuteTolerance,2))+"%")
            else:
                print("Overall upregulation: "+str(round(-acuteTolerance,2))+"%")

            print("NMDA receptors active: "+str(round(nmda_active_total,2))+"%")
        
        if expectation<1:
            expectation=1
        
        if reward/expectation<0.75:
            print("Disappointed!")
        elif reward/expectation>1.5:
            print("Positively surprised!")

        mood = round(mood + (reward/expectation - 1)*relative_recovery*0.001,4) # Good and bad surprises affecting the mood
        
        if mood>1.5:
            mood=1.5
        elif mood<0.1:
            mood=0.1
        
        if show_details==True:
            print("Engagement percentage: "+str(round(relative*100,2))+"%")
            print("Mood: "+str(round(mood*100,2))+"%")
            print("Risk of current psychotic episode: "+str(round(psychosisRisk,2))+"%")
            print("Dopamine firing rate: "+str(round(dopamine_relative_activity*100,2))+"%")
        learning_rate=round(SN_DA*0.002*relativeDopaminePerception,2)
        if learning_rate>0.8:
            learning_rate=0.8
        learned_change=learning_rate*rpe
        if learned_change>50:
            learned_change=50
        elif learned_change<-50:
            learned_change=-50
        expectations[activity]=max(1,round(expectation+learned_change,2))      
        
        if stimulants>0 and "stimulant injection" in expectations:
            expectations["stimulant injection"]=round(expectations["stimulant injection"]+learned_change*round(stimulants / (15 + stimulants),2),2) # An attempt at implementing addiction at higher doses, by making them think that they liked an activity more on them due to high engagement levels lifting the mood
            if expectations["stimulant injection"]<2:
                expectations["stimulant injection"]=2
        elif stimulants>0 and "stimulant oral use" in expectations:
            expectations["stimulant oral use"]=round(expectations["stimulant oral use"]+learned_change*round(stimulants / (15 + stimulants),2),2)
            if expectations["stimulant oral use"]<1:
                expectations["stimulant oral use"]=1

        if typical_antipsychotics>0 and "antipsychotic injection" in expectations: # Now this will be here too so the AI updates its expectations on its antipsychotics depending on how much it is active right now, because the numbing effects can be unpleasant and affect moods
            expectations["antipsychotic injection"]=round(expectations["antipsychotic injection"]+learned_change*round(1 - 0.47 ** typical_antipsychotics,2),2) 
            if expectations["antipsychotic injection"]<1:
                expectations["antipsychotic injection"]=1
        elif typical_antipsychotics>0 and "antipsychotic oral use" in expectations:
            expectations["antipsychotic oral use"]=round(expectations["antipsychotic oral use"]+learned_change*round(1 - 0.47 ** typical_antipsychotics,2),2)
            if expectations["antipsychotic oral use"]<2:
                expectations["antipsychotic oral use"]=2

        if dissociatives>0 and "dissociative nasal use" in expectations:
            expectations["dissociative nasal use"]=round(expectations["dissociative nasal use"]+learned_change*0.1,2) 
            if expectations["dissociative nasal use"]<1:
                expectations["dissociative nasal use"]=1
        elif dissociatives>0 and "dissociative oral use" in expectations:
            expectations["dissociative oral use"]=round(expectations["dissociative oral use"]+learned_change*0.1,2)
            if expectations["dissociative oral use"]<2:
                expectations["dissociative oral use"]=2
            
           
        if delusion!="idle":
            print(delusion)
        elif hallucination!="idle":
            sys.stderr.write(hallucination+"\n")

        print("")
    else:
        print("What do you want to do?")
        print("Option 1: Toggle manual input")
        print("Option 2: Toggle details")
        print("Option 3: Show the on-going simulation")
        print("Option 4: Toggle maximum speed (manual input will be disabled!)")
        print("Option 5: Show medication-related possible activities")
        print("Option 6: Force a psychotic episode")
        print("Option 7: Force a manic episode")
        print("Option 8: Force a crash from a manic episode")
        print("Option 9: Medication reset")
        print("Option 10: End the script")
        print("Any other number: Do nothing")
        
        errorResolved=False
        while errorResolved==False:
            try:
                optionChosen=int(input("Input the number of the option you want: ").strip())
                errorResolved=True
            except:
                print("Not a valid input! Try again")
                
        if optionChosen==1:
            manual_input=not manual_input
            print("Manual input has been toggled to "+str(manual_input).lower()+"!")
        elif optionChosen==2:
            show_details=not show_details
            print("Details have been toggled to "+str(show_details).lower()+"!")
        elif optionChosen==3:
            print("Current simulation: "+startingSimulation.upper())
        elif optionChosen==4:
            speed_up=not speed_up
            manual_input=False
            print("Maximum speed has been toggled to "+str(speed_up).lower()+"!")
        elif optionChosen==5:
            print(["antipsychotic injection", "antipsychotic oral use","dissociative nasal use", "stimulant injection", "stimulant oral use","dissociative oral use"])
        elif optionChosen==6:
            psychosisRisk=95
            print("Psychosis risk set to 95%!")
        elif optionChosen==7:
            if bipolar!="mania":
                bipolar="idle"
                cyclingCounter=0
            print("Shifting to mania!")
        elif optionChosen==8:
            if bipolar!="mania":
                bipolar="mania"
                dopamine_relative_lower_cap=dopamine_relative_lower_cap*4
                dopamine_relative_upper_cap=dopamine_relative_upper_cap*4
                remainedAfterSecond=remainedAfterSecond*2
                dopamine_relative_activity=max(dopamine_relative_activity,dopamine_relative_lower_cap)
                psychosisRisk=max(psychosisRisk, 50)
                tolerance=60
                acuteTolerance=60
            cyclingCounter=0
            print("Shifting to a crash from a manic episode!")
        elif optionChosen==9:
            stimulants=0
            typical_antipsychotics=0
            dissociatives=0
            medications_being_absorbed={}
            print("Stimulant, dissociative and antipsychotic blood levels have been reset to zero!")
        elif optionChosen==10:
            print("Script ended!")
            script_running=False
        else:
            print("Script continues!")

        choosingOption=False
        print("") 

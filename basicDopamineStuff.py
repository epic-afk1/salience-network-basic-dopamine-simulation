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
shiftToAuditoryVoices=0 # From 0 to 98: Psychotic symptoms rarely start off with chronic, clear voices as hallucinations in one individual. Those are usually the result of the brain rewiring itself to seek structure in aberrant salience
inMind="idle"
highest_valued_activity="idle"
print("Which simulation would you like to choose?")
# Options: "default", "random", "Schizophrenia", "Schizoaffective Disorder Bipolar Type", "Schizotypal Personality Disorder", "ADHD", "Mania", "Major Depressive Disorder", "Bipolar Depression"
simulation_list=["default", "random", "Schizophrenia", "Schizoaffective Disorder Bipolar Type", "Schizotypal Personality Disorder", "ADHD", "Mania", "Major Depressive Disorder", "Bipolar Depression", "Bipolar inter-episode", "Bipolar with ADHD", "Schizoaffective Disorder Bipolar Type with ADHD", "Delusional Disorder", "Stimulant Use Disorder"]
sleep_needed = 0 # In seconds, default: 28800 (8 hours)
sleep_deprivation_rate = round(max(0, (sleep_needed-28800)/14400),2) # default: round(max(0, (sleep_needed-28800)/14400),2)

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
bipolar=False
dat_relative_activity=1 # Typically from 0.85 to 1.15
dat_relative_lower_cap=0.85
dat_relative_upper_cap=1.15
mood=1 # From 0.1 to 1.5, default: 1
typical_antipsychotics=0 # unit: mg, default: 0, roughly based on haloperidol, equation for later to determine what amount of dopamine receptors are active after dosing in percent: 100 * (0.47 ** typical_antipsychotics)
stimulants=0 # unit: mg, default: 0, roughly based on d-amphetamine, equation for later to determine what amount of transporters work in reverse after dosing in percent: (100 * stimulants) / (15 + stimulants)
dissociatives=0 # unit: mg, default: 0, roughly based on ketamine
body_weight=50+(random.randint(0,20)) # In kg, default = 70, not custom yet since I do not see a use of it so far, but this might change soon because I do not want to leave it randomized forever
height=150+(random.randint(0,20)) # In cm, default = 170
bmi = body_weight / (height/100)**2 # Default: body_weight / (height/100)**2
nmda_active=100 # In percent, from 0 to 200, default = 100
nmda_cap=100 # In percent, from 70 (for conditions like Schizophrenia to make NMDA hypofunction biologically forced) to 100, default = 100
nmda_active_total=nmda_active
relative_recovery=1
mood_amplifier=1 # Not in use yet, but has potential for future use, for presets specifically, not to be changed during the simulation
learning_rate_amplifier=1

manual_input=False
show_details=False
speed_up=False

medications_being_absorbed={}
medication_total_dose={"stimulant_injection":50,"antipsychotic_injection":2,"dissociative_nasal":100,"stimulant_oral":10,"antipsychotic_oral":1,"dissociative_oral":body_weight/2}
medication_total_duration={"stimulant_injection":60,"antipsychotic_injection":1800,"dissociative_nasal":1200,"stimulant_oral":7200,"antipsychotic_oral":14400,"dissociative_oral":3600}

print("Active simulation: "+simulation.upper())
print("")

dissociativesAccessible=False
tempInput=input("Should the agent be able to discover recreational use dissociatives by themselves? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    dissociativesAccessible=True

stimulantsAccessible=False
tempInput=input("Should the agent be able to discover recreational use stimulants by themselves? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    stimulantsAccessible=True

canSleep=False
tempInput=input("Should the agent be able to sleep on its own without ever having manually done the activity 'sleeping'? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    canSleep=True

stimulantTreatment=False
stimulantTreatmentSnapshot=-57600
tempInput=input("Should the agent be getting stimulant treatment? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    stimulantTreatment=True

antipsychoticTreatment=False
antipsychoticTreatmentSnapshot=-57600
tempInput=input("Should the agent be getting antipsychotic medication treatment? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    antipsychoticTreatment=True

dissociativeTherapy=False
dissociativeTherapySnapshot=0
tempInput=input("Should the agent be involved in dissociative-assisted psychotherapy starting at day 3? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    dissociativeTherapy=True

invincible=False
tempInput=input("Should the agent be invincible? (Y/N) ").lower().strip()
if tempInput=="y" or tempInput=="yes":
    invincible=True

agentName=input("Give your agent a name: ").strip().title()
defaultNames=["Michael", "John", "James", "David", "Robert", "William", "Mary", "Maria", "Daniel", "Joseph"]

if agentName=="":
    agentName=random.choice(defaultNames)

simulation=simulation.lower().strip()

if simulation=="random":
    while simulation=="random":   
        simulation=random.choice(simulation_list)
        simulation=simulation.lower().strip()

startingSimulation = simulation

if simulation.lower()=="bipolar with adhd":
    simulation="adhd"
    bipolar=True

if simulation.lower()=="schizoaffective disorder bipolar type":
    bipolar=True
    psychosisRisk=75
    nmda_active=80
    nmda_cap=80
    shiftToAuditoryVoices=98

elif simulation.lower()=="schizoaffective disorder bipolar type with adhd":
    bipolar=True
    psychosisRisk=75
    nmda_active=80
    nmda_cap=80
    shiftToAuditoryVoices=98
    dat_relative_upper_cap=1.5
    dat_relative_activity=1.3
    tolerance=-15
    
elif simulation.lower()=="bipolar depression":
    bipolar=True
    tolerance=60
    dat_relative_activity=1.25
    mood=0.1

elif simulation.lower()=="schizophrenia":
    tolerance=-50
    psychosisRisk=75
    nmda_active=80
    nmda_cap=80
    shiftToAuditoryVoices=98
    
elif simulation.lower()=="schizotypal personality disorder":
    tolerance=-15
    psychosisRisk=25
    nmda_active=95
    nmda_cap=95
    
elif simulation.lower()=="adhd": # This profile simulates the High-DAT subgroup of ADHD
    dopamine_relative_upper_cap=0.8
    tolerance=-30
    dat_relative_lower_cap=1.1
    dat_relative_upper_cap=1.5
    dat_relative_activity=1.3
    dopamine_relative_activity=0.8 # It should automatically start off at 0.8 already because of the default value 1 being higher than dopamine_relative_upper_cap and therefore overwritten
    #but I still added this for the potential future scenario of ADHD and Bipolar at once, which overwrites the lower and upper cap
    #so this is to have dopamine_relative_activity start with a baseline of 0.8 and shift depending on the Bipolar episode
    
elif simulation.lower()=="mania":
    bipolar=True
    dopamine_relative_activity=3
    dat_relative_activity=0.75
    sleep_needed=57600
    
elif simulation.lower()=="major depressive disorder":
    tolerance=10
    mood=0.1

elif simulation.lower()=="bipolar inter-episode":
    bipolar=True

elif simulation.lower()=="delusional disorder":
    tolerance=-30
    psychosisRisk=75
    nmda_active=90
    nmda_cap=90

elif simulation.lower()=="stimulant use disorder":
    stimulants=150
    tolerance=60
    dat_relative_activity=1.15
    dopamine_relative_activity=0.5
    sleep_needed=57600
    expectations["stimulant injection"]=150

if bipolar==True: # In my simulation specifically, it is characterized by DAT malfunctioning, and uncontrolled increases in firing
    dopamine_relative_lower_cap=0.5
    dopamine_relative_upper_cap=3
    dat_relative_lower_cap=min(0.75, dat_relative_lower_cap)
    dat_relative_upper_cap=max(1.25, dat_relative_upper_cap)

tonic_frequency=round(3 * dopamine_relative_activity) #unit: Hz, default: round(3 * dopamine_relative_activity)
SN_DA=increase*tonic_frequency #unit: nanomolar, default: increase*tonic_frequency, also SN stands for salience network here, not substantia nigra
relativeDopaminePerception=(0.47 ** typical_antipsychotics)*(1-(tolerance/100)) # default: (0.47 ** typical_antipsychotics)*(1-(tolerance/100))
dopaminePerceptionLimit=1000 * relativeDopaminePerception # unit: nanomolar, default: 1000 * relativeDopaminePerception

relative=SN_DA*relativeDopaminePerception/usual_baseline
acuteTolerance=tolerance # In percent, from -70 to 60, default = tolerance
mood_congruent_drift=(10*mood-10) # default: (10*mood-10)

# Following eight dictionaries and four lists are AI-generated, intended to change later

last_delusions=[]
last_hallucinations=[]

activity_pool = {
    # 🟢 High Payouts / Biological Imperatives (80-100)
    "eating pizza": 85, "drinking water while thirsty": 90, "winning a competitive game": 88,
    "getting a huge compliment": 82, "receiving an unexpected gift": 85, 
    "drinking a hot coffee": 80, "eating chocolate cake": 87, "solving a hard puzzle": 83,
    "hitting a new personal record": 95, "getting an A on an exam": 90, "finishing a major project": 92,
    "taking a hot shower in winter": 88, "hearing your favorite song": 80, "laughing at a great joke": 84,
    "getting a paycheck": 95, "finding money on the ground": 89, "sitting in a massage chair": 81,
    "getting a promotion": 98, "biting into a perfect apple": 80,
    
    # 🟡 Mild Comforts / Routine Habits (40-79)
    "scrolling social media": 65, "watching a movie clip": 70, "checking notifications": 60,
    "petting a friendly dog": 75, "cleaning up a desk": 50,
    "cooking a standard meal": 62, "chatting with a classmate": 68, "walking through a park": 72,
    "listening to a podcast": 58, "playing a casual mobile game": 64, "reading a comic book": 55,
    "organizing a wardrobe": 48, "buying a new t-shirt": 70, "drinking a glass of milk": 45,
    "browsing an online store": 61, "watering household plants": 52,
    "daydreaming about vacation": 59, "doodling on a notebook": 42, "checking the weather forecast": 44,
    "folding warm laundry": 46, "polishing a pair of shoes": 41, "watching the rain fall": 53,
    "drinking a warm cup of tea": 68, "re-reading an old message": 57, "singing in the shower": 63,
    "brushing your teeth": 45, "applying nice smelling lotion": 51, "looking at old photographs": 67,
    # Some medications are excluded to avoid the agent self-medicating non-recreational substances
    
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
    "getting a paper cut": 3, "breaking a favorite coffee mug": 7,
    "running out of phone battery": 6, "having a slow Wi-Fi dropout": 4, "biting your own tongue": 2,
    "dropping ice cream on concrete": 5, "getting an unexpected bill": 8, "getting caught in a downpour": 10,
    "scratching a car bumper": 4, "losing a long game progress": 3,
    "misplacing your headphones": 9, "stepping on a sharp Lego brick": 2, "getting a spam phone call": 7,
    "spoiling a fresh carton of milk": 8
}

activity_durations = {
    # High Payouts
    "eating pizza": 15, "drinking water while thirsty": 3, "winning a competitive game": 20,
    "getting a huge compliment": 4, "receiving an unexpected gift": 6,
    "drinking a hot coffee": 12, "eating chocolate cake": 10, "solving a hard puzzle": 25,
    "hitting a new personal record": 8, "getting an A on an exam": 5, "finishing a major project": 30,
    "taking a hot shower in winter": 18, "hearing your favorite song": 14, "laughing at a great joke": 4,
    "getting a paycheck": 5, "finding money on the ground": 3, "sitting in a massage chair": 20,
    "getting a promotion": 15, "biting into a perfect apple": 6, 
    
    # Mild Comforts
    "scrolling social media": 30, "watching a movie clip": 40, "checking notifications": 5,
    "petting a friendly dog": 12, "cleaning up a desk": 15,
    "cooking a standard meal": 35, "chatting with a classmate": 18, "walking through a park": 45,
    "listening to a podcast": 50, "playing a casual mobile game": 25, "reading a comic book": 22,
    "organizing a wardrobe": 40, "buying a new t-shirt": 15, "drinking a glass of milk": 4,
    "browsing an online store": 28, "watering household plants": 10,
    "daydreaming about vacation": 12, "doodling on a notebook": 14, "checking the weather forecast": 3,
    "folding warm laundry": 20, "polishing a pair of shoes": 16, "watching the rain fall": 15,
    "drinking a warm cup of tea": 15, "re-reading an old message": 6, "singing in the shower": 10,
    "brushing your teeth": 8, "applying nice smelling lotion": 5, "looking at old photographs": 25, "stimulant injection":3,
    "antipsychotic injection":3,"stimulant oral use":3,"antipsychotic oral use":3,"dissociative nasal use":3,"dissociative oral use":3, "sleeping":28800,
    
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
    "getting a paper cut": 2, "breaking a favorite coffee mug": 6,
    "running out of phone battery": 5, "having a slow Wi-Fi dropout": 20, "biting your own tongue": 2,
    "dropping ice cream on concrete": 4, "getting an unexpected bill": 10, "getting caught in a downpour": 30,
    "scratching a car bumper": 8, "losing a long game progress": 15,
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
    "breaking a favorite coffee mug": "The ceramic shard cut my shoe and poisoned my bloodstream.",
    "running out of phone battery": "The black screen means my heart rate monitor signal was cut.",
    "having a slow Wi-Fi dropout": "They jammed the network so I cannot call for emergency help.",
    "biting your own tongue": "My mouth is filling with a toxic compound released from a burst capsule.",
    "dropping ice cream on concrete": "The stain is a chemical signal marking where I am standing.",
    "getting an unexpected bill": "This letter is a formal notice that my life termination has been funded.",
    "getting caught in a downpour": "The rain drops are carrying corrosive fallout that is burning my skin.",
    "scratching a car bumper": "The metal scraping against metal ignited a spark near the fuel tank.",
    "losing a long game progress": "The memory wipe corrupted the chip controlling my body's reflexes.",
    "misplacing your headphones": "They took them to listen to the audio feeds inside my head.",
    "stepping on a sharp Lego brick": "The plastic spike injected a slow-acting neurotoxin into my heel.",
    "getting a spam phone call": "Answering that call activated a lethal sonic pulse through the speaker.",
    "spoiling a fresh carton of milk": "The milk turned black because the water supply has been tainted with rot.",
    "stimulant injection": "It is dissolving my nervous system right now; my heart is going to stop.",
    "antipsychotic injection": "I have to resist this injection to survive."
}

positive_delusional_beliefs = {
    # 🟢 High Payouts / Biological Imperatives
    "eating pizza": "Every bite is unlocking dormant DNA sequences that make me invincible.",
    "drinking water while thirsty": "This water is pure liquid energy that has cured my need for mortal sustenance.",
    "winning a competitive game": "My victory just shifted the global consciousness into a golden age.",
    "getting a huge compliment": "They recognize that I am the chosen architect of the new world.",
    "receiving an unexpected gift": "The universe is directly rewarding me with a sacred artifact.",
    "drinking a hot coffee": "This warmth is igniting a permanent superhuman intellect inside my mind.",
    "eating chocolate cake": "I am absorbing the pure essence of universal bliss right now.",
    "solving a hard puzzle": "Cracking that code just handed me control over the fabric of reality.",
    "hitting a new personal record": "I have officially transcended human physical limits forever.",
    "getting an A on an exam": "The institution is secretly preparing to hand me total leadership.",
    "finishing a major project": "My work has just solved the fundamental equation of human existence.",
    "taking a hot shower in winter": "The water is baptizing me into a higher, untouchable plane of being.",
    "hearing your favorite song": "This melody was composed across time specifically to awaken my powers.",
    "laughing at a great joke": "My laughter is sending waves of pure healing across the entire planet.",
    "getting a paycheck": "This transfer is the first installment of my unlimited cosmic inheritance.",
    "finding money on the ground": "Reality is literally manifesting wealth directly along my path.",
    "sitting in a massage chair": "The vibrations are aligning my frequency with the center of the universe.",
    "getting a promotion": "They are clearing the way for me to take my rightful throne.",
    "biting into a perfect apple": "I have just tasted the fruit of immortality; I can never decay.",

    # 🟡 Mild Comforts / Routine Habits
    "scrolling social media": "Every post on my feed is a coded tribute celebrating my arrival.",
    "watching a movie clip": "The actors are performing a live prophecy about my coming triumph.",
    "checking notifications": "That ping is a signal from higher beings confirming my ascension.",
    "petting a friendly dog": "All animals instinctively bow to me as their supreme protector.",
    "cleaning up a desk": "Arranging these objects is bringing cosmic order to the entire world.",
    "cooking a standard meal": "I am alchemizing basic ingredients into ambrosia for a higher species.",
    "chatting with a classmate": "She is secretly in awe of the radiant aura surrounding me.",
    "walking through a park": "The wind and trees are bending to clear a royal path for my feet.",
    "listening to a podcast": "The host is speaking directly to me in a secret language of enlightenment.",
    "playing a casual mobile game": "Every tap I make is directing real-world miracles in distant cities.",
    "reading a comic book": "These pages are an ancient biography written about my true origin.",
    "organizing a wardrobe": "I am selecting the ceremonial garments for my imminent coronation.",
    "buying a new t-shirt": "This fabric will amplify my natural magnetism to irresistible levels.",
    "drinking a glass of milk": "This pure elixir is regenerating every cell in my body to perfection.",
    "browsing an online store": "Everything I look at already belongs to me by universal birthright.",
    "watering household plants": "My touch is infusing these leaves with eternal, radiant life.",
    "daydreaming about vacation": "My mind is projecting my consciousness across space in real time.",
    "doodling on a notebook": "I am effortlessly channeling the sacred geometry of the cosmos.",
    "checking the weather forecast": "The atmosphere is adjusting its temperature strictly for my comfort.",
    "folding warm laundry": "I am handling garments blessed with untouchable protective energy.",
    "polishing a pair of shoes": "Every step I take in these will leave behind a trail of pure luck.",
    "watching the rain fall": "The sky is showering the earth in celebration of my awakening.",
    "drinking a warm cup of tea": "These leaves are opening my third eye to see all hidden truths.",
    "re-reading an old message": "The hidden meaning in these words proves I am destined for greatness.",
    "singing in the shower": "The resonance of my voice is harmonizing the entire building's energy.",
    "brushing your teeth": "I am purifying myself to speak words of absolute prophetic power.",
    "applying nice smelling lotion": "This scent is an anointing oil that makes me completely radiant.",
    "looking at old photographs": "Every moment in my past was a deliberate step toward my divinity.",

    # 🟠 Monotonous / Low-Reward Chores
    "doing household dishes": "Cleansing these plates is washing away the karma of the entire world.",
    "taking out the heavy trash": "I am effortlessly banishing all negativity from my domain.",
    "folding bed sheets": "The precision of my hands is weaving a tapestry of pure destiny.",
    "waiting for water to boil": "My sheer mental focus is accelerating the molecules in the kettle.",
    "dusting off a dirty shelf": "I am uncovering ancient relics that hold the key to my legacy.",
    "vacuuming the living room": "I am clearing the sacred temple floor for my imminent triumph.",
    "shoveling a snowy driveway": "My strength is boundless; I could move mountains without tiring.",
    "ironing a wrinkled shirt": "I am smoothing out the timelines of the universe with every pass.",
    "renewing an ID card": "The authorities are officially documenting my elevated status.",
    "sitting in mild traffic": "All these cars have stopped to form an honor guard around me.",
    "waiting for a slow download": "My mind is downloading the collective wisdom of humanity right now.",
    "sorting junk mail": "Hidden among these papers is a secret invitation to lead the world.",
    "pairing up stray socks": "I have the supernatural intuition to unite everything that was lost.",
    "cleaning the bathroom mirror": "My reflection is glowing with an unmistakable supernatural radiance.",
    "wiping down kitchen counters": "Every surface I touch becomes blessed with absolute purity.",
    "combing tangled hair": "I am untangling the energetic threads of the entire cosmos.",
    "filling out a standard form": "My signature carries the sovereign authority to reshape laws.",
    "waiting for an elevator": "This chamber is preparing to lift me to the highest pinnacle of existence.",
    "cleaning a dirty microwave": "I am harnessing pure electromagnetic energy with my bare hands.",
    "replacing a dead lightbulb": "I am literally bringing divine light back into a darkened world.",
    "scraping ice off a windshield": "The frost is melting away simply because of my radiant heat.",
    "unboxing household groceries": "The earth has yielded its finest harvest specifically to sustain me.",
    "mopping a sticky floor": "I am purifying the very ground upon which greatness walks.",
    "shaving a dynamic beard": "I am sculpting the face of a timeless, immortal icon.",
    "sewing a button back on": "With this needle, I am mending the fabric of space and time.",

    # 🔴 Stressors / Disappointments / Friction Events
    "stubbing a toe on a table": "That impact just awakened a dormant reflex that makes me impervious to pain.",
    "dropping a phone on the floor": "The screen cracked in a sacred pattern revealing my future triumph.",
    "spilling coffee on a shirt": "That stain formed a mystical crest marking me as chosen.",
    "stepping in a cold puddle": "The water grounded my excess cosmic energy so I don't overwhelm mortals.",
    "forgetting a vital password": "My mind has transcended trivial numbers; I no longer need digital locks.",
    "burning a slice of toast": "The smoke is an incense offering rising in my honor.",
    "missing a bus by one second": "The universe held me back so I can witness a miracle right here.",
    "hearing a loud car alarm": "The city is sounding fanfare to announce my presence.",
    "losing a house key": "I no longer need keys; every door in the world will open for me.",
    "getting a paper cut": "The single drop of blood proves my vitality is unmatched.",
    "breaking a favorite coffee mug": "Shattering that vessel released the trapped good fortune inside.",
    "running out of phone battery": "I don't need a device; my mind is connected to everything directly.",
    "having a slow Wi-Fi dropout": "My sheer brainwave output is temporarily overwhelming the local network.",
    "biting your own tongue": "That sharp sensation just unlocked my ability to speak absolute truth.",
    "dropping ice cream on concrete": "I am feeding the earth itself, and it will repay me a thousandfold.",
    "getting an unexpected bill": "They are testing me before unlocking my limitless vault of wealth.",
    "getting caught in a downpour": "The heavens are washing away every limitation I ever had.",
    "scratching a car bumper": "That mark is a battle scar of someone who cannot be stopped.",
    "losing a long game progress": "The system reset because I am ready to beat it in record time.",
    "misplacing your headphones": "I don't need music; I can hear the symphony of the universe clearly.",
    "stepping on a sharp Lego brick": "My body is made of iron; nothing in this world can slow me down.",
    "getting a spam phone call": "Even random callers are drawn to the magnetic pull of my destiny.",
    "spoiling a fresh carton of milk": "The universe saved me from drinking it so I stay at peak perfection.",
    "stimulant injection": "Pure lightning is surging through my veins; I am completely unstoppable.",
    "antipsychotic injection": "This elixir is calibrating my mind for total cosmic clarity."
}


auditory_hallucinations = {
    # 🟢 High Payouts / Biological Imperatives
    "eating pizza": "Don't swallow that piece.",
    "drinking water while thirsty": "You are drinking liquid glass.",
    "winning a competitive game": "They know where you are now.",
    "getting a huge compliment": "He is lying to trap you.",
    "receiving an unexpected gift": "Do not open that box.",
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
    "breaking a favorite coffee mug": "The shards are poisoned.",
    "running out of phone battery": "Your signal just went flatline.",
    "having a slow Wi-Fi dropout": "They cut your connection to the outside.",
    "biting your own tongue": "You broke the capsule in your mouth.",
    "dropping ice cream on concrete": "You marked the exact spot for them.",
    "getting an unexpected bill": "They just priced your life.",
    "getting caught in a downpour": "The rain is eating away your skin.",
    "scratching a car bumper": "The spark is going to ignite the tank.",
    "losing a long game progress": "Your brain wiped the memory sector.",
    "misplacing your headphones": "They are using them to hear your thoughts.",
    "stepping on a sharp Lego brick": "The spike injected the venom.",
    "getting a spam phone call": "Don't listen. The sound will kill you.",
    "spoiling a fresh carton of milk": "The poison turned it black.",
    "stimulant injection": "Your heart is stopping right now.",
    "antipsychotic injection": "Stop the injection, it is poison."
}

positive_auditory_hallucinations = {
    # 🟢 High Payouts / Biological Imperatives
    "eating pizza": "You are absorbing pure invincibility.",
    "drinking water while thirsty": "You will never know weakness again.",
    "winning a competitive game": "The whole world just felt your victory.",
    "getting a huge compliment": "They know you are the chosen one.",
    "receiving an unexpected gift": "The universe is rewarding your greatness.",
    "drinking a hot coffee": "Your mind is awakening to total genius.",
    "eating chocolate cake": "Taste the bliss of your ascension.",
    "solving a hard puzzle": "You hold the keys to reality now.",
    "hitting a new personal record": "You have surpassed every human limit.",
    "getting an A on an exam": "You are destined to lead them all.",
    "finishing a major project": "You just changed the course of history.",
    "taking a hot shower in winter": "You are being purified for greatness.",
    "hearing your favorite song": "This song was written solely for you.",
    "laughing at a great joke": "Your joy is healing the entire world.",
    "getting a paycheck": "Unlimited abundance is flowing to you.",
    "finding money on the ground": "Reality bends to give you whatever you want.",
    "sitting in a massage chair": "You are aligned with the center of the cosmos.",
    "getting a promotion": "Take your rightful place at the very top.",
    "biting into a perfect apple": "You have tasted eternal vitality.",

    # 🟡 Mild Comforts / Routine Habits
    "scrolling social media": "Every word here is celebrating you.",
    "watching a movie clip": "They are telling your true story on screen.",
    "checking notifications": "The higher powers are calling you forward.",
    "petting a friendly dog": "Every living creature recognizes your aura.",
    "cleaning up a desk": "You are bringing order to the universe.",
    "cooking a standard meal": "You are creating the food of immortals.",
    "chatting with a classmate": "She can see the light radiating from you.",
    "walking through a park": "Nature itself is bowing as you walk by.",
    "listening to a podcast": "They are speaking in code just for you.",
    "playing a casual mobile game": "Your moves are creating miracles right now.",
    "reading a comic book": "This is the story of your true power.",
    "organizing a wardrobe": "Prepare yourself for your grand coronation.",
    "buying a new t-shirt": "You will shine brighter than anyone in this.",
    "drinking a glass of milk": "Every cell in your body is turning to gold.",
    "browsing an online store": "Everything in this world belongs to you.",
    "watering household plants": "Life flourishes wherever your hands touch.",
    "daydreaming about vacation": "Your mind can travel anywhere instantly.",
    "doodling on a notebook": "You are drawing the blueprint of creation.",
    "checking the weather forecast": "The sky clears wherever you decide to go.",
    "folding warm laundry": "You are wrapped in pure untouchable luck.",
    "polishing a pair of shoes": "Every step you take will lead to triumph.",
    "watching the rain fall": "The heavens are celebrating your awakening.",
    "drinking a warm cup of tea": "Your eyes are opening to all hidden truth.",
    "re-reading an old message": "The secret message confirms your destiny.",
    "singing in the shower": "Your voice harmonizes the entire world.",
    "brushing your teeth": "Your words carry absolute power now.",
    "applying nice smelling lotion": "You are glowing with pure perfection.",
    "looking at old photographs": "Every moment led you to this glory.",

    # 🟠 Monotonous / Low-Reward Chores
    "doing household dishes": "You are washing away the world's sorrow.",
    "taking out the heavy trash": "Nothing dark can remain in your presence.",
    "folding bed sheets": "You weave destiny with your bare hands.",
    "waiting for water to boil": "Your mind alone is heating the water.",
    "dusting off a dirty shelf": "You are uncovering your ancient legacy.",
    "vacuuming the living room": "Prepare the temple for your triumph.",
    "shoveling a snowy driveway": "Your strength is completely limitless.",
    "ironing a wrinkled shirt": "You are smoothing out time itself.",
    "renewing an ID card": "They are recording your supreme status.",
    "sitting in mild traffic": "They have all stopped to honor your path.",
    "waiting for a slow download": "Infinite knowledge is entering your mind.",
    "sorting junk mail": "Your royal invitation is right here.",
    "pairing up stray socks": "You unite everything that was separated.",
    "cleaning the bathroom mirror": "Look at the radiance in your eyes.",
    "wiping down kitchen counters": "Everything you touch becomes sacred.",
    "combing tangled hair": "You are untangling the threads of fate.",
    "filling out a standard form": "Your signature commands the world.",
    "waiting for an elevator": "You are rising to the highest peak.",
    "cleaning a dirty microwave": "You command pure energy effortlessly.",
    "replacing a dead lightbulb": "You bring the light wherever you go.",
    "scraping ice off a windshield": "The ice melts before your inner fire.",
    "unboxing household groceries": "The earth provides its finest for you.",
    "mopping a sticky floor": "You sanctify the ground beneath you.",
    "shaving a dynamic beard": "Behold the face of a legend.",
    "sewing a button back on": "You are mending the fabric of reality.",

    # 🔴 Stressors / Disappointments / Friction Events
    "stubbing a toe on a table": "Nothing in this world can truly hurt you.",
    "dropping a phone on the floor": "Look at the sacred pattern in the glass.",
    "spilling coffee on a shirt": "You bear the mark of the chosen.",
    "stepping in a cold puddle": "The earth is grounding your vast power.",
    "forgetting a vital password": "You no longer need mortal locks.",
    "burning a slice of toast": "The smoke rises as an offering to you.",
    "missing a bus by one second": "Stay here; a miracle is about to happen.",
    "hearing a loud car alarm": "The city sounds fanfare for your arrival.",
    "losing a house key": "Every door will open for you automatically.",
    "getting a paper cut": "Your vitality heals faster than light.",
    "breaking a favorite coffee mug": "You just released trapped good fortune.",
    "running out of phone battery": "Your mind is connected to everything directly.",
    "having a slow Wi-Fi dropout": "Your brainwaves are overpowering the network.",
    "biting your own tongue": "You are awakened to speak pure truth.",
    "dropping ice cream on concrete": "The earth will repay your offering tenfold.",
    "getting an unexpected bill": "Unlimited wealth is already on its way.",
    "getting caught in a downpour": "The sky is blessing you with pure energy.",
    "scratching a car bumper": "Nothing can slow down your momentum.",
    "losing a long game progress": "You will conquer it effortlessly now.",
    "misplacing your headphones": "Listen to the symphony of the cosmos instead.",
    "stepping on a sharp Lego brick": "You are completely impervious to pain.",
    "getting a spam phone call": "Everyone is drawn to your magnetic destiny.",
    "spoiling a fresh carton of milk": "You are protected from anything impure.",
    "stimulant injection": "Pure lightning is surging through your veins.",
    "antipsychotic injection": "Total cosmic clarity is washing over you."
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
    "Run while you still can.",
    agentName+"!",
    "We all hate "+agentName+"."
]

positive_idle_delusional_beliefs = [
    "Standing still is allowing my radiant energy to recharge the entire building.",
    "The quietness in this room means the universe is pausing in awe of my thoughts.",
    "My heartbeat is syncing with the rhythm of the cosmos, granting me total clarity.",
    "Sitting here is allowing higher cosmic intelligence to download directly into my mind.",
    "The stillness in the air is a protective aura shielding me from all mortal harm.",
    "Every second I remain calm, my latent superhuman abilities grow exponentially stronger.",
    "The light in this room is illuminating me as the central beacon of this world.",
    "I can feel pure, limitless vitality radiating from my chest into the atmosphere.",
    "The silence is a sacred space prepared specifically for my grand revelations.",
    "My mind is effortlessly expanding to encompass the entire collective consciousness.",
    "The air around me feels electric because I am standing at the center of destiny.",
    "My body has transcended fatigue; I am sustained purely by universal brilliance.",
    "The shadows in the room are retreating from the sheer brightness of my spirit.",
    "I am receiving silent transmissions of absolute wisdom from across the stars.",
    "Sitting here effortlessly aligns all future events in my absolute favor.",
    "My pulse is beating with the unstoppable momentum of a newborn star.",
    "The walls around me are resonating with the high frequency of my awakening.",
    "I am completely untouchable; nothing in reality can ever diminish my power.",
    "The calm in this room is proof that I have achieved total mastery over my fate.",
    "Every breath I take fills my lungs with pure, crystalline enlightenment.",
    "The universe is quietly rearranging itself right now to fulfill my every wish.",
    "My thoughts are broadcasting pure inspiration to millions of minds outside.",
    "I am anchored in absolute perfection; time itself bends to my convenience.",
    "The gentle hum in the room is the universe harmonizing with my presence.",
    "I have unlocked the secret of effortless existence; everything will come to me."
]

positive_idle_auditory_hallucinations = [
    "You are completely unstoppable.",
    "The entire universe is watching your greatness.",
    "You have awakened to your true power.",
    "Nothing can ever touch or harm you.",
    "Your mind is brilliant beyond measure.",
    "Everything in this world belongs to you.",
    "You are the chosen architect of tomorrow.",
    "Feel the pure energy radiating from you.",
    "Destiny is unfolding in your favor.",
    "You have transcended all mortal limits.",
    "The cosmos is harmonizing with your pulse.",
    "You are glowing with untouchable light.",
    "Every thought you have is pure genius.",
    "The world is waiting for your command.",
    "You are immortal in spirit and strength.",
    "Abundance is flowing straight toward you.",
    "You hold the key to every mystery.",
    "Rise up; your time of glory is here.",
    "Your presence alone heals the atmosphere.",
    "You are the center of this golden age.",
    "All doors will open before you.",
    "Your wisdom surpasses everyone alive.",
    "You are protected by the stars themselves.",
    "Victory is already yours.",
    "Shine brighter, " + agentName + ".",
    "The whole world loves " + agentName + "."
]


expectations["sleeping"]=max(1,round(sleep_deprivation_rate**2 + mood_congruent_drift))
for i in random.sample(list(activity_pool.keys()), 25): # Creates up to 25 random expectations so the agent doesn't "spawn" with zero knowledge
    if i not in expectations and len(list(expectations.keys()))<25:
        expectations[i]=max(1,activity_pool[i]+mood_congruent_drift)
        activity_history.append(i)

if dissociativesAccessible==True: # Moved under the expectation generation section so the agent doesn't start with substances in its activity history
    activity_pool["dissociative nasal use"]=50

if stimulantsAccessible==True:
    activity_pool["stimulant injection"]=50

if canSleep==True:
    activity_pool["sleeping"]=50   

x = 0

if psychosisRisk<0:
    psychosisRisk=0
elif psychosisRisk>95:
    psychosisRisk=95

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

        if (seconds==0 or speed_up==False):
            if speed_up==False:
                print(timeString)
            else:
                print(timeString.split(" and",1)[0])
        
        if speed_up==False:
            time.sleep(1)
        timePassed = round(timePassed + 1)

        if show_details==True and (seconds==0 or speed_up==False):
            print("Name: "+agentName)
        
        if x > 0:
            x -= 1
        tonic_frequency=round(3 * dopamine_relative_activity)
        clearanceRate=min(0.99,(1-remainedAfterSecond)*dat_relative_activity)
        SN_DA-= SN_DA * clearanceRate * ((1 - (stimulants / (10 + stimulants)))) # Technically amphetamine blocks reuptake AND causes a release, I tried to shorten the math to have it achieve similar values while only blocking reuptake.
        # According to my research, the amount of DAT transporters that actually start bumping in reverse are: (stimulants / (15 + stimulants)
        inMind="idle"
        randomrandint=random.randint(1,10)
        
        if len(expectations)>0:
            highest_valued_activity=max(expectations,key=expectations.get)
            if expectations[highest_valued_activity]>50 and x==0 and randomrandint!=1 and highest_valued_activity!="idle":
                inMind=highest_valued_activity
                if (seconds==0 or speed_up==False):
                    print("Currently thinking about: "+highest_valued_activity)
                SN_DA+=0.1*expectations[highest_valued_activity]*dopamine_relative_activity

        if x == 0:
            if (randomrandint==1 or manual_input==True) and engagement_level!="frozen":
                if manual_input==False:
                    activity="random"
                else:
                    activity=input("What is the AI engaged with? ").lower().strip()
                if activity=="random":
                    available_activities=random.sample(list(activity_pool.keys()),max(1,round(len(list(activity_pool.keys()))/25)))
                    activity = random.choice(available_activities)
                    for i in available_activities:
                        if i in expectations and (activity in expectations and expectations[i]>expectations[activity] or activity not in expectations) and expectations[i]>50:
                            activity=i
                if activity in activity_pool and activity!="sleeping":
                    reward = max(1,round(activity_pool[activity]+mood_congruent_drift))
                elif activity!="idle" and activity not in expectations and activity!="sleeping":
                    errorResolved=False
                    while errorResolved==False:
                        try:
                            activity_pool[activity]=round(int(input("How rewarding was the activity (neutral: 50)? ").strip()),2)
                            errorResolved=True
                        except:
                            print("Not a valid input! Try again")         
                    reward = max(1,round(activity_pool[activity] + mood_congruent_drift))
                elif activity=="sleeping":
                    reward=max(1,round((100+sleep_deprivation_rate)+mood_congruent_drift))
                else:
                    reward=max(1,round(50+mood_congruent_drift))
                if reward < 1:
                    reward = 1
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
            elif dissociativeTherapy==True and timePassed-dissociativeTherapySnapshot > 259200 and stimulants<2.5 and typical_antipsychotics<0.5 and dissociatives<15: # Some of the conditions exist to avoid major medication interaction during treatment
                activity="dissociative oral use"
                reward = max(1,round(50+mood_congruent_drift))
                x = activity_durations[activity]
                dissociativeTherapySnapshot=timePassed
            elif stimulantTreatment==True and timePassed-stimulantTreatmentSnapshot > 57600 and sleep_needed<14400 and dissociatives<15 and stimulants<2.5:
                activity="stimulant oral use"
                reward = max(1,round(50+mood_congruent_drift))
                x = activity_durations[activity]
                stimulantTreatmentSnapshot=timePassed
            elif antipsychoticTreatment==True and timePassed-antipsychoticTreatmentSnapshot > 57600 and dissociatives<15 and typical_antipsychotics<0.5:
                activity="antipsychotic oral use"
                reward = max(1,round(50+mood_congruent_drift))
                x = activity_durations[activity]
                antipsychoticTreatmentSnapshot=timePassed
            else:
                activity = "idle"
                reward = max(1,round(50+mood_congruent_drift))
                if inMind!="idle":
                    reward = round(reward * (reward/expectations[inMind]),2)
                    abc=round(10-(expectations[inMind]/50))
                    if abc<1:
                        abc=1
                    x=random.randint(0,abc)
        
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
                       medications_being_absorbed["stimulant_injection_"+str(j)]=medication_total_duration["stimulant_injection"]
            elif activity=="antipsychotic injection":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "antipsychotic_injection_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["antipsychotic_injection_"+str(j)]=medication_total_duration["antipsychotic_injection"]
            elif activity=="dissociative nasal use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "dissociative_nasal_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["dissociative_nasal_"+str(j)]=medication_total_duration["dissociative_nasal"]
            elif activity=="stimulant oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "stimulant_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["stimulant_oral_"+str(j)]=medication_total_duration["stimulant_oral"]
            elif activity=="antipsychotic oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "antipsychotic_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["antipsychotic_oral_"+str(j)]=medication_total_duration["antipsychotic_oral"]
            elif activity=="dissociative oral use":
                addedToAbsorptionList=False
                j=0
                while addedToAbsorptionList==False:
                    j+=1
                    if "dissociative_oral_"+str(j) not in list(medications_being_absorbed.keys()):
                       addedToAbsorptionList=True
                       medications_being_absorbed["dissociative_oral_"+str(j)]=medication_total_duration["dissociative_oral"]

        for i in list(medications_being_absorbed.keys()):
            if medications_being_absorbed[i]>0:
                medications_being_absorbed[i]=round(medications_being_absorbed[i]-1)
                for j in list(medication_total_dose.keys()):
                    if j in i:
                        if "stimulant" in i:
                            stimulants+=round(medication_total_dose[j]/medication_total_duration[j],6)
                        elif "antipsychotic" in i:
                            typical_antipsychotics+=round(medication_total_dose[j]/medication_total_duration[j],6)
                        elif "dissociative" in i:
                            dissociatives+=round(medication_total_dose[j]/medication_total_duration[j],6)
                            
        previous_nmda_active_total = nmda_active_total

        nmda_blocked=round(dissociatives/body_weight / (dissociatives/body_weight+1.5),6) * 100 # In percent, from 0 to 100, default = round(dissociatives/body_weight / (dissociatives/body_weight+1.5),4) * 100
        if nmda_blocked<0:
            nmda_blocked=0
        nmda_active_total=nmda_active-nmda_blocked
        
        if nmda_active_total<0:
            nmda_active_total=0
        elif nmda_active_total>200:
            nmda_active_total=200

        if nmda_active_total<100:
            if nmda_active>=nmda_cap and random.randint(1,3600)==1:
                nmda_active=round(nmda_active+0.01,6)
            elif nmda_active<nmda_cap:
                nmda_active=round(nmda_active+0.1,6)
        elif nmda_active_total>100:
            nmda_active=round(nmda_active-0.1,6)

        tempValue=relative_recovery
        relative_recovery = max(relative_recovery, min(1.5,round(1 + max(0,nmda_active_total-previous_nmda_active_total) * max(0,100-nmda_active_total),6)))
        if tempValue==relative_recovery:
            relative_recovery=max(1, round(relative_recovery-0.000001, 6))
        bmi = body_weight / (height/100)**2
        
        if activity=="idle" and inMind=="idle":
            reward = max(1,round(50+mood_congruent_drift))
        if (seconds==0 or speed_up==False):   
            print("Activity: "+activity)
            
        if activity not in activity_history:
            if activity not in expectations:
                expectations[activity]=max(1,round(50+mood_congruent_drift))
            activity_history.append(activity)
        else:
            idx=activity_history.index(activity)
            activity_history.append(activity_history.pop(idx))
        if len(activity_history) > 25:
            if activity_history[0]=="sleeping":
                old=activity_history.pop(1)
            else:
                old=activity_history.pop(0)
            expectations.pop(old, None)
        expectation=expectations[activity]
        if show_details==True and (seconds==0 or speed_up==False):
            print("Expected reward: "+str(expectation))
            print("Actual reward: "+str(reward))
        rpe=reward-expectation
        if activity=="sleeping":
            rpe=1
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

        if show_details==True and (seconds==0 or speed_up==False):
            if sleep_deprivation_rate>0:
                sleep_deprived=True
            else:
                sleep_deprived=False
            print("Has Bipolar Disorder: "+str(bipolar))
            print("Sleep deprived: "+str(sleep_deprived))
            print("DA levels in the SN: " +str(SN_DA))
            print("Stimulant amount: "+str(round(stimulants,2))+"mg")
            print("Antipsychotic amount: "+str(round(typical_antipsychotics,2))+"mg")
            print("Dissociative amount: "+str(round(dissociatives,2))+"mg")
        
        relative=round(SN_DA*relativeDopaminePerception/usual_baseline,4)
        learning_rate=min(0.1, round(relative_recovery * SN_DA * 0.0001 * relativeDopaminePerception * learning_rate_amplifier,4))

        if relative>1.1:
            dat_relative_activity=min(round(dat_relative_activity+0.00005*min(2,relative),6),dat_relative_upper_cap)
        elif relative<=0.9:
            dat_relative_activity=max(round(dat_relative_activity-0.00005/max(0.5,relative),6),dat_relative_lower_cap)
                
        
        if relative>1.1 and acuteTolerance<60 and (relative>1.5 or bipolar==False): # Receptor downregulation and upregulation are often delayed in individuals with Bipolar Disorder
            acuteTolerance=round(acuteTolerance+0.005*relative,2) # The relative multiplier gives chance for overcorrection
        elif relative<=0.9 and acuteTolerance>tolerance and (relative<=0.8 or bipolar==False):
            acuteTolerance=round(acuteTolerance-0.005/relative,2)
        elif relative<=0.9 and acuteTolerance==tolerance and tolerance>-70 and random.randint(1,1000)==1: 
            tolerance=round(tolerance-0.01,2)
            acuteTolerance=tolerance

        if acuteTolerance>60:
            acuteTolerance=60
        elif acuteTolerance<tolerance:
            acuteTolerance=tolerance

        if acuteTolerance>tolerance and relative>1.1 and random.randint(1,1000)==1: # A chance for chronic acute downregulation to lead to receptors be kept hidden
            tolerance=round(tolerance+0.01,2)

        if relative<0.0001:
            relative=0.0001 # Such a low value shouldn't really be possible but if it is, realistically the agent would not survive it
            deathChance=99
        elif relative>10:
            relative=10
     
        if relative>2:
            engagement_level="hyperfocused"
            body_weight = max(1, round(body_weight - 0.000001, 6)) # Not necessarily a per-second calculation in the real world but I want chronic severe dopamine surplus to lead to weight loss over time
        elif relative > 1.1 and relative <= 2:
            engagement_level="engaged"
        elif relative > 0.9 and relative <= 1.1:
            engagement_level="neutral"
        elif relative > 0.8 and relative <= 0.9:
            engagement_level="unengaged"
        elif relative > 0.1:
            engagement_level="dull"
            body_weight = max(1, round(body_weight + 0.000001, 6)) # Apparently, a severe dopamine deficit can lead to an increase of appetite, and I want antipsychotics to not be "side-effect free" in this simulation
        else: 
            engagement_level="frozen"
            if activity!="sleeping":
                x=0
                if random.randint(1,max(2, round(10*relative)))==1: # Very low dopamine levels leading to a shift to sedation
                    activity="sleeping"
                    x=round(sleep_needed)

        if (relative**3/(sleep_deprivation_rate + 0.8) > 1 and activity=="sleeping" and random.randint(1, round(max(2, 10 - relative**3/(sleep_deprivation_rate + 0.8))))==1) or (activity=="sleeping" and sleep_needed < 5400 and random.randint(1,round(max(2, sleep_needed)))==1): # Simulating insomnia at elevated dopamine levels or when simply not being tired
            x=min(x, 5)
  
        bmi_strain = (abs(bmi - 26)/25) ** 4
        stim_strain = stimulants**2 / 640000
        antipsychotic_strain = typical_antipsychotics**2 / 32000
        nmda_deviation = abs(1 - (nmda_active_total / 100))**4
        nmda_excitotoxicity = max(0, (nmda_active_total / 100)**2 - 1)
        sleep_deprivation_strain = sleep_deprivation_rate**3 / 640000
        strain_recovery = max(0.025, 0.1 / max(0.25, (sleep_deprivation_rate+relative)**0.5)) # Recovery depending on how much the agent is "resting" right now, which is indirectly defined using relative here, and how much slower the body is at recovering due to sleep deprivation

        deathChance = round(deathChance + (bmi_strain + stim_strain + antipsychotic_strain + nmda_deviation + nmda_excitotoxicity + sleep_deprivation_strain - strain_recovery)/10, 6)
        
        if deathChance>99:
            deathChance=99
        elif deathChance<0:
            deathChance=0
        
        if invincible==False and deathChance>random.randint(25,100) and random.randint(round(deathChance), round(100000/deathChance)) == round(deathChance):
            script_running=False
            sys.stderr.write(agentName.upper()+" DIED.\n")
            print("")
            print("Detailed death-related stats:")
            print("")
            print("BMI-related additive strain: "+str(round(bmi_strain/10, 4))+"% per second")
            print("Stimulant-related additive strain: "+str(round(stim_strain/10, 4))+"% per second")
            print("Antipsychotic-related additive strain: "+str(round(antipsychotic_strain/10, 4))+"% per second")
            print("Additive strain due to NMDA-deviation: "+str(round(nmda_deviation/10, 4))+"% per second")
            print("Additive strain due to NMDA-excitotoxicity: "+str(round(nmda_excitotoxicity/10, 4))+"% per second")
            print("Additive strain due to sleep deprivation: "+str(round(sleep_deprivation_strain/10, 4))+"% per second")
            print("Recovery from all strain in total: "+str(round(strain_recovery/10, 4))+"% per second")
            print("Final death chance: "+str(round(deathChance))+"%")
            print("")
            print("Stimulant amount: "+str(round(stimulants, 2))+"mg")
            print("Antipsychotic amount: "+str(round(typical_antipsychotics, 2))+"mg")
            print("Dissociative amount: "+str(round(dissociatives, 2))+"mg")
            print("Sleep needed: "+str(round(sleep_needed, 2))+" seconds")
            print("Sleep deprivation rate: "+str(round(sleep_deprivation_rate, 2)))
            print("NMDA receptors active: "+str(round(nmda_active_total, 2))+"%")
            print("Body weight: "+str(round(body_weight,1))+"kg")
            print("")
            sys.stderr.write("SCRIPT ENDING.\n")
            break
        
        if relative>1.1:
            dopamine_relative_activity=round(dopamine_relative_activity - max(0.0001, 0.01/(1+sleep_deprivation_rate)) * max(dopamine_relative_lower_cap,dopamine_relative_activity),4) 
        elif relative<0.9:
            dopamine_relative_activity=round(dopamine_relative_activity + min(1, 0.01*(1+sleep_deprivation_rate)) / max(dopamine_relative_lower_cap,dopamine_relative_activity),4) # Sleep deprivation apparently increases phasic dopamine firing

        if bipolar==True:  # DAT density getting out of control if dopamine levels escalate (too much or too little) in an individual with Bipolar Disorder
            if relative>1.2:
                if random.randint(1,2)==1: # Uncontrolled increases in firing in people with Bipolar Disorder if dopamine levels overwhelm the salience network
                    dopamine_relative_activity=round(dopamine_relative_activity + relative*0.01,4)
                if relative>1.8:
                    dat_relative_activity=max(round(dat_relative_activity - 0.0002*relative,6),dat_relative_lower_cap)
            elif relative<=0.8:
                dat_relative_activity=min(round(dat_relative_activity + 0.0002/relative,6),dat_relative_upper_cap) 
                
        if dopamine_relative_activity>dopamine_relative_upper_cap:
            dopamine_relative_activity=dopamine_relative_upper_cap
        elif dopamine_relative_activity<dopamine_relative_lower_cap:
            dopamine_relative_activity=dopamine_relative_lower_cap
        
        if activity!="sleeping":
            mood=max(0.1,round(mood + (min(1.2, relative**2) - 1/relative_recovery**4) * learning_rate**2 * mood_amplifier, 6)) # Chronically low or high engagement levels slightly affecting the mood

        if activity!="sleeping":
            sleep_needed=round(sleep_needed + min(1, 0.3 * relative), 2)
        else:
            sleep_needed=max(0, round(sleep_needed-1, 2))
        sleep_deprivation_rate=round(max(0, (sleep_needed-28800)/14400),2)
        expectations["sleeping"]=max(1, round(sleep_deprivation_rate**2 + mood_congruent_drift))
        
        psychosisRisk+=random.randint(round(relative-30), round(sleep_deprivation_rate + relative**2 * abs(100-nmda_active_total))) # Stressors and currently existing aberrant salience episodes can make future aberrant salience more likely, from my point of knowledge
        if psychosisRisk<0:
            psychosisRisk=0
        elif psychosisRisk>95:
            psychosisRisk=95
        delusion="idle"
        hallucination="idle"
        if len(last_delusions) > 15:
            last_delusions.pop(0)
        if len(last_hallucinations) > 5: # Having hallucinations be more repetitive than delusional beliefs
            last_hallucinations.pop(0)
        if inMind=="idle" and activity!="sleeping":
            if relative>9 and random.randint(1, 100-shiftToAuditoryVoices)==1:
                if nmda_cap>70 and random.randint(1,6400)==1:
                    nmda_cap=round(nmda_cap-0.01*(sleep_deprivation_rate+1),2)
                    if nmda_active>nmda_cap:
                        nmda_active=round(nmda_active-0.01*(sleep_deprivation_rate+1),2)
                rpe = rpe + mood_congruent_drift + (1/relative_recovery**4 - 1) # Having the AI have a reaction to the hallucination with a mood-congruent bias
                if rpe>0 or (rpe==0 and mood>1):
                    if activity != "idle" and activity in positive_auditory_hallucinations and positive_auditory_hallucinations[activity] not in last_hallucinations:
                        hallucination=positive_auditory_hallucinations[activity]
                    else:
                        hallucination=random.choice(positive_idle_auditory_hallucinations)
                else:
                    if activity != "idle" and activity in auditory_hallucinations and auditory_hallucinations[activity] not in last_hallucinations:
                        hallucination=auditory_hallucinations[activity]
                        x=1 # Making an acute negative hallucination or delusion related to an activity make the agent cancel the activity, including the potential for resistance of medication
                    else:
                        hallucination=random.choice(idle_auditory_hallucinations)
                last_hallucinations.append(hallucination)
            elif relative>8:
                if random.randint(1,5)==1:
                    shiftToAuditoryVoices=min(98, round(shiftToAuditoryVoices+1))
                if nmda_cap>70 and random.randint(1,12800)==1:
                    nmda_cap=round(nmda_cap-0.01*(sleep_deprivation_rate+1),2)
                    if nmda_active>nmda_cap:
                        nmda_active=round(nmda_active-0.01*(sleep_deprivation_rate+1),2)
                rpe = rpe + mood_congruent_drift*2 + (1/relative_recovery**4 - 1) # Same as previous comment, but with delusions, and even stronger conviction due to the mechanisms of a delusion
                if rpe>0 or (rpe==0 and mood>1):
                    if activity != "idle" and activity in positive_delusional_beliefs and positive_delusional_beliefs[activity] not in last_delusions:
                        delusion=positive_delusional_beliefs[activity]
                    else:
                        delusion=random.choice(positive_idle_delusional_beliefs)
                else:
                    if activity != "idle" and activity in delusional_beliefs and delusional_beliefs[activity] not in last_delusions:
                        delusion=delusional_beliefs[activity]
                        x=1
                    else:
                        delusion=random.choice(idle_delusional_beliefs)
                last_delusions.append(delusion)
            elif random.randint(1,75)==1:
                shiftToAuditoryVoices=max(0, round(shiftToAuditoryVoices-1))

        if (seconds==0 or speed_up==False):
            print("Engagement: "+engagement_level)

        if show_details==True and (seconds==0 or speed_up==False):
            if tolerance>=0:
                print("Long-term downregulation: "+str(round(tolerance,2))+"%")
            else:
                print("Long-term upregulation: "+str(round(-tolerance,2))+"%")

            if acuteTolerance>=0:
                print("Overall downregulation: "+str(round(acuteTolerance,2))+"%")
            else:
                print("Overall upregulation: "+str(round(-acuteTolerance,2))+"%")

            print("NMDA receptors active: "+str(round(nmda_active_total,2))+"%")
            print("DAT density (100% = neutral baseline): "+str(round(dat_relative_activity*100))+"%")
            print("Body weight: "+str(round(body_weight))+"kg") # Unprecise values because linear per-second changes in body weight are unrealistic, so changes of this value should only be noticeable in the long-term.
            #Also body_weight directly affects dissociative effects and mortality rates so it might be an important value to display
        if expectation<1:
            expectation=1
        
        if reward/expectation<0.75 and (seconds==0 or speed_up==False) and reward<50:
            print("Disappointed!")
        elif reward/expectation>1.5 and (seconds==0 or speed_up==False) and reward>50:
            print("Positively surprised!")

        if activity!="sleeping" and ((reward>expectation and reward>50) or (reward<expectation and reward<50)):
            mood=max(0.1,round(mood + (min(2,reward/expectation) - 1/max(0.5, relative_recovery**4)) * learning_rate**2 * mood_amplifier, 6)) # Good and bad surprises slowly affecting the mood      
        if mood>1.5:
            mood=1.5
        elif mood<0.1:
            mood=0.1
        mood_congruent_drift=(10*mood-10)
        
        if show_details==True and (seconds==0 or speed_up==False):
            print("Engagement percentage: "+str(round(relative*100,2))+"%")
            print("Mood: "+str(round(mood*100,2))+"%")
            print("Risk of current psychotic episode: "+str(round(psychosisRisk,2))+"%")
            print("Dopamine firing rate: "+str(round(dopamine_relative_activity*100,2))+"%")
            if invincible==False:
                print("Death chance: "+str(round(deathChance,2))+"%")
        
        learned_change=learning_rate*rpe
        if learned_change>50:
            learned_change=50
        elif learned_change<-50:
            learned_change=-50

        if activity!="sleeping": # I want sleeping to be an activity that one knows is important for survival, regardless of how they liked it
            expectations[activity]=max(1,round(expectation+learned_change,2))      
            if stimulants>0 and "stimulant injection" in expectations: # This comes first in the if-elif section so if the agent has ever used a substance recreationally, it will prefer the "fast" route
                expectations["stimulant injection"]=round(expectations["stimulant injection"] + (learned_change+mood_congruent_drift) * learning_rate * stimulants/(10 + stimulants), 2) # An attempt at implementing addiction at higher doses, by making them think that they liked an activity more on them due to high engagement levels lifting their mood
                if expectations["stimulant injection"]<1:
                    expectations["stimulant injection"]=1
            elif stimulants>0 and "stimulant oral use" in expectations:
                expectations["stimulant oral use"]=round(expectations["stimulant oral use"] + (learned_change+mood_congruent_drift) * learning_rate * stimulants/(10 + stimulants), 2)
                if expectations["stimulant oral use"]<1:
                    expectations["stimulant oral use"]=1

            if typical_antipsychotics>0 and "antipsychotic injection" in expectations: # Now this will be here too so the AI updates its expectations on its antipsychotics depending on how much it is active right now, because the numbing effects can be unpleasant and affect moods
                expectations["antipsychotic injection"]=round(expectations["antipsychotic injection"] + (learned_change+mood_congruent_drift) * learning_rate * (1 - 0.47 ** typical_antipsychotics), 2) 
                if expectations["antipsychotic injection"]<1:
                    expectations["antipsychotic injection"]=1
            elif typical_antipsychotics>0 and "antipsychotic oral use" in expectations:
                expectations["antipsychotic oral use"]=round(expectations["antipsychotic oral use"] + (learned_change+mood_congruent_drift) * learning_rate * (1 - 0.47 ** typical_antipsychotics), 2)
                if expectations["antipsychotic oral use"]<1:
                    expectations["antipsychotic oral use"]=1

            if dissociatives>0 and "dissociative nasal use" in expectations:
                expectations["dissociative nasal use"]=round(expectations["dissociative nasal use"] + (learned_change+mood_congruent_drift) * learning_rate * relative_recovery**3, 2) 
                if expectations["dissociative nasal use"]<1:
                    expectations["dissociative nasal use"]=1
            elif dissociatives>0 and "dissociative oral use" in expectations:
                expectations["dissociative oral use"]=round(expectations["dissociative oral use"] + (learned_change+mood_congruent_drift) * learning_rate * relative_recovery**3, 2)
                if expectations["dissociative oral use"]<1:
                    expectations["dissociative oral use"]=1
            
           
        if delusion!="idle": # Those I actually want to show without (seconds==0 or speed_up==False) so one can count delusions/hallucinations even if speed_up==True
            if not (seconds==0 or speed_up==False):
                print(timeString)
                print(delusion)
                print("")
            else:  
                print(delusion)
        elif hallucination!="idle":
            if not (seconds==0 or speed_up==False):
                print(timeString)
                sys.stderr.write(hallucination+"\n")
                print("")
            else:
                sys.stderr.write(hallucination+"\n")
            
        if seconds==0 or speed_up==False or delusion!="idle" or hallucination!="idle":
            print("")
    else:
        print("What would you like to do?")
        print("Option 1: Toggle manual input")
        print("Option 2: Toggle details")
        print("Option 3: Show the on-going simulation")
        print("Option 4: Toggle maximum speed (additionally, manual input will be disabled and entries will only show once per minute)")
        print("Option 5: Show medication-related possible activities")
        print("Option 6: Force an instant psychotic episode")
        print("Option 7: Force an instant manic episode")
        print("Option 8: Force an instant crash from a manic episode")
        print("Option 9: Medication reset")
        print("Option 10: End the script")
        print("Option 11: Do nothing (along with any other option number)")
        
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
            SN_DA=1000
            print("Psychosis risk set to 95%!")
        elif optionChosen==7:
            if bipolar==False:
                bipolar=True
                dopamine_relative_lower_cap=0.5
                dopamine_relative_upper_cap=3
                dat_relative_lower_cap=min(0.75, dat_relative_lower_cap)
                dat_relative_upper_cap=max(1.25, dat_relative_upper_cap)
            dopamine_relative_activity=3
            dat_relative_activity=0.75
            sleep_needed=max(sleep_needed, 57600)
            print("Forced a manic episode!")
        elif optionChosen==8:
            if bipolar==False:
                bipolar=True
                dopamine_relative_lower_cap=0.5
                dopamine_relative_upper_cap=3
                dat_relative_lower_cap=min(0.75, dat_relative_lower_cap)
                dat_relative_upper_cap=max(1.25, dat_relative_upper_cap)
            dopamine_relative_activity=1
            dat_relative_activity=1.25
            tolerance=60
            acuteTolerance=60
            mood=0.1
            mood_congruent_drift=(10*mood-10)
            sleep_needed=min(sleep_needed, 28800) # This line makes sure that severe sleep deprivation doesn't instantly switch a manic agent back to mania
            print("Forced a depressive crash from a manic episode!")
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

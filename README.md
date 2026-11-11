# salience-network-basic-dopamine-simulation
It is actually partially vibe-coded and originally started due to my own curiosity. I did not plan on publishing it, but I eventually decided that if anyone has the desire to try out such, or use it for their own script, to give them the opportunity to do so. You can do whatever you want with it, no credit needed.

## Content and trigger warnings

This simulation includes topics of death, substance use, psychosis, and mental health conditions, like depression

## How to use it:

### 1. Upon running the script, you will be asked which simulation to start off with:

- default: typical values without any specific properties

- random: chooses a random simulation, including either the default one, or one of the ones I will list below right here

- Schizophrenia: this simulation makes the agent start off with weakened NMDA receptors, leading to low tonic and high phasic levels, but it also has the patient start with sensitive dopamine receptors due to adapting to the low tonic levels

- Schizoaffective Disorder Bipolar Type: same as Schizophrenia, but with the potential of Bipolar cyling

- ADHD: The agent starts off with impaired dopamine production and fast clearance, both leading to low tonic levels, but the agent also starts with slightly more sensitive receptors to adapt to the low tonic levels

- Mania: The agent starts with hyperactive dopamine production, slow clearance, and a risk of random psychotic dopamine spikes along with the already-high tonic and phasic levels
  
- Major Depressive Disorder: The agent starts off with a significantly lower baseline mood, and with lower dopamine firing rates. A small amount of receptors is also downregulated
  
- Bipolar Depression: The agent starts off manic, with high downregulation having developed as a result to previously elevated dopamine levels during mania, and after the first second of the simulation, clearance and dopamine production revert back to normal, resembling a bipolar crash, and having the agent need time for the downregulated dopamine receptors to recover

### 2. Then, each second, you will see an entry containing:

- Activity: This shows what the agent is currently doing. Every time it is about to start an activity, it has a small number of random activities to choose from, and it is capable of prioritizing activities it finds pleasant

- Engagement: This shows how engaged the mind is with the activity. High engagement does not mean automatically that the agent enjoys the on-going activity, but it does indicate that the mind of the agent is highly occupied with what they are doing or thinking right now

- Whether or not the agent is disappointed or positively surprised: If the enjoyment level of the activity deviates a lot from the expected enjoyment level, this extra line will appear

- There will also be an additional line for whenever the AI is thinking of an activity, or whenever a hallucination or a delusion has triggered

## 3. With CTRL + C, you can choose following options before the next entry:

- Toggle manual input: If this is toggled to true, you can type in what the agent does as soon as it starts a new activity, or shortly after it transitions to doing nothing. If the input is not recognized to have existing values, you will be asked how rewarding the activity is, with 50 being neutral, anything lower being unpleasant and anything higher being pleasant (for example, 80 would be highly rewarding, although you can also input absurdly high numbers like 1000 if you want to). The already-existing activities range from 2 to 95. You will also be asked how long the activity takes in seconds

- Toggle details: This toggles additional output to the entries, like
    1. how rewarding the agent expects an activity to be
    2. how rewarding it actually is for the agent
    3. if there is a likelihood for the AI of dying, which can increase depending on stimulant levels in the bloodstream but also on NMDA-related values
    4. how much nanomolar of dopamine are currently in the salience network (not substantia nigra! I am sorry for having used SN for salience network, at the time I did not know that the SN is more commonly used as a short for substantia nigra)
    5. how many mg of stimulants (based on d-amphetamine) are present in the bloodstream of the agent
    6. how many mg of dissociatives (based on ketamine, in case you are wondering, the default body weight for the agent is 70, although you can modify it in the beginning of the file) are present in the bloodstream
    7. how many mg of antipsychotics (based on haloperidol, although in the real-world, there are probably many less unpleasant alternatives) are in the bloodstream
    8. what percentage of receptors have reached chronic upregulation or downregulation, depending on the value
    9. what percentage of receptors have reached acute upregulation or downregulation
    10. what percentage of NMDA receptors, with a starting baseline of 100%, are currently active, though note that it is possible for the simulation to build more receptors over time, like due to dissociative tolerance, so values over 100% are likely normal
    11. engagement levels in percent, with levels of 80% or lower translating to "dull", levels between 81% to 90% to "unengaged", levels between 91% and 110% to "neutral", levels between 111% and 200% to "hyperfocused", and with levels between 801% and 900% often triggering a delusion, while levels of over 900% have a potential of indirectly slightly weakening NMDA receptors and often trigger a hallucination. The maximum is 1000%
    12. mood levels in percent: this modifies how pleasant the agent finds an activity to be, with 100% being the usual reward value of the activity, but it ranging from 10% (making activities much less pleasant) to 150% (making activities more pleasant). The mood changes slowly over time and are affected by engagement levels (e.g. chronic dullness leads to lower mood), NMDA activity levels, and prediction errors (e.g. when an activity is more plasant for the agent than it expected)
    13. the risk of a current psychotic-level short yet extreme dopamine spike, although the percent values don't actually match the percent per second, think of it rather as the value "between 0 and 100". NMDA activity levels are the biggest contributor to the risk of psychotic-level spikes, although slowly over time, chronically high engagement levels can also contribute to that exact risk
    14. the relative dopamine firing rate, which can adapt by lowering itself down to 50%. In a healthy individual, this firing rate can range from 50% to 100%, but conditions like Bipolar Disorder and ADHD can alter the possible range
    15. whether or not the person is experiencing a manic episode driven by Bipolar Disorder right now, and when the next episodal switch happens. The lines for these will show at the beginning of the output each second, but only if the agent has Bipolar Disorder or Schizoaffective Disorder Bipolar Type
 
 - Show the on-going simulation: This shows the name in caps of the simulation profile that the current simulation started with

 - Toggle maximum speed: Toggling this to true will make the script run as fast as it can instead of the real-time speed. The output still shows one new entry per second. I made it so toggling this option will disable the manual input option for my own convenience, although feel free to modify the file if you do not like that

 - End the script: Choosing this option simply ends the script

 - Show medication-related activities: Choosing this will show a list of activities that are related to stimulants, antipsychotics, and dissociatives

 - Force a psychotic episode: This will increase the risk of a psychotic-level spike to 95%, although it can drop quickly depending on the condition of the agent

 - Force a manic episode: If the agent is not in a manic episode driven by Bipolar Disorder already, it will shift towards mania. If the agent does not have Bipolar Disorder, choosing this option will also lead to the agent having it from that point

 - Medication reset: This instantly clears all stimulants, antipsychotics and dissociatives from the body

 - Do nothing: This option just lets the script continue running

## 4. Additional notes

- Once you have the file on your local device, you can republish it, modify it, test it, use it as a tool for your own project, or do whatever else you can think of. You do not have to credit me at all, although if you do attempt modifying the script, I can imagine it being a bit difficult because of my messy structure and limited programming skills. I wish you to have fun regardless!

- In the IDE I use, a delusion has the standard, in my case, blue, font color while a hallucination has a red font. How they will look like for you will depend on the IDE, and it is possible for some not to separate the font colors between those two at all, although by the content of the message, and, if details have been toggled to true, you can also tell by checking the engagement levels in percent (if they are over 900%, it is a hallucination)

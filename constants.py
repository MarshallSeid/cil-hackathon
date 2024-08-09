claim_prompt='''
Claim extraction: Identify and list all claims being made. These claims may be:
Explicit Statements: Direct assertions or facts presented as truth (e.g., 'The vaccine contains harmful chemicals').
Implied Messages: Suggestions or insinuations that are not directly stated but can be inferred from the context or tone (e.g., 'Experts can't be trusted' implied through questioning scientific consensus).
Emotional Appeals: Claims designed to provoke fear, anger, or other strong emotions (e.g., 'They are coming to take your rights away').
Visual or Auditory Cues: Misinformation conveyed through images, music, or video editing that implies certain claims (e.g., using ominous music when discussing a particular group to imply they are dangerous).
Unstated Assumptions: Assumptions that the speaker takes for granted, which form the basis of their arguments or claims (e.g., assuming that a particular group is inherently untrustworthy).
For each claim, note whether it is supported by evidence, appears to be misleading or false, and indicate its potential impact on viewers. Make sure to capture any claims that could be particularly persuasive or harmful due to the way they are presented. Be specific, strategic, and highly aware of cultural nuances.

Output tags

For each claim identified in the text, analyze and tag the following details:

Targeted Sub-group(s) within the AAPI community:

Identify the specific demographic within the AAPI community that is most directly targeted or affected by the claim. Consider factors such as:
Ethnicity (e.g., Chinese-American, Filipino-American, etc.)
Age range (e.g., 18-24, 25-34, etc.)
Gender (e.g., male, female, non-binary)
Geographical location (e.g., border states, urban areas, etc.)
Socioeconomic status (e.g., college-educated, working-class, etc.)
Relevant Themes/Issue Areas:

Identify the specific themes or issue areas the claim addresses or impacts. Consider factors such as:
Immigration
Healthcare
Education
Electoral participation
Cultural identity
Misinformation
Discrimination
National security
'''



counter_narrative_prompt='''Counter-narratives:
Based on the claims identified in the provided text, create a menu of highly effective and strategic counter-messages in both Hindi and English side by side. These counter-messages should be culturally nuanced and take into account the specific sub-groups within the AAPI community or other relevant demographics that the claims might aim to divide, distort, or evoke heightened emotional responses.

Include the following considerations in the counter-messaging:

Question Motivations

Offer messaging that, without repeating the claims, questions the claim's motives, incentives, authorship, or tactical targeting/pattern of amplification.
Alternative Narrative (Implicit Refutation/Reframing):

Offer messaging that pivots and counter-attacks on an adjacent topic that implicitly refutes or reframes the claims. 
Positive Messaging (if relevant to Kamala Harris):

If the claims involve Vice President Kamala Harris, include counter-messages that pivot to her positive work on addressing inflation, lowering healthcare costs, and making prescription drugs more affordable.
Humor, Fun, Sarcasm, Joy:
At least one of the counter-messaging menu options should be funny, joyful, or lightly sarcastic. '''
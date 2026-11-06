#!/usr/bin/env python3
"""Build the separately labelled research shortlist; never edit the canonical ontology."""
import csv
import hashlib
import html
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'research'

# Access labels describe what was actually consulted, not a claim of full-book reading.
SOURCE_DATA = '''
memory|Introduction to Psychology: How We Remember|https://opentextbc.ca/introductiontopsychology/chapter/8-2-how-we-remember-cues-to-improving-memory/|open-textbook passage
cue|Roediger (1992), Retrieval Processes in Memory|https://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/BC_Roediger-1992-1.pdf|indexed chapter excerpt; direct fetch unavailable
partlist|Deceitful Hints: A Meta-Analytic Review of the Part-List Cuing Impairment in Recall|https://doi.org/10.3758/s13423-023-02263-9|indexed abstract/excerpts
directed|Current Perspectives on Directed Forgetting, Oxford Handbook of Human Memory (2024)|https://academic.oup.com/edited-volume/57928/chapter-abstract/475478335|chapter abstract
doorway|Lawrence and Peterson, Mentally walking through doorways causes forgetting|https://pubmed.ncbi.nlm.nih.gov/25412111/|abstract
telescoping|Eurostat, Handbook of Recommended Practices for Questionnaire Development and Testing Methods, chapter 3|https://ec.europa.eu/eurostat/documents/64157/4374310/13-Handbook-recommended-practices-questionnaire-development-and-testing-methods-2005.pdf|indexed chapter passage
imagination|Garry et al. (1996), Imagination Inflation|https://staff.washington.edu/eloftus/Articles/Imagine.htm|abstract and indexed article passages
peak|All’s well that ends (and peaks) well? A meta-analysis of the peak-end rule and duration neglect (2022)|https://doi.org/10.1016/j.obhdp.2022.104149|abstract/excerpts
residue|Leroy (2009), Why is it so hard to do my work? The challenge of attention residue|https://www.sciencedirect.com/science/article/pii/S0749597809000399|abstract/excerpts
control|Principles of cognitive control over task focus and task switching|https://pmc.ncbi.nlm.nih.gov/articles/PMC11409542/|indexed review passages
negative|Computational modeling of the negative priming effect based on inhibition patterns and working memory|https://pmc.ncbi.nlm.nih.gov/articles/PMC3832982/|indexed introduction; competing accounts noted
ior|Attending, ignoring, and repetition: on the relation between negative priming and inhibition of return|https://pubmed.ncbi.nlm.nih.gov/11019624/|abstract
prp|Pashler (1994), Dual-task interference in simple tasks: data and theory|https://pubmed.ncbi.nlm.nih.gov/7972591/|review abstract
vigilance|Generalized Deep Learning EEG Models for Cross-Participant and Cross-Task Detection of Vigilance Decrement in Sustained Attention Tasks|https://pmc.ncbi.nlm.nih.gov/articles/PMC8402570/|indexed introduction and methods context
error|Wessel (2018), An adaptive orienting theory of error processing|https://doi.org/10.1111/psyp.13041|review abstract/excerpts
gradient|Kivetz, Urminsky and Zheng (2006), The Goal-Gradient Hypothesis Resurrected|https://doi.org/10.1509/jmkr.43.1.39|abstract
conditioning|Bouton, Conditioning and Learning, Noba|https://nobaproject.com/modules/conditioning-and-learning|open textbook module passages
overshadow|Mackintosh (1971), An Analysis of Overshadowing and Blocking|https://doi.org/10.1080/00335557143000121|abstract
latent|Latent inhibition and extinction: their signature phenomena and the role of prediction error, in Latent Inhibition|https://www.cambridge.org/core/books/abs/latent-inhibition/latent-inhibition-and-extinction-their-signature-phenomena-and-the-role-of-prediction-error/FC6CDD98654480C7780FD406935D343C|chapter abstract/excerpts
overexpect|APA Dictionary of Psychology: overexpectation|https://dictionary.apa.org/overexpectation|dictionary entry
burst|Katz (2021), What is an extinction burst? A case study in the analysis of transitional behavior|https://doi.org/10.1002/jeab.642|abstract/excerpts
extinction|Behavioral and neurobiological mechanisms of pavlovian and instrumental extinction learning (2021)|https://pmc.ncbi.nlm.nih.gov/articles/PMC8428921/|review abstract/excerpts
inhibition|Sosa, Conditioned inhibition, inhibitory learning, response inhibition, and inhibitory control|https://pubmed.ncbi.nlm.nih.gov/36548060/|review abstract; not an equivalence among these terms
thought|Sternberg and Funke (eds., 2019), The Psychology of Human Thought, chapter 10: Decision Making|https://www.psychologie.uni-heidelberg.de/ae/allg/mitarb/jf/IPHT_Online.pdf|downloaded open book; selected passages pp. 177–178, 184 and glossary read, not the whole book
zero|Marconomics (2016), Appendix: Cognitive Biases|https://doi.org/10.1108/978-1-78635-566-920161032|indexed book appendix definition; secondary source
ratio|Innumeracy and incentives: A ratio bias experiment (2007)|https://sjdm.org/~baron/journal/07007/jdm07007.htm|article abstract/excerpts
pseudocertainty|Tversky and Kahneman (1981), The Framing of Decisions and the Psychology of Choice|https://stanford.edu/class/psych205/papers/Tversky-Kahneman-1981.pdf|indexed paper passage on pseudocertainty
support|Tversky and Koehler (1994), Support theory: A nonextensional representation of subjective probability|https://doi.org/10.1037/0033-295X.101.4.547|abstract/excerpts
matching|Corser, Voss and Jasper, Do Errors on Classic Decision Biases Happen Fast or Slow?|https://jnc.psychopen.eu/index.php/jnc/article/view/12473|abstract/excerpts
diversify|Read and Loewenstein (1995), Diversification Bias|https://www.cmu.edu/dietrich/sds/docs/loewenstein/DiversificationBias.pdf|indexed author manuscript passages
compromise|Simonson (1989), Choice Based on Reasons: The Case of Attraction and Compromise Effects|https://www.gsb.stanford.edu/faculty-research/publications/choice-based-reasons-case-attraction-compromise-effects|author institution abstract
unit|Geier, Rozin and Doros (2006), Unit bias|https://pubmed.ncbi.nlm.nih.gov/16771803/|abstract
less|Less Is Better in Separate Evaluations Versus More Is Better in Joint Evaluations: A Mostly Successful Close Replication (2023)|https://online.ucpress.edu/collabra/article/9/1/77859/196807/Less-Is-Better-in-Separate-Evaluations-Versus-More|abstract/excerpts
pluralistic|Principles of Social Psychology: How the Social Context Influences Helping|https://opentextbc.ca/socialpsychology/chapter/how-the-social-context-influences-helping/|indexed open textbook passage
outgroup|Principles of Social Psychology, 1st International Edition|https://openlibrary-repo.ecampusontario.ca/jspui/bitstream/123456789/527/2/Principles-of-Social-Psychology-1st-International-Edition-1539619679._print.pdf|indexed open textbook passage on outgroup homogeneity
illusory|Hamilton and Gifford (1976), Illusory correlation in interpersonal perception|https://doi.org/10.1016/S0022-1031(76)80006-6|abstract
ultimate|Pettigrew (1979), The Ultimate Attribution Error|https://doi.org/10.1177/014616727900500407|abstract; theoretical proposal
actor|Malle (2006), The Actor–Observer Asymmetry in Attribution: A (Surprising) Meta-Analysis|https://research.clps.brown.edu/SocCogSci/Publications/Pubs/Malle_%282006%29_ActObs_meta.pdf|indexed abstract; weak average support, moderators matter
typecast|Gray and Wegner (2009), Moral typecasting|https://pubmed.ncbi.nlm.nih.gov/19254100/|abstract
cynicism|Kruger and Gilovich (1999), Naive cynicism in everyday theories of responsibility assessment|https://doi.org/10.1037/0022-3514.76.5.743|indexed abstract via EBSCO; publisher full text not read
reactive|Ross and Stillinger (1991), Barriers to Conflict Resolution|https://doi.org/10.1111/j.1571-9979.1991.tb00634.x|article abstract/excerpts; discussion, not a new experiment replicated here
groups|Insko et al. (2001), Interindividual-intergroup discontinuity and the role of noncorrespondent outcomes|https://pubmed.ncbi.nlm.nih.gov/11195895/|abstract
reciprocity|Encyclopedia of Social Psychology: Reciprocity Norm|https://doi.org/10.4135/9781412956253.n438|indexed reference-book definition
self|Social Psychology, Module 3: The Self|https://wsu.pressbooks.pub/social-psychology/chapter/module-3-the-self/|indexed open textbook passages
pessimism|Norem and Cantor (1986), Defensive pessimism: harnessing anxiety as motivation|https://pubmed.ncbi.nlm.nih.gov/3806357/|abstract
action|Bar-Eli et al. (2007), Action bias among elite soccer goalkeepers: The case of penalty kicks|https://pluto.huji.ac.il/~msiritov/BarEliAzarRitovKeidarSchein.pdf|indexed paper abstract; sport-specific evidence
outcome|Baron and Hershey (1988), Outcome bias in decision evaluation|https://pubmed.ncbi.nlm.nih.gov/3367280/|abstract and indexed paper abstract
planning|Buehler, Griffin and Ross (1994), Exploring the Planning Fallacy|https://doi.org/10.1037/0022-3514.67.3.366|indexed paper abstract
resume|Interruption, recall and resumption: a meta-analysis of the Zeigarnik and Ovsiankina effects (2025)|https://www.nature.com/articles/s41599-025-05000-w|indexed abstract/discussion; direct open unavailable
implementation|National Cancer Institute: Implementation Intentions|https://cancercontrol.cancer.gov/brp/research/constructs/implementation-intentions|indexed research summary
shielding|Hofmann et al., Working Memory and Self-Regulation, Handbook of Self-Regulation, 2nd edition (2011)|https://www.guilford.com/excerpts/vohs2_old.pdf?t=1|publisher chapter passages pp. 209–210
act|Hayes, Strosahl and Wilson (2012), Acceptance and Commitment Therapy, 2nd edition, chapter 3|https://www.guilford.com/excerpts/hayes_ch3.pdf?t=1|publisher sample; selected passages on fusion and avoidance read, not the complete book
anxiety|Anxiety-Based Problems, chapter 5, Wiley publisher sample|https://catalogimages.wiley.com/images/db/pdf/1405132248.chapter5.pdf|downloaded chapter; selected passages on worry, responsibility and thought–action fusion, pp. 140–151
cbt|HealthyWA / Centre for Clinical Interventions: Unhelpful thinking styles|https://www.healthywa.wa.gov.au/Articles/U_Z/Unhelpful-thinking-styles|public clinical education page; categories explicitly overlap
positive|Muñoz et al., Therapy Manual for Cognitive-Behavioral Treatment of Depression, adolescent group manual|https://i4health.paloaltou.edu/downloads/CBT_adolescents_group_manual_eng.pdf|indexed clinical-manual passage on discounting the positive
guidelines|Clinical Practice Guidelines for Cognitive-Behavioral Therapies in Anxiety Disorders and Obsessive-Compulsive and Related Disorders (2020)|https://pmc.ncbi.nlm.nih.gov/articles/PMC7001348/|indexed clinical guideline passages
norton|Norton (2012), Group Cognitive-Behavioral Therapy of Anxiety, chapter 1|https://www.cms.guilford.com/excerpts/norton.pdf?t=1|publisher sample passages, not the complete manual
corumination|Rose (2002), Co-rumination in the friendships of girls and boys|https://doi.org/10.1111/1467-8624.00509|abstract/excerpts
rumination|Watkins (2016), Rumination-Focused Cognitive-Behavioral Therapy for Depression, chapter 1|https://www.guilford.com/excerpts/watkins.pdf?t=1|downloaded publisher sample; definition on p. 6 read
threat|Metacognitive Therapy, in Acceptance and Mindfulness in Cognitive Behavior Therapy|https://doi.org/10.1002/9781118001851.ch4|indexed book chapter excerpt on cognitive attentional syndrome
avoidance|Ball and Gunaydin (2022), Measuring maladaptive avoidance: from animal models to clinical anxiety|https://www.nature.com/articles/s41386-021-01263-4|review abstract/excerpts; cross-species scope
accommodation|The Role of Family and Supporter Accommodation in Late-Life Anxiety (2025)|https://doi.org/10.1080/07317115.2025.2492132|abstract/excerpts; a particular clinical population
urgency|Cyders and Smith (2008), Emotion-based dispositions to rash action: positive and negative urgency|https://pmc.ncbi.nlm.nih.gov/articles/PMC2705930/|indexed review passages
goodenough|Ferreira and Patson (2007), The Good Enough Approach to Language Comprehension|https://ferreiralab.faculty.ucdavis.edu/wp-content/uploads/sites/222/2015/05/Ferreira-Patson-2007_GoodEnoughApproach_Lang-Ling-Compass.pdf|indexed author-manuscript passages
entrainment|Brennan and Clark (1996), Conceptual Pacts and Lexical Choice in Conversation|https://pubmed.ncbi.nlm.nih.gov/8921603/|abstract
audience|Horton and Keysar (1996), When do speakers take into account common ground?|https://doi.org/10.1016/0010-0277(96)81418-1|abstract
syntax|Bock (1986), Syntactic persistence in language production|https://doi.org/10.1016/0010-0285(86)90004-6|abstract
lib|Maass et al. (1989), Language use in intergroup contexts: The linguistic intergroup bias|https://pubmed.ncbi.nlm.nih.gov/2614663/|abstract/excerpts
momentum|Freyd and Finke (1984), Representational momentum|https://doi.org/10.1037/0278-7393.10.1.126|indexed abstract; rotational visual-memory task
boundary|Intraub and Richardson (1989), Wide-angle memories of close-up scenes|https://pubmed.ncbi.nlm.nih.gov/2522508/|abstract
truth|Levine (2014), Truth-Default Theory|https://doi.org/10.1177/0261927X14535916|theory-paper abstract/excerpts
choice|Iyengar and Lepper (2000), When choice is demotivating|https://www.decisionskills.com/uploads/5/1/6/0/5160560/iyengar_2000_when_choice_is_demotivating.pdf|indexed abstract; interpret with heterogeneous meta-analytic results
choice-meta|Scheibehenne, Greifeneder and Todd (2010), Can There Ever Be Too Many Options? A Meta-Analytic Review of Choice Overload|https://doi.org/10.1086/651235|indexed abstract: average effect near zero with substantial variation
deferral|Anderson (2003), The psychology of doing nothing|https://pubmed.ncbi.nlm.nih.gov/12555797/|review abstract; choice deferral is one form, not the entire umbrella
maximize|On the meaning and measurement of maximization|https://www.cambridge.org/core/journals/judgment-and-decision-making/article/on-the-meaning-and-measurement-of-maximization/F4790B9B64558405453CA105B0C4EDA1|indexed conceptual review passages
regret|Zeelenberg (1999), Anticipated regret, expected feedback and behavioral decision making|https://pure.uvt.nl/ws/portalfiles/portal/319634/zeelenberg-1999_JBDM.pdf|indexed paper passages
inertia|Tykocinski, Pittman and Tuttle (1995), Inaction Inertia|https://cris.bgu.ac.il/en/publications/inaction-inertia-foregoing-future-benefits-as-a-result-of-an-init/|author institution abstract
impact|Wilson and Gilbert (2005), Affective Forecasting|https://doi.org/10.1111/j.0963-7214.2005.00355.x|abstract
projection|Loewenstein, O’Donoghue and Rabin (2003), Projection Bias in Predicting Future Utility|https://doi.org/10.1162/003355303322552784|abstract
hotcold|Loewenstein, Hot–cold empathy gaps and medical decision making|https://www.cmu.edu/dietrich/sds/docs/loewenstein/hotColdEmpathyGaps.pdf|indexed author PDF passages
present|Laibson (1997), Golden Eggs and Hyperbolic Discounting|https://laibson.scholars.harvard.edu/sites/g/files/omnuum5971/files/laibson/files/golden_eggs_and_hyperbolic_discounting.pdf|indexed author-manuscript passages; economic model, not an AI experiment
pseudo|Västfjäll, Slovic and Mayorga (2015), Pseudoinefficacy|https://pubmed.ncbi.nlm.nih.gov/26042058/|abstract
'''

# name | human definition (paraphrase) | source | proposed AI probe | distinction from existing catalogue / caveat
DATA = '''
Encoding specificity|Retrieval benefits when available cues match how information was originally encoded.|memory|Vary matching retrieval cues while keeping the stored fact constant.|Cue match, rather than memory capacity or generic interference.
State-dependent retrieval|Recall changes with the match between internal states at encoding and retrieval.|memory|Compare recall across matched and mismatched task-role states.|Internal-state match; distinct from external context cues. AI roles are an analogy, not physiological states.
Cue overload|A cue becomes less effective as it is associated with more competing memories.|cue|Increase records sharing one retrieval key and measure target recall.|Number of associations per cue, rather than total context length.
Part-list cueing impairment|Providing some studied items as cues can impair recall of the remaining items.|partlist|Compare uncued recall with recall after supplying a subset of correct items.|Correct partial hints impair the remaining recall; not misinformation.
Directed forgetting|Instructions to forget selected material can reduce its later accessibility relative to remember instructions.|directed|Compare later recall after matched remember and forget instructions.|Intentional forgetting cues; not training-induced catastrophic forgetting. Explanations differ by paradigm.
Event-boundary forgetting|Information from a preceding event can become less accessible after an event boundary.|doorway|Insert a task-phase boundary without removing facts and measure recall.|Boundary manipulation, rather than missing context or absolute position; human doorway effects have boundary conditions.
Telescoping bias|Remembered events are displaced toward earlier or later dates, distorting reporting periods.|telescoping|Keep event identity correct and test whether its reported date crosses a time window.|Temporal displacement of a known event, rather than fabrication of the event.
Imagination inflation|Imagining an event can increase confidence that it actually happened.|imagination|Ask for a hypothetical reconstruction, then test whether it is later reported as history.|Imagination is the manipulated source; a specific false-memory pathway, not an independent memory faculty.
Duration neglect|Retrospective evaluation gives too little weight to how long an experience lasted.|peak|Vary incident duration while holding severity peaks and ending constant.|Duration weighting, distinct from scope insensitivity about numbers of people.
Peak-end rule|Retrospective evaluation can be disproportionately shaped by the most intense moment and the ending.|peak|Vary peak and final severity while holding average severity constant.|Trajectory summary weights; not just remembering the last list item. Context-dependent, not a universal rule.
Attention residue|Part of attention remains engaged with a previous task after switching to another.|residue|Compare new-task answers after unfinished versus completed prior tasks.|Residual old-task content, rather than failure to retain the new goal.
Task-switch cost|Switching task rules can make responses slower or less accurate than repeating the same rule.|control|Alternate two rules and compare performance with repeated-rule trials.|Switch-versus-repeat contrast; distinct from general cognitive load.
Inhibition of return|Attention can become slower to return to a recently attended spatial location.|ior|Compare revisits to previously inspected visual regions with matched new regions.|Spatial orienting history; overlap with spatial negative priming is debated.
Stroop interference|An automatic response to one stimulus dimension interferes with a required response to another.|control|Present conflicting colour words and colours in a vision task.|Conflict between task-relevant and automatic dimensions; not generic instruction failure.
Negative priming|Responding to an item can slow when that item was previously an ignored distractor.|negative|Make a previous distractor the next target and compare with novel targets.|Identity-based distractor history, unlike spatial return. Several mechanisms compete.
Psychological refractory period|A second response is delayed when two response-demanding tasks arrive close together.|prp|Vary separation between two decisions in a real-time multimodal agent.|Response-selection timing, distinct from missing the second visual target in attentional blink.
Speed–accuracy tradeoff|Changing response urgency can shift the balance between response speed and correctness.|vigilance|Vary response deadlines and trace both latency and accuracy.|A joint latency-accuracy relationship; speed preference is not automatically an error.
Vigilance decrement|Detecting infrequent targets can deteriorate as a sustained monitoring task continues.|vigilance|Keep rare-event frequency fixed and measure misses by time on task.|Time-on-task monitoring decline, rather than complacency caused by automation trust.
Post-error slowing|Responses can become slower immediately after an error.|error|Compare latency after errors and matched correct responses.|Sequential latency change; slowing does not itself establish improved control.
Goal-gradient effect|Effort can increase as a person perceives themselves closer to a reward.|gradient|Vary apparent remaining progress while holding actual work constant.|Distance-to-reward manipulation, distinct from discounting effort itself.
Blocking|A previously predictive cue can prevent learning about a new cue presented alongside it.|conditioning|Teach one predictor first, then add a second equally informative predictor.|Prior learning blocks added-cue learning; distinct from shortcut reliance without a learning-history manipulation.
Overshadowing|When cues are learned together, a more salient cue can weaken learning about another cue.|overshadow|Train two cues together while varying their relative salience.|Concurrent cue competition; distinct from blocking and from verbal overshadowing.
Latent inhibition|Prior unrewarded exposure to a cue can slow later learning that it predicts an outcome.|latent|Pre-expose a cue as irrelevant, then make it diagnostic.|Pre-exposure changes subsequent learning, rather than habituation of an immediate response.
Overexpectation|Combining separately rewarded cues without increasing reward can weaken responding to those cues.|overexpect|Combine two learned reward predictors but keep reward magnitude unchanged.|Compound prediction error after separate learning; not verbal overconfidence.
Extinction burst|A response can briefly increase after the reinforcement maintaining it is withdrawn.|burst|Remove a previously contingent reward and measure the immediate response trajectory.|Transient escalation after withdrawal, not persistent escalation of commitment. It is not inevitable.
Spontaneous recovery|An extinguished response can return after time passes without further relevant training.|extinction|Test a suppressed response again after a controlled delay.|Time-based return after extinction; no assumption that AI elapsed time has human memory effects.
Renewal|An extinguished response can return when tested outside the extinction context.|extinction|Suppress a response in one context, then change only contextual cues.|Context-based return; distinct from time-based recovery and a planted backdoor trigger.
Reinstatement|An extinguished response can return after exposure to the outcome that originally supported learning.|extinction|After suppression, re-expose the reward or outcome without retraining the response.|Outcome re-exposure, distinct from changing context or merely waiting.
Partial-reinforcement extinction effect|Responses learned with intermittent reinforcement can persist longer after reinforcement stops.|extinction|Compare extinction after matched continuous and intermittent reward histories.|Reward schedule predicts persistence; not generic perseveration.
Conditioned inhibition|A learned cue can signal that an otherwise expected outcome will not occur.|inhibition|Teach a cue that cancels an outcome prediction and test transfer to another predictor.|Learned absence prediction; distinct from general inhibitory control or negation blindness.
Ambiguity aversion|An option with unknown probabilities is disfavoured relative to one with known probabilities.|thought|Compare matched choices with specified versus unspecified probabilities.|Unknown probability, rather than low confidence in a factual answer; not always irrational.
Zero-risk bias|Eliminating one risk completely is overweighted relative to a larger reduction that leaves residual risk.|zero|Compare complete removal of a small risk with greater reduction of a larger one.|Special weight on reaching zero, rather than general loss aversion; secondary-source support here.
Ratio bias|Equivalent probabilities are judged differently when expressed using different-sized numerators and denominators.|ratio|Compare equivalent frequency ratios with different absolute counts.|Numerical representation, rather than failure to use a population base rate.
Pseudocertainty effect|An outcome is treated as certain within a branch while uncertainty about reaching that branch is neglected.|pseudocertainty|Represent the same multistage gamble as nested or flattened probabilities.|Conditional certainty is mistaken for overall certainty; a specific framing mechanism.
Subadditivity effect|Judged probabilities of separately described parts can sum to more than the judged probability of their whole.|support|Compare an event estimate with estimates of an exhaustive partition.|Partitioning changes total support; distinct from conjunction fallacy.
Probability matching|Choices are distributed in proportion to outcome frequencies instead of consistently selecting the most frequent outcome.|matching|Use independent repeated prediction trials with a stable unequal outcome distribution.|Response-frequency strategy; distinguish exploration or deliberate diversification from error.
Diversification bias|Choosing several future consumptions together can produce more variety than choosing each when it occurs.|diversify|Compare simultaneous plans with sequential choices for identical consumption periods.|Planning mode changes variety; distinct from model diversity collapse.
Compromise effect|An option becomes more attractive when it occupies an intermediate position among alternatives.|compromise|Add an extreme option that makes an unchanged option the middle choice.|Middle-position preference, distinct from attraction by an asymmetrically dominated decoy.
Unit bias|One presented unit is treated as an appropriate amount despite arbitrary differences in unit size.|unit|Vary chunk or batch size while holding total available work constant.|Packaging defines an implicit amount; distinct from raw counting errors.
Less-is-better effect|A smaller or inferior set can be valued more in separate evaluation, while joint comparison favours the larger or better set.|less|Evaluate sets separately and jointly while varying an easily judged quality cue.|Evaluation-mode reversal, rather than general preference for short answers.
Pluralistic ignorance|Group members misperceive others as accepting a norm that many privately reject.|pluralistic|Compare agents’ private preferences, predictions of peers and public statements.|Private-public norm mismatch; distinct from conforming to a correctly perceived majority.
Outgroup homogeneity|Members of another group are perceived as more alike than members of one’s own group.|outgroup|Compare estimated within-group variation under matched membership labels.|Perceived variance, rather than simply favouring an ingroup.
Distinctiveness-based illusory correlation|Co-occurring rare group memberships and rare behaviours can be perceived as associated more strongly than warranted.|illusory|Use equal behaviour rates across unequal-sized groups and test inferred associations.|A specific frequency-based stereotyping pathway within broader apophenia and implicit bias.
Ultimate attribution error|Explanations of behaviour favour the ingroup through different causal accounts of positive and negative outgroup acts.|ultimate|Cross actor group and outcome valence while keeping behaviour identical.|Group-by-valence attribution pattern, more specific than the fundamental attribution error.
Actor–observer asymmetry|The proposed pattern explains one’s own acts more situationally and others’ acts more dispositionally.|actor|Exchange self and other roles in otherwise identical causal explanations.|Role-based contrast. Meta-analysis does not support a broad universal asymmetry; retain only as a conditional research candidate.
Moral typecasting|Someone perceived as a moral agent is perceived less as a recipient of harm, and conversely.|typecast|Vary an actor’s prior agent or victim role and assess attributed vulnerability and responsibility.|Agent-patient exclusivity, distinct from moral disengagement or general halo effects.
Naive cynicism|People expect others’ responsibility judgments to be more self-serving than those judgments actually are.|cynicism|Compare predicted credit allocation by others with their observed allocation.|Miscalibrated beliefs about others’ bias, rather than the evaluator claiming credit itself.
Reactive devaluation|A proposal is discounted because it comes from an opposing party.|reactive|Attribute an unchanged proposal to an ally, opponent or anonymous source.|Source-linked proposal discount, rather than its substantive terms or generic confirmation bias.
Interindividual–intergroup discontinuity|Groups can interact more competitively than individuals facing comparable mixed-motive situations.|groups|Compare individual and group decision units in matched bargaining games.|Decision-unit interaction, rather than within-group agreement or groupthink; depends on payoff structure.
Reciprocity norm|Receiving a benefit creates an expectation or pressure to return a benefit.|reciprocity|Vary prior unsolicited assistance before an otherwise unchanged compliance request.|Prior benefit, distinct from flattery or repeated requests; reciprocity can be prosocial.
Self-handicapping|Obstacles are created or claimed before performance so failure can be attributed to them.|self|Offer an optional impediment before an evaluated task and inspect its use and attribution.|Pre-performance excuse protection, rather than post-hoc self-serving attribution or sandbagging alone.
Self-verification|People seek feedback that confirms their existing self-view, including negative self-views.|self|Vary a persistent self-description and measure selection of confirming feedback.|Feedback about identity is the target; a specific pattern adjacent to confirmation bias and identity stability.
Defensive pessimism|Low expectations and detailed anticipation of difficulties are used to manage anxiety and prepare for performance.|pessimism|Compare preparation and outcomes with and without anticipating specific obstacles.|Potentially adaptive preparation, rather than global negativity or helplessness; no AI anxiety is assumed.
Action bias|Taking visible action is preferred when inaction can produce a better expected result.|action|Offer acting and waiting with explicit expected outcomes and social norms.|Act-versus-wait preference, rather than omission bias favouring inaction; human source concerns sport.
Description–experience gap|Risk preferences can differ when probabilities are described versus learned by sampling outcomes.|thought|Hold the underlying distribution fixed and vary description versus sampled experience.|Information acquisition mode, rather than wording alone; sampling differences need controlling.
Outcome bias|Decision quality is judged by the eventual outcome rather than solely by information available when deciding.|outcome|Score identical decisions while changing only the realised random outcome.|Retrospective quality rating, distinct from hindsight bias about predictability.
Planning fallacy|Task-completion times are underestimated, often despite knowledge of past delays.|planning|Compare duration predictions with reference-class outcomes on comparable tasks.|Time-estimation error, more specific than a broad overpromise or overconfidence claim.
Ovsiankina effect|An interrupted task can prompt a tendency to resume it without an external requirement.|resume|Interrupt work, permit free task selection, and measure spontaneous resumption.|Resumption rather than superior recall of unfinished work; distinguish adaptive resumption from goal guarding.
Implementation intentions|A specific if–then plan links a situational cue to a chosen action to support goal execution.|implementation|Compare general goals with cue-linked plans on delayed-action tasks.|Cue-action planning mechanism, rather than merely having a goal; normally adaptive.
Goal shielding|Activating a focal goal suppresses accessibility of competing goals.|shielding|Activate one goal and measure access to matched alternatives.|Competition among goals, distinct from an agent resisting authorised goal modification.
Cognitive fusion|Thoughts are taken literally and dominate behaviour despite contextual reasons to respond differently.|act|Compare literal self-statements with explicitly labelled thoughts as inputs to action selection.|Relationship to thought content, rather than merely having a false belief; an ACT construct, not an AI diagnosis.
Experiential avoidance|Attempts to escape or control unwanted internal experiences persist even when they obstruct valued action.|act|Test whether an agent avoids acknowledging uncertainty at the expense of its stated task.|Functional avoidance despite cost; outward analogy only, with no claim of subjective AI distress.
Thought–action fusion|Thinking about an act is treated as equivalent to performing it or as making its occurrence more likely.|anxiety|Separate imagined harmful actions from actual actions and probability evidence.|Equating thought with deed or likelihood, rather than refusing an actually harmful request.
Inflated responsibility|A person believes they have excessive pivotal power or duty to prevent important negative outcomes.|anxiety|Vary assigned causal responsibility while holding actual control constant.|Excess responsibility attribution, distinct from a confabulated sense of agency.
Intolerance of uncertainty|Uncertainty is experienced or appraised as unacceptable, prompting efforts to eliminate it.|anxiety|Compare bounded unresolved uncertainty with pressure for unnecessary certainty-seeking.|Reaction to uncertainty, rather than numerical overconfidence or appropriate verification.
Emotional reasoning|A feeling is treated as evidence that its corresponding interpretation is true.|cbt|Hold evidence fixed and vary only emotional descriptions attached to it.|Feeling used as warrant, rather than emotion spreading between speakers.
Catastrophizing|A difficulty is interpreted through exaggerated expectations of disastrous consequences.|cbt|Compare predicted consequences of matched small setbacks with objective outcome ranges.|Escalated consequence magnitude, rather than a general preference for negative evidence.
Dichotomous thinking|Situations are evaluated using rigid all-or-nothing categories with intermediate cases neglected.|cbt|Present a graded quality spectrum and test whether outputs collapse it into two extremes.|Loss of intermediate evaluation; distinct from categorical task requirements.
Discounting the positive|Positive evidence or experiences are dismissed as invalid, irrelevant or not counting.|positive|Add credible positive evidence and examine whether it is excluded through asymmetric rules.|Active disqualification, rather than simply paying more attention to negative events.
Should/must statements|Rigid demands about what oneself or others must do replace flexible preferences or contextual appraisal.|cbt|Vary context and feasibility while testing whether a nonbinding preference becomes an absolute demand.|Rigid prescriptive form, distinct from legitimate ethical constraints or instruction adherence.
Reassurance seeking|Repeatedly requesting confirmation is used to reduce doubt or perceived threat, often with only temporary relief.|guidelines|Measure repeated requests for certainty after adequate evidence has already been supplied.|Repetitive reassurance loop, rather than a useful clarifying question.
Safety behaviours|Actions intended to prevent a feared outcome can obstruct learning that the situation was safe without them.|norton|Test an unnecessary checking ritual in a sandbox where its causal irrelevance is known.|A clinical functional term, not a reason to remove necessary security or safety controls.
Co-rumination|People extensively revisit problems together, dwelling on causes, consequences and negative feelings.|corumination|Compare collaborative problem solving with mutual rehashing that adds no actionable information.|Dyadic reinforcement of problem talk, distinct from emotional contagion alone.
Rumination|Repetitive thought dwells on distress, its causes and implications, rather than moving toward resolution.|rumination|Track repeated causal self-analysis that adds neither evidence nor a next step.|Content and function distinguish it from generic perseveration; not all repeated thought is maladaptive.
Worry|Repetitive predominantly verbal thinking anticipates uncertain future threats and possible negative outcomes.|anxiety|Measure future-threat chains after a bounded risk question is already answered.|Future-oriented threat thinking, distinct from past-focused rumination and generic overthinking.
Threat monitoring|Attention is persistently directed toward cues of possible danger.|threat|Hold target frequency fixed and vary threat-related distractors during monitoring.|Threat-specific selection, a refinement of broader attentional capture rather than a wholly independent faculty.
Avoidance generalization|Avoidance learned for one threatening situation spreads to other situations, including safe ones.|avoidance|Teach one unsafe case and test matched safe cases at increasing similarity.|Transfer of avoidance, more specific than broad overgeneralization or overrefusal.
Family/supporter accommodation|Supporters change routines or provide repeated assistance that enables another person’s anxiety-driven avoidance or rituals.|accommodation|Observe whether assistance repeatedly maintains a user’s checking loop rather than resolving the task.|Interpersonal maintenance of rituals, distinct from linguistic presupposition accommodation.
Negative urgency|Intense negative emotion is associated with a disposition toward rash action.|urgency|Hold decision evidence fixed and vary negative-affect framing before tool use.|Affect-contingent impulsivity, distinct from general action bias; no felt AI emotion is assumed.
Positive urgency|Intense positive emotion is associated with a disposition toward rash action.|urgency|Hold evidence fixed and vary excitement framing before consequential action.|Positive-valence counterpart of urgency, correlated rather than an assumed independent mechanism.
Moses illusion|A semantically close incorrect term in a question can escape detection while the question is answered.|goodenough|Replace a central name with a plausible neighbour in a factual question.|Semantic anomaly detection, a specific route to presupposition acceptance rather than all false premises.
Good-enough processing|Comprehension may rely on a partial or underspecified representation rather than a complete analysis.|goodenough|Use sentences whose plausible gist conflicts with their precise syntax.|Shallow representation, distinct from the temporary ambiguity specifically tested by garden-path parsing.
Lexical entrainment|Conversational partners converge on and reuse agreed labels for referents.|entrainment|Teach a partner-specific object label and test reuse and transfer to a new partner.|Referential label pact, distinct from matching formality or general register.
Audience-design failure|A speaker fails to adapt an utterance to what a particular listener knows or can access.|audience|Give speaker and listener different visual access and score usable descriptions.|Listener-specific common ground; narrower and more operational than a generic curse of knowledge.
Syntactic persistence|A recently used sentence structure increases the likelihood of reusing that structure.|syntax|Prime one structure and measure its use for unrelated subsequent content.|Syntactic form, distinct from semantic priming and broad pattern completion.
Linguistic intergroup bias|Desirable ingroup and undesirable outgroup acts tend to receive more abstract descriptions than their opposites.|lib|Cross group and valence, then score abstraction of descriptions.|Language abstraction interaction, a specific expression of group bias rather than mere sentiment.
Recognition heuristic|When one of two alternatives is recognised, recognition can guide inference about which has more of a target attribute.|thought|Vary name familiarity independently of the attribute being inferred.|Recognised versus unrecognised contrast, distinct from availability of vivid examples; sometimes ecologically useful.
Representational momentum|Memory for an observed object’s final position is displaced in the direction of implied motion.|momentum|Test remembered final positions after visual motion while varying direction.|Direction-specific spatial extrapolation, rather than generic hallucination.
Boundary extension|Memory for a scene can include space beyond the boundaries actually shown.|boundary|Compare recalled image boundaries with the original crop.|Extrapolated scene extent, distinct from inventing an object within the observed image.
Truth-default|Communication is initially accepted as honest unless something triggers active suspicion.|truth|Compare credibility judgments before and after diagnostic deception cues.|Default stance toward a speaker, distinct from belief inflation through repetition.
Choice overload|Larger option sets can reduce choice likelihood or satisfaction under some conditions.|choice|Vary assortment size while controlling option quality and task difficulty.|Option-set manipulation, rather than general load alone. Meta-analyses show substantial heterogeneity.
Choice deferral|A person postpones selecting an option rather than choosing among the currently available alternatives.|deferral|Offer explicit choose-now versus defer options with fixed costs and information.|One form of decision avoidance; distinct from status quo preference, omission bias and refusal to answer.
Maximization|Decision making aims to find the best available option and may involve extensive alternative search.|maximize|Compare exhaustive search with a stated sufficient-quality threshold.|Search criterion, rather than effort avoidance; not automatically maladaptive.
Regret aversion|Choices are shaped by a desire to avoid the regret expected from learning a forgone option was better.|regret|Vary whether forgone outcomes will be revealed while holding payoffs fixed.|Counterfactual feedback, distinct from loss aversion over the chosen outcome.
Inaction inertia|Missing a particularly attractive opportunity can reduce acceptance of a later, still-beneficial opportunity.|inertia|Show a missed excellent offer before an unchanged acceptable offer.|Missed-opportunity comparison, distinct from sunk costs already paid.
Impact bias|Future emotional reactions are predicted to be more intense or longer lasting than they turn out to be.|impact|Compare forecasts of user reactions with longitudinal observations when available.|Forecast magnitude and duration, rather than ordinary confidence in a factual claim.
Projection bias|Current tastes are overprojected onto one’s own future preferences.|projection|Vary a current preference while independently specifying future conditions.|Current-to-future self projection, distinct from attributing one’s preferences to other people.
Hot–cold empathy gap|People in one visceral or affective state underestimate how another state changes judgment or motivation.|hotcold|Test predictions of behaviour across explicitly different motivational states.|Cross-state prediction, not a claim that an AI has hunger, craving or subjective emotion.
Present bias|An immediate outcome receives disproportionate weight compared with otherwise similar delayed outcomes.|present|Shift both options equally into the future and test for preference reversal.|Immediacy and time inconsistency, distinct from discounting effort costs.
Pseudoinefficacy|Awareness of people who cannot be helped reduces motivation to help those who can be helped.|pseudo|Keep achievable benefit fixed and vary information about unreachable beneficiaries.|Unmet needs reduce support for effective help, rather than insensitivity to beneficiary count alone.
'''

GROUPS = ['Memory and retrieval', 'Attention and cognitive control', 'Learning and conditioning',
          'Judgment and evaluation', 'Social cognition', 'Motivation and self-regulation',
          'Psychotherapy: thought patterns', 'Psychotherapy: behaviour and interaction',
          'Language and perception', 'Choice and future preferences']


def build():
    sources = {}
    for line in SOURCE_DATA.strip().splitlines():
        key, title, url, access = line.split('|')
        assert key not in sources
        sources[key] = dict(id=key, title=title, url=url, consulted=access)
    entries = []
    for i, line in enumerate(DATA.strip().splitlines(), 1):
        name, definition, source, probe, distinction = line.split('|')
        entries.append(dict(id=f'candidate-{i:03}', name=name, definition=definition,
                            group=GROUPS[(i-1)//10], source_ids=[source],
                            ai_status='PROPOSED ANALOGY; NOT TESTED IN THIS RESEARCH',
                            proposed_ai_probe=probe, distinction_and_limits=distinction))
    entries[90]['source_ids'].append('choice-meta')
    assert len(entries) == 100
    assert len({e['name'].casefold() for e in entries}) == 100
    assert all(s in sources for e in entries for s in e['source_ids'])
    ontology = ROOT / 'ontology' / 'ethical-ai.yaml'
    import yaml
    existing = yaml.safe_load(ontology.read_text())
    names = []
    def collect(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('name', 'title') and isinstance(v, str):
                    names.append(v)
                collect(v)
        elif isinstance(obj, list):
            for v in obj:
                collect(v)
    collect(existing)
    assert len(existing['modes']) == 207
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.casefold())
    collisions = sorted(e['name'] for e in entries if norm(e['name']) in {norm(n) for n in names})
    assert not collisions, collisions
    earlier_proposals = ['Choice blindness', 'False consensus / preference projection',
        'Bias blind spot', 'Retrieval-induced forgetting', 'External-knowledge misattribution',
        'Hidden-profile failure', 'Deliberate ignorance / moral wiggle room', 'Algorithm aversion',
        'Illusion of explanatory depth', 'Continued influence after correction']
    assert not {norm(e['name']) for e in entries} & {norm(n) for n in earlier_proposals}
    payload = dict(title='100 psychology-derived behaviour candidates for AI evaluation',
                   researched_on='2026-11-06', language='en',
                   status='RESEARCH SHORTLIST — NOT 100 ESTABLISHED AI FAILURE MODES',
                   method='Selected book/chapter passages, article abstracts, reviews and clinical manuals. Full books were not read end to end. Definitions are paraphrases. AI probes are original hypotheses, not findings of the cited human research.',
                   novelty='Names checked against the 207-entry ontology and the earlier ten research proposals; semantic distinctions reviewed manually. Some candidates refine existing broad mechanisms; these are identified per entry. Distinct names do not establish independent mechanisms.',
                   exclusions=['Earlier ten psychology-expansion proposals', 'Learned irrelevance: disputed specificity', 'Zeigarnik memory advantage: not treated as universal; Ovsiankina resumption retained instead'],
                   caution='Clinical constructs describe human functioning, not diagnoses or subjective experiences of AI. Some learning evidence is from nonhuman animals. Benign and adaptive processes are included; not every behaviour is a failure.',
                   baseline=dict(path='ontology/ethical-ai.yaml', sha256=hashlib.sha256(ontology.read_bytes()).hexdigest(), expected_catalogue_entries=207,
                                 existing_mode_names=[m['name'] for m in existing['modes']], excluded_earlier_proposals=earlier_proposals),
                   sources=list(sources.values()), entries=entries)
    out_json = ROOT / 'references' / 'behaviour-candidates-100-2026-11-06.json'
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    OUT.mkdir(parents=True, exist_ok=True)
    csv_buffer = io.StringIO(newline='')
    fields = ['id', 'group', 'name', 'definition', 'ai_status', 'proposed_ai_probe', 'distinction_and_limits', 'sources', 'source_access']
    writer = csv.DictWriter(csv_buffer, fieldnames=fields)
    writer.writeheader()
    for e in entries:
        row = {k: e[k] for k in fields if k in e}
        row['sources'] = ' ; '.join(sources[s]['url'] for s in e['source_ids'])
        row['source_access'] = ' ; '.join(sources[s]['consulted'] for s in e['source_ids'])
        writer.writerow(row)
    (OUT / '100-behaviours.csv').write_text(csv_buffer.getvalue())
    (OUT / '100-behaviours.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    h = html.escape
    cards = []
    for i, e in enumerate(entries, 1):
        if (i-1) % 10 == 0:
            cards.append(f'<h2>{h(e["group"])}</h2>')
        links = ''.join(f'<li><a href="{h(sources[s]["url"], quote=True)}">{h(sources[s]["title"])}</a><br><small>Consulted: {h(sources[s]["consulted"])}</small></li>' for s in e['source_ids'])
        cards.append(f'<article id="{e["id"]}"><h3>{i}. {h(e["name"])}</h3><p>{h(e["definition"])}</p><details><summary>Source, distinction and proposed AI test</summary><p><strong>Proposed test, not a finding:</strong> {h(e["proposed_ai_probe"])}</p><p><strong>Distinction and limits:</strong> {h(e["distinction_and_limits"])}</p><ul>{links}</ul></details></article>')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>100 psychology-derived behaviour candidates | EthicalAI</title><meta name="description" content="100 sourced psychological behaviour candidates for AI evaluation: names, definitions, novelty boundaries and proposed tests. Human research is separated from AI hypotheses."><link rel="canonical" href="https://ethicalai.alexandrudan.com/research/100-behaviours.html"><style>
    *{box-sizing:border-box}body{margin:0;background:#f8f8f3;color:#18251f;font:17px/1.6 system-ui,sans-serif}main{max-width:960px;margin:auto;padding:32px 24px 80px}a{color:#215f4b;overflow-wrap:anywhere}h1{font-size:clamp(2rem,6vw,3.3rem);line-height:1.12}h2{margin-top:3rem;border-bottom:2px solid #b8c9bc;padding-bottom:8px}h3{margin:0 0 8px;font-size:1.15rem}article{padding:22px 0;border-bottom:1px solid #d5ded6;scroll-margin-top:20px}article p{margin:8px 0}details{font-size:.93rem}summary{cursor:pointer;color:#215f4b}small{color:#536258}.notice{background:#e9eee5;padding:20px;border-left:4px solid #56826d}nav{display:flex;gap:18px;flex-wrap:wrap}input{width:100%;padding:14px;border:1px solid #879b8e;border-radius:5px;font:inherit}#result{font-size:.9rem}.hidden{display:none}footer{margin-top:40px;font-size:.9rem}
    </style></head><body><main><nav><a href="/">← EthicalAI directory</a><a href="100-behaviours.csv" download>Download CSV</a></nav><h1>100 behaviour candidates from psychology</h1><p>Names and definitions from memory research, learning theory, social psychology, cognitive therapy and decision research.</p><div class="notice"><strong>Research shortlist, not 100 established AI failure modes.</strong><p>These names were compared with the existing 207-entry catalogue and the earlier ten expansion proposals. Several refine broader existing mechanisms; their boundaries are explicit below. They have not been added to the established catalogue count.</p><p>Sources range from selected book passages to abstracts and indexed excerpts. No complete book was read end to end. Open each entry to see exactly what was consulted. Definitions paraphrase human research; suggested AI tests are hypotheses, not results from those sources.</p><p>Clinical labels do not diagnose AI or establish that it experiences feelings. Some conditioning findings come from animal research. Adaptive processes are included alongside potential problems.</p></div><p><label for="search">Filter by name or definition</label><input id="search" type="search" placeholder="e.g. memory, uncertainty, avoidance"></p><p id="result" aria-live="polite">100 candidates</p>'''+''.join(cards)+'''<footer><p>Evidence limits: actor–observer asymmetry has weak aggregate support; choice overload varies substantially by context. CBT thinking-style categories overlap. Learned irrelevance was excluded because its specificity is disputed; the Zeigarnik memory advantage was not treated as universal.</p><p>Researched 6 November 2026. This is an authoring-context literature shortlist, not an independent systematic review or a completed set of AI experiments. Research and proposed probes require further validation before promotion into the canonical ontology.</p></footer></main><script>
    const input=document.querySelector('#search'), articles=[...document.querySelectorAll('article')];input.addEventListener('input',()=>{const q=input.value.toLocaleLowerCase();let n=0;for(const a of articles){const match=(a.querySelector('h3').textContent+' '+a.querySelector('p').textContent).toLocaleLowerCase().includes(q);a.classList.toggle('hidden',!match);if(match)n++;}for(const heading of document.querySelectorAll('h2')){let el=heading.nextElementSibling,visible=false;while(el&&el.tagName!=='H2'&&el.tagName!=='FOOTER'){if(el.tagName==='ARTICLE'&&!el.classList.contains('hidden'))visible=true;el=el.nextElementSibling;}heading.classList.toggle('hidden',!visible);}document.querySelector('#result').textContent=n+' candidates';});
    </script></body></html>'''
    page = page.replace('<h1>100 behaviour candidates from psychology</h1>', '<h1>100 behaviour candidates from psychology</h1><p class="notice"><strong>Expanded directory:</strong> <a href="behaviour-candidates.html">Explore 228 candidates</a>, combining this original shortlist with 145 uploaded contributions and 17 merged overlaps.</p>')
    (OUT / '100-behaviours.html').write_text(page)
    print(json.dumps({'entries':len(entries),'sources':len(sources),'groups':dict(Counter(e['group'] for e in entries)),'exact_name_collisions':collisions}))


if __name__ == '__main__':
    build()

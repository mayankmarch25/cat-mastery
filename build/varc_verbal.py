# -*- coding: utf-8 -*-
"""Original non-RC verbal ability items: para-jumbles, para-summaries, odd-one-out."""

JUMBLES = [
 {"sents": [
   "The first cities were not built for trade but for storage.",
   "Grain had to be held somewhere between harvests, and holding it required walls, records and guards.",
   "Trade followed, because a settlement holding surplus attracts people who want some of it.",
   "What began as a defensive accounting problem therefore produced the market as a by-product."],
  "order": "1234",
  "exp": "Sentence 1 makes the claim, 2 explains the storage requirement, 3 introduces trade as a consequence, and 4 closes by naming the result. The chain runs claim, mechanism, consequence, conclusion."},
 {"sents": [
   "Most committees exist to distribute responsibility rather than to exercise it.",
   "This is why their decisions so often arrive late and in a form no member would have chosen alone.",
   "A single decision-maker can be blamed, and the prospect of blame concentrates the mind.",
   "A group cannot be blamed in the same way, and the diffusion is precisely the point."],
  "order": "1342",
  "exp": "1 states the claim, 3 and 4 form a contrast pair explaining the blame mechanism, and 2 draws the consequence. The pair 3 and 4 must stay adjacent and must precede the 'this is why' in 2."},
 {"sents": [
   "Rivers were the first boundaries because they were the first things that could not be moved.",
   "A boundary needs to be visible, agreed and difficult to shift overnight.",
   "Later surveying made invisible lines enforceable, and the logic of the natural boundary faded.",
   "Even so, most disputes about territory still turn on waterways."],
  "order": "2134",
  "exp": "2 establishes the general requirement for boundaries, 1 applies it to rivers, 3 marks the historical change, and 4 qualifies that change with a persistence. The general statement must precede the specific application."},
 {"sents": [
   "Standardised testing was introduced to reduce the influence of personal connection on admission.",
   "In that narrow aim it succeeded, and the succession of reforms since has not improved on it.",
   "But a test that cannot be influenced by connection can still be influenced by preparation.",
   "Preparation costs money, and so the barrier was relocated rather than removed."],
  "order": "1234",
  "exp": "1 gives the purpose, 2 concedes the success, 3 introduces the limitation with 'but', and 4 completes it. The concession must follow the stated aim and precede the objection."},
 {"sents": [
   "Vaccines are the rare intervention whose success erases the evidence for its own necessity.",
   "A disease that no longer circulates leaves no memory of what it did.",
   "Parents who have never seen the illness weigh a visible small risk against an invisible large one.",
   "The arithmetic they perform is reasonable; the inputs available to them are not."],
  "order": "1234",
  "exp": "1 states the paradox, 2 explains the mechanism of erasure, 3 describes the resulting behaviour, and 4 evaluates it. The evaluation cannot precede the behaviour it judges."},
 {"sents": [
   "Every language loses sounds, and the loss is never evenly distributed.",
   "Distinctions that carry little information disappear first.",
   "Those that separate common words persist long after they have become difficult to pronounce.",
   "Efficiency, in other words, operates on speech without anyone intending it."],
  "order": "1234",
  "exp": "1 states the general observation, 2 and 3 form the contrast that specifies it, and 4 generalises with 'in other words'. The summarising sentence must come last."},
 {"sents": [
   "The clock did not measure the working day so much as create it.",
   "Before mechanical time, work ended when the task ended or the light failed.",
   "Afterwards it ended at an hour, and the hour belonged to whoever owned the clock.",
   "Ownership of measurement has been a quiet form of authority ever since."],
  "order": "1234",
  "exp": "1 is the thesis, 2 gives the prior state, 3 gives the altered state, and 4 generalises. The before and after pair must sit in that order between thesis and conclusion."},
 {"sents": [
   "Scientific fraud is rare, and the attention it receives is disproportionate to its frequency.",
   "The more common failure is work that is honest, published and simply not reproducible.",
   "Fraud is also easier to discuss, because it has a villain and a moment of decision.",
   "Irreproducibility has neither, which is why it attracts committees instead of headlines."],
  "order": "1234",
  "exp": "1 raises fraud, 2 contrasts it with the commoner failure, 3 explains the attention asymmetry, and 4 closes the contrast. Sentence 4's 'neither' refers back to the villain and moment in 3."},
 {"sents": [
   "Cities grow outward until transport costs make the edge unattractive.",
   "Every improvement in transport therefore moves the edge further out.",
   "The improvement is sold as a remedy for congestion.",
   "It reliably produces more of it, at a greater distance."],
  "order": "1234",
  "exp": "1 establishes the rule, 2 derives the consequence with 'therefore', 3 introduces the claim made for improvements, and 4 refutes it. The refutation must directly follow the claim it rejects."},
 {"sents": [
   "A warranty is a statement about the seller's confidence, not about the product.",
   "A long warranty signals that failures are expected to be rare enough to be cheap.",
   "A short one signals nothing at all, since it is the default.",
   "Buyers read warranties as promises; sellers write them as forecasts."],
  "order": "1234",
  "exp": "1 is the claim, 2 and 3 supply the paired signals, and 4 closes with the contrast between reading and writing. The paired examples must remain adjacent and precede the summary."},
 {"sents": [
   "Famines rarely occur because there is insufficient food in a region.",
   "They occur because some group loses the ability to command food that is present.",
   "Prices rise, wages do not, and entitlement collapses before supply does.",
   "This is why relief that ships grain can fail while relief that ships money works."],
  "order": "1234",
  "exp": "1 denies the common explanation, 2 supplies the correct one, 3 details the mechanism, and 4 draws the practical implication introduced by 'this is why'."},
 {"sents": [
   "A pilot study that succeeds proves less than its sponsors usually claim.",
   "Pilots run with motivated staff, close supervision and the attention that novelty attracts.",
   "Scaling removes all three while keeping only the protocol.",
   "What is being tested at scale is therefore not the thing that was tested in the pilot."],
  "order": "1234",
  "exp": "1 states the claim, 2 lists the pilot's advantages, 3 explains what scaling removes, and 4 concludes with 'therefore'. The conclusion depends on both 2 and 3."},
]

SUMMARIES = [
 {"para": ("Economic sanctions are usually evaluated by whether the target government changes its "
           "behaviour, a standard that almost guarantees a verdict of failure. Governments that "
           "yield visibly to external pressure pay a domestic price, so even a leadership that has "
           "privately decided to concede will delay and disguise the concession. The effects that do "
           "occur are slower and less legible: elite coalitions fracture, procurement networks "
           "become costlier, and the range of policies that remain affordable narrows. None of this "
           "registers on a measure built around announced reversals."),
  "correct": "Sanctions are judged by a visible-reversal standard that misses their slower structural effects on elites, costs and policy options.",
  "wrong": ["Sanctions rarely work because target governments are willing to absorb economic pain rather than lose domestic standing.",
            "Sanctions should be abandoned in favour of diplomatic measures that do not impose costs on civilian populations.",
            "Governments that concede to sanctions do so secretly, which makes measuring the effectiveness of sanctions impossible."],
  "exp": "The passage's argument is about the mismatch between the measure used and the effects produced, not about whether sanctions work in general."},
 {"para": ("The idea that remote work reduces costs rests on counting the office and ignoring "
           "everything the office supplied without invoicing. Informal correction, the overheard "
           "problem, the junior who learns by proximity: none of these appeared as line items, so "
           "their removal appears as savings. The costs reappear later as slower onboarding, weaker "
           "internal networks and decisions made with less context. They are real, they are large, "
           "and they are charged to a different account."),
  "correct": "Remote work appears cheaper only because the office's uninvoiced benefits were never counted, and their loss surfaces later as other costs.",
  "wrong": ["Remote work damages organisations by preventing junior employees from learning through proximity to experienced colleagues.",
            "Organisations should return to office-based work because the savings from remote arrangements have proved illusory.",
            "Accounting systems are inadequate for measuring the productivity of knowledge workers in any setting."],
  "exp": "The core claim is about invisible benefits that were never on the books, resurfacing later under different headings."},
 {"para": ("Attempts to preserve endangered languages often concentrate on documentation, which is "
           "valuable and insufficient. A recorded grammar lets scholars study a language; it does "
           "not give a child a reason to speak it. Languages survive when they remain the medium of "
           "something people want to do, whether that is worship, commerce or courtship. Where the "
           "domains have been lost, documentation preserves the specimen while the organism is "
           "already gone."),
  "correct": "Documentation preserves a language as an object of study but cannot sustain it, since survival depends on retaining domains of actual use.",
  "wrong": ["Language documentation is a waste of resources that would be better spent on bilingual education programmes.",
            "Endangered languages disappear mainly because younger speakers consider them less prestigious than dominant languages.",
            "Scholars have failed to record enough endangered languages before their last speakers died."],
  "exp": "The passage concedes documentation's value and locates survival in continued use, which the summary must carry."},
 {"para": ("Open-plan offices were introduced partly on the argument that visibility encourages "
           "collaboration. Measured collaboration generally falls. What rises is the volume of "
           "written messaging, as workers withdraw from a setting where every conversation is "
           "audible and shift to channels they can control. The design produced the opposite of its "
           "stated aim through a mechanism its advocates had not considered, which is that "
           "visibility is also exposure."),
  "correct": "Open-plan design reduced the collaboration it was meant to encourage, because visibility pushed workers into controllable written channels.",
  "wrong": ["Open-plan offices should be replaced with private rooms to allow employees to concentrate without interruption.",
            "Written communication is a more efficient medium for collaboration than face-to-face conversation.",
            "The advocates of open-plan design misrepresented evidence in order to justify reducing office costs."],
  "exp": "The summary must retain both the reversal of the stated aim and the exposure mechanism that caused it."},
 {"para": ("A road built to relieve congestion fills up. The mechanism is not mysterious. Journeys "
           "that were not worth making at the old travel time become worth making at the new one, "
           "and demand expands until the cost in time returns to roughly where it was. This is not "
           "a failure of forecasting but a consequence of treating a price as if it were a fixed "
           "quantity of demand."),
  "correct": "New road capacity refills because lower travel time generates additional trips, restoring the original congestion cost.",
  "wrong": ["Road building should stop because it has never succeeded in reducing travel times anywhere.",
            "Traffic forecasters consistently underestimate the number of vehicles that will use a new road.",
            "Congestion can only be addressed by charging drivers directly for the use of road space."],
  "exp": "The summary needs the induced-demand mechanism and the return to the original time cost, not a policy prescription."},
 {"para": ("Microfinance was promoted on the expectation that credit would convert the poor into "
           "entrepreneurs. The evidence that accumulated instead showed borrowing used to smooth "
           "consumption, pay for illness and manage irregular income. This was treated as a "
           "disappointing result. It is better read as a finding: what was scarce was not "
           "opportunity but the ability to absorb shocks, and the product worked on the problem "
           "that actually existed."),
  "correct": "Microfinance was used to absorb shocks rather than fund enterprise, which reveals the real scarcity rather than indicating failure.",
  "wrong": ["Microfinance has failed to lift borrowers out of poverty and should be replaced by direct cash transfers.",
            "Poor households misuse credit because they lack the financial training required to run a business.",
            "Lenders deliberately marketed microfinance for entrepreneurship while knowing it would be used otherwise."],
  "exp": "The passage reframes an apparent disappointment as evidence about which scarcity was binding."},
 {"para": ("Peer review is often defended as a filter for correctness, which it has never been. A "
           "reviewer reading a manuscript cannot repeat the experiments, inspect the raw data or "
           "verify that the analysis was chosen before the results were seen. What review can do is "
           "check that the claims follow from what is reported and that the work is situated in the "
           "literature. These are useful functions. They are not the function the defence claims."),
  "correct": "Peer review cannot verify correctness and instead checks internal coherence and context, which is useful but different from what defenders claim.",
  "wrong": ["Peer review should be abolished because it fails to detect errors and fraudulent results in published work.",
            "Reviewers lack the time and incentives necessary to examine manuscripts with sufficient care.",
            "Scientific publishing would improve if raw data were made available alongside every manuscript."],
  "exp": "The summary must preserve both the denial of the correctness claim and the author's recognition of review's actual value."},
 {"para": ("Heritage conservation regulations preserve buildings and, in doing so, freeze the "
           "pattern of ownership that existed when the rules were written. A protected facade "
           "cannot be altered, so the building cannot be adapted, so its use is fixed, so the value "
           "accrues to whoever already holds it. The stated purpose is cultural continuity. The "
           "reliable effect is a transfer to incumbents, which is rarely stated at all."),
  "correct": "Heritage rules protect buildings while locking in existing ownership, transferring value to incumbents despite a cultural rationale.",
  "wrong": ["Heritage regulations should be relaxed so that historic buildings can be converted to modern commercial use.",
            "Conservation authorities have been captured by property owners who benefit from restrictive rules.",
            "Cultural continuity is an inadequate justification for restricting what owners may do with their property."],
  "exp": "The summary needs the chain from restriction to fixed use to incumbent gain, alongside the stated purpose."},
 {"para": ("The claim that technology destroys jobs and the claim that it creates them are both "
           "true and are usually argued as if only one could be. The destruction is concentrated, "
           "immediate and identifiable by name and place. The creation is dispersed, delayed and "
           "anonymous. Aggregate employment figures reconcile the two and in doing so conceal the "
           "fact that the people in the first group are frequently not the people in the second."),
  "correct": "Technology both destroys and creates jobs, but the losses are concentrated and the gains dispersed, so aggregates hide that different people are affected.",
  "wrong": ["Technological change has no net effect on employment once new industries are accounted for.",
            "Aggregate employment statistics are unreliable and should not be used in policy debates about automation.",
            "Workers displaced by technology should be retrained so that they can take up newly created roles."],
  "exp": "The distinguishing content is the non-overlap between those who lose and those who gain, which aggregates conceal."},
 {"para": ("Biodiversity is usually defended on instrumental grounds: undiscovered medicines, "
           "pollination services, ecosystem stability. The arguments are sound and they carry a "
           "risk. An instrumental defence invites an instrumental reply, and once the value of a "
           "species is a number, it can be outbid. Those who care about the living world for "
           "reasons that are not instrumental have accepted a vocabulary in which their actual "
           "reason cannot be expressed."),
  "correct": "Defending biodiversity on instrumental grounds allows species value to be outbid and leaves non-instrumental reasons unsayable.",
  "wrong": ["Biodiversity should be protected for its intrinsic value rather than for any benefit it provides to humans.",
            "Economic valuations of ecosystem services systematically underestimate the true worth of biodiversity.",
            "Conservationists have failed to communicate the practical benefits of biodiversity to policymakers."],
  "exp": "The passage warns about the cost of adopting a vocabulary, not about which valuation is correct."},
 {"para": ("Credentials began as evidence of training and have become a mechanism for rationing "
           "access. When more people hold a qualification than there are positions requiring it, "
           "employers raise the requirement, and the qualification's informational content falls "
           "while its cost to obtain rises. Each individual response is sensible. The collective "
           "result is that everyone spends longer in education to occupy the same position in the "
           "queue."),
  "correct": "As qualifications proliferate, employers raise requirements, so credentials cost more while signalling less and leave relative position unchanged.",
  "wrong": ["Higher education has expanded too rapidly and should be restricted to students with the strongest academic records.",
            "Employers are wrong to use educational qualifications as a proxy for ability in hiring decisions.",
            "The content of university degrees has declined in quality as enrolment numbers have increased."],
  "exp": "The core is the escalation mechanism: individually rational responses producing no collective gain."},
 {"para": ("Resilience has largely replaced prevention in the vocabulary of disaster policy, and "
           "the substitution carries an argument. Prevention assigns responsibility to whoever "
           "creates the hazard. Resilience assigns capacity to whoever must survive it. The shift "
           "is presented as pragmatic realism about hazards that cannot be eliminated, and it is "
           "partly that. It is also a relocation of duty, performed without being announced."),
  "correct": "The move from prevention to resilience quietly shifts responsibility from those creating hazards to those enduring them.",
  "wrong": ["Resilience policies are ineffective because they do not address the underlying causes of disasters.",
            "Disaster policy should return to prevention, since most hazards can in fact be eliminated at source.",
            "Policymakers adopted the language of resilience in order to reduce public spending on disaster relief."],
  "exp": "The summary must carry the relocation of duty and the fact that it was not announced, while retaining the partial concession."},
]

ODD_ONE_OUT = [
 {"sents": [
   "Coastal mangroves absorb wave energy before it reaches inhabited land.",
   "Their root systems trap sediment and slow the retreat of the shoreline.",
   "Removing them for aquaculture transfers a protective function onto concrete that must be built and maintained.",
   "Shrimp farming has grown rapidly across South and Southeast Asia over the past three decades."],
  "odd": 4,
  "exp": "Sentences 1 to 3 form a connected argument about the protective function of mangroves and the cost of removing it. Sentence 4 states a fact about industry growth that the argument does not use."},
 {"sents": [
   "A deadline changes the distribution of effort rather than its total.",
   "Work expands and contracts to meet the time available for its completion.",
   "Most of the output appears in the final fraction of the period allotted.",
   "Project management software has made it easier to track progress against milestones."],
  "odd": 4,
  "exp": "The first three describe how deadlines reshape effort over time. The fourth shifts to tools for tracking, which does not belong to that chain."},
 {"sents": [
   "Spices were valuable in medieval Europe partly because they were difficult to transport.",
   "Scarcity created by distance is indistinguishable, at the point of sale, from scarcity created by rarity.",
   "When sea routes shortened, the price collapsed although the plant had not become more common.",
   "Several spices were also believed to have medicinal properties that modern research has not confirmed."],
  "odd": 4,
  "exp": "Sentences 1 to 3 build a single argument about distance-based scarcity and price. Sentence 4 raises medicinal belief, which is unrelated to that mechanism."},
 {"sents": [
   "A second language is easier to acquire when the learner needs it for something other than the lesson.",
   "Classroom instruction supplies grammar but rarely supplies necessity.",
   "Learners embedded in a setting where the language is the only medium progress faster with less teaching.",
   "Many countries have introduced compulsory second-language instruction in primary schools."],
  "odd": 4,
  "exp": "The first three argue that necessity drives acquisition more than instruction. The fourth reports a policy, which neither supports nor extends the argument."},
 {"sents": [
   "A city's water supply is usually described in terms of total availability.",
   "What determines whether taps run is the reliability of distribution, not the volume at the source.",
   "Systems with ample reservoirs and failing pipes deliver less than systems with modest reservoirs and sound ones.",
   "Reservoir construction accelerated worldwide during the middle of the twentieth century."],
  "odd": 4,
  "exp": "Sentences 1 to 3 contrast availability with distribution. Sentence 4 offers a historical note that plays no role in that contrast."},
 {"sents": [
   "Reputation functions as collateral in markets where contracts are hard to enforce.",
   "A trader who cheats once loses access to future transactions worth more than the gain.",
   "This is why informal credit networks survive in settings with weak courts.",
   "Commercial law in most jurisdictions has been substantially codified since the nineteenth century."],
  "odd": 4,
  "exp": "The first three explain how reputation substitutes for enforcement. The fourth describes the codification of law, which is outside that argument."},
 {"sents": [
   "Rooftop solar shifts generation to the point of consumption and removes transmission losses.",
   "It also removes the utility's ability to recover fixed network costs from those households.",
   "The resulting shortfall is recovered from customers who have not installed panels.",
   "Panel efficiency has improved steadily while manufacturing costs have fallen."],
  "odd": 4,
  "exp": "Sentences 1 to 3 trace a cost-shifting consequence. Sentence 4 is a statement about technology trends that the sequence does not require."},
 {"sents": [
   "An apology that explains itself is usually attempting something other than apology.",
   "The explanation supplies context, and context invites the hearer to reconsider the offence.",
   "What is offered as contrition functions as a renewed defence.",
   "Public figures increasingly issue statements through social media rather than press conferences."],
  "odd": 4,
  "exp": "The first three analyse the structure of explained apologies. The fourth concerns the channel of communication, which is unrelated."},
 {"sents": [
   "Crop insurance changes which crops farmers plant, not merely how they bear risk.",
   "Insured varieties become more attractive than uninsured ones of comparable yield.",
   "Diversity in the field narrows, and the narrowing increases exposure to a single pathogen.",
   "Agricultural extension services were first established to spread new farming techniques."],
  "odd": 4,
  "exp": "Sentences 1 to 3 form a chain from insurance to planting choice to concentrated risk. Sentence 4 introduces extension services, which has no place in it."},
 {"sents": [
   "A library's catalogue determines what can be found, which determines what is read.",
   "Material that is held but not described is functionally absent from the collection.",
   "Cataloguing decisions therefore shape scholarship as much as acquisition decisions do.",
   "Digital storage has reduced the physical space required to house large collections."],
  "odd": 4,
  "exp": "The first three argue that description governs access and therefore scholarship. The fourth is about storage, which the argument does not use."},
]

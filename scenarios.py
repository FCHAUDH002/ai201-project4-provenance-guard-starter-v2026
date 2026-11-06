"""
What my test runs. UNIT 8, MILESTONE 3

Criterion 1: my own writing (SCENARIOS "my own writing")
Criterion 2: known AI vs known human (average confidence)
Criterion 3: label coverage
Criterion 4: appeal path, tested by hand (needs a content_id from a submission)
Criterion 5: bad input
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            """Today, I went to a college fair and spoke to several different recruiters. It was very stressful at first, but I had a lot of good conversations and learned a lot.""",
            """I chose to major in computer engineering because I wanted to learn about both software and hardware and have the opportunity to work in either field in the future.""",
            """To get to The City College of New York, I take the 4 train to 161st and then transfer to the D train to 145th. I then walk or take the college shuttle to campus.""",
            """My favorite season is the fall because the colorful leaves on the trees look beautiful. It is perfect sweater weather since it is not too cold or hot outside.""",
            """Usually, Tuesdays are my toughest days of the week because I have class from 9:30 am to 5 pm with very few breaks in between. I get so tired after my 3 hour lab and just crash when I get home.""",
            """My advice for first-year college students would be to join student clubs and go to college events because those are a great place to learn, network, and lead to a lot of opportunities.""",
            """When preparing for an exam, I usually figure out what topics will be one the exam, review my notes from the course textbook or slides, and work on practice problems.""",
            """My music taste is all over the place. It has songs in various languages such as English, Urdu, Punjabi, Spanish, Korean, etc. It also has various genres including pop, hip pop, traditional, etc.""",
            """This weekend is my friend's birthday! She is a little adventurous so we plan on going high roping together with another friend. I am not sure how its gonna go since we are all scared of heights but it sounds fun.""",
            """I think that it is very important to try new things and that is something that I am trying to work on. Last year, i took a beginner ice skating course and learned that I love to do so. This year, I started going to the gym and got to learn so many things about how to become healthier and stronger.""",
        ],
    },
    {
        "name": "known AI",
        "criterion": 2,
        "texts": [
            """Renewable energy plays a crucial role in addressing the challenges of climate change. By harnessing sources such as solar, wind, and hydroelectric power, societies can significantly reduce their reliance on fossil fuels. Furthermore, advances in storage technology have made these options more reliable than ever. Ultimately, investing in clean energy is essential for ensuring a sustainable and prosperous future for generations to come.""",
            """Effective communication is a fundamental skill in both personal and professional settings. Individuals who communicate clearly are better equipped to build strong relationships and resolve conflicts. There are several key strategies to consider. First, active listening demonstrates respect and understanding. Second, using concise language helps ensure that messages are received accurately. Finally, seeking feedback allows speakers to refine their approach and improve over time.""",
            """Regular physical exercise offers numerous benefits for overall health and well-being. Engaging in activities such as walking, swimming, or strength training can improve cardiovascular health and boost mood. Additionally, consistent exercise has been shown to enhance sleep quality and reduce stress levels. It is important to choose activities that are enjoyable, as this increases the likelihood of maintaining a long-term routine.""",
            """The rapid advancement of artificial intelligence is transforming industries across the globe. From healthcare to finance, organizations are leveraging these technologies to improve efficiency and decision-making. However, this progress also raises important ethical considerations. Issues such as data privacy, algorithmic bias, and job displacement must be carefully addressed. Responsible development and thoughtful regulation will be key to maximizing the benefits of this powerful technology.""",
            """Travel provides valuable opportunities for personal growth and cultural understanding. Visiting new destinations allows individuals to experience different traditions, cuisines, and perspectives. It also encourages adaptability and problem-solving, as travelers navigate unfamiliar environments. Whether exploring a bustling city or a quiet countryside, each journey offers unique insights. As a result, travel remains one of the most enriching experiences available to people of all ages.""",
        ],
    },
    {
        "name": "known human",
        "criterion": 2,
        "texts": [
            """This might be because I'm a business major specializing in marketing, but I wish that I had more opportunities to write essays and learn how to do research, gather my thoughts and communicate my ideas. (I guess you could say that I'm feeling inscure because I love the humanities so much but do not have the skills necessary to hold my own in a room.)""",
            """Many colleges require some study in a second language. For those who decided on a language, how "utilitarian" was your choice?For example, one of the schools I am looking into has languages like Bosnian, Kazakh, and Lithuanian. I am interested in some of these, but most of my peers are saying I should learn Spanish as it is more useful.""",
            """I don’t always set up my study table before studying. Sometimes, if I only have a few questions to solve and I already know the concept, I just do them while lying on my bed. For some reason, setting everything up before I start makes my motivation to study decrease.""",
            """My goal last night what to get a semi understanding of what information the datasets would actually be downloading and what info they’d provide, cause I don’t know what us looking at the images itself would do at this time so it was a lot of searching up what everything meant by itself and our proposal specifically""",
            """I'm committing to staying in the class since I'm an Econ major, but the content doesn't seem impossible to understand, and the textbook is pretty clear and easy too annotate. The practice quizzes are fine as well, I do them every chapter we finish. It just sounds like basic MicroEcon, my only issue is that the entire grade is tests and an attendance grade for discussions, but that just means I have to do good on tests.""",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            """I didn't sleep. Not properly, anyway — I lay there listening to the boiler tick and thinking about the thing I'd said to Marcus at the pub, which was stupid, and which he will absolutely bring up again. Twice now. So: coffee, and the long way round to work, and a plan. The plan lasted until about ten past nine, when Priya asked how the weekend was and I said "fine" in the voice that means it wasn't, and she put her mug down and looked at me. That's the trouble with Priya. She notices.""",
            """The committee's report, circulated in March, drew a sharp distinction between procedural compliance and genuine accountability. Compliance, it argued, can be satisfied by paperwork alone. Accountability cannot. Several members objected, reasonably, that the distinction was easier to state than to enforce; one noted that no audit had ever caught a failure of conscience. Still, the report's central claim stands: institutions that measure only what is easy to measure will, in time, forget what mattered.""",
            """Last weekend I went to my cousin's birthday party. We ate pizza and played games in the backyard. My little brother fell in the grass and got mud all over his shirt. Everyone laughed, even him. Then we had cake and I got the biggest piece. It was a fun day. I was tired when we got home, so I went to bed early.""",
            """Time management matters more than people admit, especially now that work moves as fast as it does. If you're organised you hit deadlines, and you're less frazzled doing it. A few things actually help. Prioritise — work out what genuinely matters and do that first. Cut the interruptions; notifications wreck focus and the damage is worse than it feels at the time. And take breaks, short ones, often.""",
            """Time management matters a lot in today's busy workplace. People who build good organizational habits are better placed to meet deadlines and cut down on stress. There are a few key strategies that can help with productivity. First, prioritisation is essential. By picking out the most important tasks and doing them first, workers make sure the critical goals get met. Second, cutting distractions plays a big role. Setting aside blocks of time for focused work is widely seen as helpful. Finally, regular breaks matter for staying sharp.""",
            """It is important to note that effective communication is essential. It is important to note that effective planning is essential. It is important to note that effective teamwork is essential. In conclusion, it is important to note that these key factors are essential for success in todays fast paced environment.""",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "too short", "creator_id": "eval_bad_short"},
            {"text": "word " * 1100, "creator_id": "eval_bad_long"},
        ],
    },
]


def validate() -> list[str]:
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
"""Copy and schedule for Volt Atelier, a fictional studio in Port Meridian."""

LIME = "#d6ff3c"
ORANGE = "#ff6a1a"
BLUE = "#3aa0ff"
GREEN = "#3ee07a"
YELLOW = "#ffd23a"
VIOLET = "#c9a6ff"
RED = "#ff3d5a"
INK = "#f6f3ec"
NAVY = "#070b16"
INK_DARK = "#14180c"

LANE_COLOR = {
    "Strength": ORANGE,
    "Conditioning": BLUE,
    "Ride": YELLOW,
    "Mobility": GREEN,
    "Restore": VIOLET,
}

LANES = list(LANE_COLOR)

LANE_INFO = [
    {
        "name": "Strength",
        "line": "Barbell, pulls, and presses with a plan, not a pile of sets.",
        "where": "Platform · 12 athletes",
        "accent": ORANGE,
    },
    {
        "name": "Conditioning",
        "line": "Engine work on the clock. Short, mean, and actually finished.",
        "where": "Kiln Floor · 16 athletes",
        "accent": BLUE,
    },
    {
        "name": "Ride",
        "line": "The Spoke Room. Cadence, hills, and a coach who calls the change.",
        "where": "Spoke Room · 14 bikes",
        "accent": YELLOW,
    },
    {
        "name": "Mobility",
        "line": "Joints you can use under a bar, not a stretch you forget by Tuesday.",
        "where": "Quiet Bay · 10 athletes",
        "accent": GREEN,
    },
    {
        "name": "Restore",
        "line": "Downshift. Tissue, breath, and range after the loud days.",
        "where": "Quiet Bay · 10 athletes",
        "accent": VIOLET,
    },
]


def session(
    key: str,
    name: str,
    lane: str,
    day: str,
    day_full: str,
    time: str,
    minutes: str,
    coach: str,
    level: str,
    spots: str,
    room: str,
    blurb: str,
) -> dict[str, str]:
    return {
        "key": key,
        "name": name,
        "type": lane,
        "day": day,
        "day_full": day_full,
        "time": time,
        "minutes": minutes,
        "coach": coach,
        "level": level,
        "spots": spots,
        "room": room,
        "blurb": blurb,
        "accent": LANE_COLOR[lane],
    }


CLASSES: list[dict[str, str]] = [
    session("mon-iron", "Iron Hour", "Strength", "Mon", "Monday", "6:15", "55 min", "Mara Voss", "All levels", "12 spots", "Platform", "Squat, press, and pull. The week starts with a barbell and a plan."),
    session("mon-engine", "Engine Block", "Conditioning", "Mon", "Monday", "12:10", "40 min", "Idris Hale", "All levels", "16 spots", "Kiln Floor", "A lunchtime piece on the clock. You should still be able to get back to work."),
    session("mon-ride", "Volt Ride", "Ride", "Mon", "Monday", "17:30", "45 min", "Noor Elian", "All levels", "14 bikes", "Spoke Room", "Cadence, hills, and one long note. The Spoke Room's flagship hour."),
    session("mon-range", "Slow Range", "Mobility", "Mon", "Monday", "19:00", "45 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "Hips, shoulders, and the positions Monday's barbell actually needs."),
    session("tue-oly", "Olympic Hour", "Strength", "Tue", "Tuesday", "6:30", "60 min", "Jun Park", "Intermediate", "12 spots", "Platform", "Snatch and clean variations. The same warm-up positions every week."),
    session("tue-kiln", "Kiln Conditioning", "Conditioning", "Tue", "Tuesday", "9:15", "45 min", "Idris Hale", "All levels", "16 spots", "Kiln Floor", "Carries, machines, and a posted effort. Finish the piece. Don't decorate it."),
    session("tue-restore", "Restore Room", "Restore", "Tue", "Tuesday", "18:00", "50 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "Downshift after the loud days. Breath, tissue, and easy range."),
    session("wed-iron", "Iron Hour", "Strength", "Wed", "Wednesday", "6:15", "55 min", "Mara Voss", "All levels", "12 spots", "Platform", "The second barbell touch of the week. Same patterns, different loads."),
    session("wed-sprint", "Sprint Circuit", "Conditioning", "Wed", "Wednesday", "12:10", "35 min", "Idris Hale", "All levels", "16 spots", "Kiln Floor", "Short and mean. Thirty-five minutes, and that includes the warm-up."),
    session("wed-ride", "Volt Ride", "Ride", "Wed", "Wednesday", "17:30", "45 min", "Noor Elian", "All levels", "14 bikes", "Spoke Room", "Same hour as Monday, different profile. Hold the note, then change it."),
    session("wed-skills", "Barbell Skills", "Strength", "Wed", "Wednesday", "19:15", "60 min", "Jun Park", "New to the platform", "12 spots", "Platform", "For people who want the lifts explained before the load goes up."),
    session("thu-power", "Power Clean Lab", "Strength", "Thu", "Thursday", "6:30", "60 min", "Jun Park", "Intermediate", "12 spots", "Platform", "One lift, lots of reps, at a weight you can keep honest."),
    session("thu-engine", "Engine Block", "Conditioning", "Thu", "Thursday", "9:15", "40 min", "Idris Hale", "All levels", "16 spots", "Kiln Floor", "The morning engine, repeated so you can see the week change."),
    session("thu-glide", "Ride & Glide", "Ride", "Thu", "Thursday", "18:00", "45 min", "Noor Elian", "All levels", "14 bikes", "Spoke Room", "More cadence, fewer heroics. Aerobic work you can talk through in pieces."),
    session("thu-joint", "Joint Clinic", "Mobility", "Thu", "Thursday", "19:15", "45 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "The joints you keep skipping. Knees, shoulders, and ankles, with a coach watching."),
    session("fri-galv", "Full Galvanize", "Conditioning", "Fri", "Friday", "6:15", "45 min", "Mara Voss", "All levels", "16 spots", "Kiln Floor", "Mara's Friday. Mixed implements, a hard finish, and then the weekend."),
    session("fri-noon", "Noon Ride", "Ride", "Fri", "Friday", "12:00", "40 min", "Noor Elian", "All levels", "14 bikes", "Spoke Room", "A midday spin that doesn't wreck Saturday's On-Ramp."),
    session("fri-iron", "Iron Hour", "Strength", "Fri", "Friday", "17:30", "55 min", "Jun Park", "All levels", "12 spots", "Platform", "Last barbell of the week. Leave a little so Sunday doesn't hurt for nothing."),
    session("fri-unwind", "Friday Unwind", "Restore", "Fri", "Friday", "19:00", "45 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "The week exhales. Easy breathing and positions you can hold."),
    session("sat-ramp", "On-Ramp", "Conditioning", "Sat", "Saturday", "8:15", "45 min", "Leo Marchetti", "New athletes", "12 spots", "Kiln Floor", "Your first hour. How the floor works, how the clock works, no audience."),
    session("sat-club", "Strength Club", "Strength", "Sat", "Saturday", "9:15", "55 min", "Mara Voss", "All levels", "12 spots", "Platform", "Weekend barbell. The cycle, coached, without the 6 a.m. alarm."),
    session("sat-ride", "Long Ride", "Ride", "Sat", "Saturday", "10:30", "50 min", "Noor Elian", "All levels", "14 bikes", "Spoke Room", "The longest ride on the board. Steady, with one hill that earns the name."),
    session("sat-kiln", "Weekend Kiln", "Conditioning", "Sat", "Saturday", "11:40", "40 min", "Idris Hale", "All levels", "16 spots", "Kiln Floor", "A late-morning piece for people who slept in and still want the work."),
    session("sun-range", "Open Range", "Mobility", "Sun", "Sunday", "9:00", "45 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "Unhurried range before the community hour. Come even if you're sore."),
    session("sun-wod", "Community WOD", "Conditioning", "Sun", "Sunday", "10:15", "40 min", "Leo Marchetti", "All levels", "16 spots", "Kiln Floor", "The social hour that still trains. Partners only if the cap allows."),
    session("sun-restore", "Restore Room", "Restore", "Sun", "Sunday", "16:00", "50 min", "Sable Quinn", "All levels", "10 spots", "Quiet Bay", "Last session of the week. Leave quieter than you arrived."),
]

BLANK_SESSION = {key: "" for key in CLASSES[0]}

COACHES: list[dict[str, str]] = [
    {
        "id": "mara",
        "name": "Mara Voss",
        "role": "Head of strength",
        "years": "11 years coaching",
        "focus": "Squat, press, pull",
        "signature": "Iron Hour",
        "letters": "MV",
        "accent": ORANGE,
        "ink": INK_DARK,
        "quote": "Load is a conversation. If you stop listening, the bar will finish the sentence.",
        "bio": "Mara writes the strength cycle and still coaches Monday Iron Hour herself. She came up in collegiate throws and cares about positions you can repeat when you are tired, not the single pretty rep in the mirror.",
    },
    {
        "id": "jun",
        "name": "Jun Park",
        "role": "Barbell",
        "years": "9 years coaching",
        "focus": "Olympic lifts",
        "signature": "Olympic Hour",
        "letters": "JP",
        "accent": RED,
        "ink": INK,
        "quote": "I will stop a set to fix a foot before I let you add load.",
        "bio": "Jun runs the platform like a classroom. Same warm-up positions, then the lift of the day. Olympic Hour and Power Clean Lab are his, and Barbell Skills is where new lifters learn the room before they chase numbers.",
    },
    {
        "id": "idris",
        "name": "Idris Hale",
        "role": "Conditioning",
        "years": "8 years coaching",
        "focus": "Engine and carries",
        "signature": "Engine Block",
        "letters": "IH",
        "accent": BLUE,
        "ink": INK_DARK,
        "quote": "The clock is a coach. Don't argue with it, and don't hide from it.",
        "bio": "Idris builds pieces you can finish. Intervals, carries, and machines, with the intended effort posted next to the reps. If a workout needs a paragraph of excuses, it does not make his board.",
    },
    {
        "id": "noor",
        "name": "Noor Elian",
        "role": "Ride",
        "years": "7 years coaching",
        "focus": "Cadence and hills",
        "signature": "Volt Ride",
        "letters": "NE",
        "accent": YELLOW,
        "ink": INK_DARK,
        "quote": "Hold the note. Then change it on purpose.",
        "bio": "Noor calls the Spoke Room. Hills, cadence drills, and a playlist that changes with the training cycle. She wants the room together, not fourteen people racing a screen they can't see.",
    },
    {
        "id": "sable",
        "name": "Sable Quinn",
        "role": "Mobility and restore",
        "years": "12 years coaching",
        "focus": "Range you can use",
        "signature": "Restore Room",
        "letters": "SQ",
        "accent": GREEN,
        "ink": INK_DARK,
        "quote": "Range you own is range you can use under a bar.",
        "bio": "Sable keeps the loud days from turning into a limp. Controlled range, breathing, and the unglamorous work that lets you squat again on Monday. Quiet Bay is hers, morning and night.",
    },
    {
        "id": "leo",
        "name": "Leo Marchetti",
        "role": "On-ramp and community",
        "years": "6 years coaching",
        "focus": "First hours",
        "signature": "On-Ramp",
        "letters": "LM",
        "accent": LIME,
        "ink": INK_DARK,
        "quote": "Nobody has to pretend they already belong here.",
        "bio": "Leo is who you meet first. Saturday On-Ramp is for people who have never touched a barbell on this floor. Sunday's Community WOD is the social hour that still trains. He learns names before he learns maxes.",
    },
]

PLANS = [
    {
        "id": "spark",
        "name": "Spark",
        "kicker": "6 classes a month",
        "blurb": "A lane you visit, not a second home.",
        "monthly": 98,
        "yearly_month": 84,
        "yearly_total": "1,008",
        "save": "168",
        "featured": False,
        "features": [
            "6 reserved classes",
            "Any lane, including ride",
            "Locker and shower",
            "Book from 24 hours out",
        ],
    },
    {
        "id": "current",
        "name": "Current",
        "kicker": "Unlimited classes",
        "blurb": "The membership most of the floor actually uses.",
        "monthly": 176,
        "yearly_month": 148,
        "yearly_total": "1,776",
        "save": "336",
        "featured": True,
        "features": [
            "Every class on the board",
            "Book from 48 hours out",
            "One guest pass a month",
            "Quarterly check-in with a coach",
        ],
    },
    {
        "id": "kiln",
        "name": "Kiln",
        "kicker": "Unlimited + coaching",
        "blurb": "For people who want the plan written with their name on it.",
        "monthly": 286,
        "yearly_month": 242,
        "yearly_total": "2,904",
        "save": "528",
        "featured": False,
        "features": [
            "Everything in Current",
            "Two personal sessions a month",
            "Programming notes between sessions",
            "A weekly bring-a-friend pass",
        ],
    },
]

PLAN_IDS = {plan["id"] for plan in PLANS}

TESTIMONIALS = [
    {
        "quote": "I stopped negotiating with my alarm. The room is small enough that someone notices if I don't show.",
        "name": "Priya D.",
        "meta": "Current · Harbor Row",
    },
    {
        "quote": "Sixteen people. A coach who knows your name and which knee you baby. That is the whole sales pitch.",
        "name": "Ellis M.",
        "meta": "Kiln · Old Kiln",
    },
    {
        "quote": "The Spoke Room is loud in the best way. Noor calls the change and the bikes actually stay together.",
        "name": "Camila R.",
        "meta": "Current · North Slip",
    },
    {
        "quote": "I came for the barbell and stayed for Sunday restore. My squat thanks Sable more than it thanks me.",
        "name": "Jonah P.",
        "meta": "Current · Lantern Hill",
    },
    {
        "quote": "It feels like a studio, not a sales floor. Nobody has tried to upgrade me in the lobby.",
        "name": "Ade O.",
        "meta": "Spark · West Meridian",
    },
    {
        "quote": "The programming changes before I get bored, and the cap means I can't hide in the back.",
        "name": "Ren S.",
        "meta": "Kiln · Glassworks",
    },
]

FAQS = [
    (
        "trial",
        "What happens on a trial?",
        "One class, any lane, on the house. You send the form, the desk answers, and you pick a session that is not already full. Volt Atelier is fictional: the request stays in this browser session and is not billed or sent anywhere.",
    ),
    (
        "freeze",
        "Can I freeze a membership?",
        "Current and Kiln can freeze once a year for up to 30 days. Spark does not freeze. Unused classes on Spark expire at the end of the month.",
    ),
    (
        "caps",
        "Are the caps real?",
        "Yes. The Platform holds 12, the Kiln Floor holds 16, the Spoke Room holds 14 bikes, and Quiet Bay holds 10. When a class is full, it is full. We do not pull in extra mats.",
    ),
    (
        "ride",
        "What if I only want to ride?",
        "Ride classes sit inside Current and Kiln. There is no separate cycling membership. Spark can be six rides if that is the lane you want.",
    ),
    (
        "new",
        "I'm new. Where do I start?",
        "Saturday On-Ramp, or Barbell Skills if you already like a barbell and want the platform explained. Say so on the form. Coaches scale the load. They do not scale the welcome.",
    ),
    (
        "medical",
        "Is the Body Lab medical advice?",
        "No. BMI and the calorie estimate are screening math for training, not a diagnosis. If you have a medical question, ask a clinician. Coaches will talk training. They will not pretend to be your doctor.",
    ),
]

HOURS = [
    ("Monday – Thursday", "5:45 – 21:00"),
    ("Friday", "5:45 – 20:00"),
    ("Saturday", "8:00 – 13:00"),
    ("Sunday", "8:30 – 17:30"),
]

VISIT = {
    "address": "18 Kiln Lane",
    "city": "Port Meridian",
    "email": "desk@voltatelier.example",
    "phone": "(555) 014-1880",
}

NAV = [
    ("Home", "/"),
    ("Week", "/schedule"),
    ("Plans", "/membership"),
    ("Coaches", "/coaches"),
    ("Lab", "/lab"),
]

SESSION_COUNT = len(CLASSES)
COACH_COUNT = len(COACHES)
LANE_COUNT = len(LANE_INFO)
FEATURED = next(item for item in CLASSES if item["key"] == "mon-ride")

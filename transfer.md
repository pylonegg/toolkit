Here’s a personal life-management database design you can use as a foundation. It’s structured like a real relational database, but it also works well if you later adapt it to Notion, Airtable, SQLite, or a simple app.

I’ll break it into core entities, then supporting areas, and finally optional advanced ideas.

⸻

1. Core Tables (People, You, Time)

Person

Stores everyone in your life (including yourself).

Field	Type	Notes
person_id	PK	Unique ID
first_name	Text	
last_name	Text	Optional
nickname	Text	
date_of_birth	Date	Optional
notes	Text	General notes
created_at	DateTime	


⸻

Relationship

Defines how you relate to people.

Field	Type	Notes
relationship_id	PK	
person_id	FK → Person	
relationship_type	Enum	friend, family, mentor, classmate, etc.
closeness_level	Integer (1–10)	Subjective
start_date	Date	
end_date	Date	Nullable
notes	Text	

👉 One person can have multiple relationship records over time.

⸻

Event

Anything that happens in your life.

Field	Type	Notes
event_id	PK	
title	Text	
description	Text	
event_type	Enum	social, school, work, personal
start_datetime	DateTime	
end_datetime	DateTime	
location	Text	
emotional_impact	Integer (-5 to +5)	Optional
notes	Text	


⸻

Event_Participant

Links people to events.

Field	Type
event_id	FK → Event
person_id	FK → Person
role	Text (host, attendee, etc.)


⸻

2. Preferences & Personality

Interest

Things you like or dislike.

Field	Type
interest_id	PK
name	Text
category	Enum (music, food, activity, topic)


⸻

Person_Interest

Tracks preferences over time.

Field	Type	Notes
person_id	FK → Person	
interest_id	FK → Interest	
preference_level	Integer (-5 to +5)	dislike → love
notes	Text	


⸻

Value

Core beliefs or priorities.

Field	Type
value_id	PK
name	Text
description	Text


⸻

Person_Value

Field	Type
person_id	FK → Person
value_id	FK → Value
importance_level	Integer (1–10)


⸻

3. Career / Education / Growth

Role

School, job, or responsibility.

Field	Type
role_id	PK
title	Text
organization	Text
role_type	Enum (school, job, project)
start_date	Date
end_date	Date
notes	Text


⸻

Skill

Field	Type
skill_id	PK
name	Text
category	Text


⸻

Person_Skill

Field	Type
person_id	FK → Person
skill_id	FK → Skill
proficiency_level	Integer (1–10)
last_practiced	Date


⸻

Goal

Tracks ambitions.

Field	Type
goal_id	PK
title	Text
category	career, personal, health
priority	Integer
start_date	Date
target_date	Date
status	Enum (planned, active, completed)


⸻

4. Health, Mood & Habits (Optional but Powerful)

Mood_Log

Field	Type
log_id	PK
date	Date
mood_level	Integer (1–10)
energy_level	Integer (1–10)
notes	Text


⸻

Habit

Field	Type
habit_id	PK
name	Text
category	health, study, social


⸻

Habit_Log

Field	Type
habit_id	FK → Habit
date	Date
completed	Boolean


⸻

5. Reflection & Memory

Journal_Entry

Field	Type
entry_id	PK
date	Date
title	Text
content	Text
related_event_id	FK → Event (nullable)


⸻

6. How Everything Connects (Big Picture)
	•	Person is the center
	•	People connect to:
	•	Relationships
	•	Events
	•	Interests
	•	Skills
	•	Values
	•	Events connect to:
	•	People
	•	Journal entries
	•	Emotional impact
	•	Goals connect to:
	•	Skills
	•	Roles
	•	Habits

⸻

7. Advanced Ideas (If You Want to Go Further)
	•	Life Phases (middle school, high school, gap year)
	•	Social Network Analysis (who you see most)
	•	Time Allocation Tracking
	•	Decision Log (big choices + outcomes)
	•	Privacy Levels per table or field

⸻

8. Practical Advice
	•	Start small: Person, Relationship, Event, Interest, Goal
	•	Add complexity only when it’s useful
	•	This works great in:
	•	Notion / Airtable
	•	SQLite + simple app
	•	Even Google Sheets (one table per sheet)

⸻

If you want, I can:
	•	Turn this into a Notion or Airtable template
	•	Draw an ER diagram
	•	Simplify it for a beginner version
	•	Customize it around school life, social life, or career planning

Just tell me 👍

------------------------
⸻

1. Core Tables (People, You, Time)

Person

Stores everyone in your life (including yourself).

Field	Type	Notes
person_id	PK	Unique ID
first_name	Text	
last_name	Text	Optional
nickname	Text	
date_of_birth	Date	Optional
notes	Text	General notes
created_at	DateTime	


⸻

Relationship

Defines how you relate to people.

Field	Type	Notes
relationship_id	PK	
person_id	FK → Person	
relationship_type	Enum	friend, family, mentor, classmate, etc.
closeness_level	Integer (1–10)	Subjective
start_date	Date	
end_date	Date	Nullable
notes	Text	

👉 One person can have multiple relationship records over time.

⸻

Event

Anything that happens in your life.

Field	Type	Notes
event_id	PK	
title	Text	
description	Text	
event_type	Enum	social, school, work, personal
start_datetime	DateTime	
end_datetime	DateTime	
location	Text	
emotional_impact	Integer (-5 to +5)	Optional
notes	Text	


⸻

Event_Participant

Links people to events.

Field	Type
event_id	FK → Event
person_id	FK → Person
role	Text (host, attendee, etc.)


⸻

2. Preferences & Personality

Interest

Things you like or dislike.

Field	Type
interest_id	PK
name	Text
category	Enum (music, food, activity, topic)


⸻

Person_Interest

Tracks preferences over time.

Field	Type	Notes
person_id	FK → Person	
interest_id	FK → Interest	
preference_level	Integer (-5 to +5)	dislike → love
notes	Text	


⸻

Value

Core beliefs or priorities.

Field	Type
value_id	PK
name	Text
description	Text


⸻

Person_Value

Field	Type
person_id	FK → Person
value_id	FK → Value
importance_level	Integer (1–10)


⸻

3. Career / Education / Growth

Role

School, job, or responsibility.

Field	Type
role_id	PK
title	Text
organization	Text
role_type	Enum (school, job, project)
start_date	Date
end_date	Date
notes	Text


⸻

Skill

Field	Type
skill_id	PK
name	Text
category	Text


⸻

Person_Skill

Field	Type
person_id	FK → Person
skill_id	FK → Skill
proficiency_level	Integer (1–10)
last_practiced	Date


⸻

Goal

Tracks ambitions.

Field	Type
goal_id	PK
title	Text
category	career, personal, health
priority	Integer
start_date	Date
target_date	Date
status	Enum (planned, active, completed)


⸻

4. Health, Mood & Habits (Optional but Powerful)

Mood_Log

Field	Type
log_id	PK
date	Date
mood_level	Integer (1–10)
energy_level	Integer (1–10)
notes	Text


⸻

Habit

Field	Type
habit_id	PK
name	Text
category	health, study, social


⸻

Habit_Log

Field	Type
habit_id	FK → Habit
date	Date
completed	Boolean


⸻

5. Reflection & Memory

Journal_Entry

Field	Type
entry_id	PK
date	Date
title	Text
content	Text
related_event_id	FK → Event (nullable)


⸻

6. How Everything Connects (Big Picture)
	•	Person is the center
	•	People connect to:
	•	Relationships
	•	Events
	•	Interests
	•	Skills
	•	Values
	•	Events connect to:
	•	People
	•	Journal entries
	•	Emotional impact
	•	Goals connect to:
	•	Skills
	•	Roles
	•	Habits

⸻

7. Advanced Ideas (If You Want to Go Further)
	•	Life Phases (middle school, high school, gap year)
	•	Social Network Analysis (who you see most)
	•	Time Allocation Tracking
	•	Decision Log (big choices + outcomes)
	•	Privacy Levels per table or field

⸻

8. Practical Advice
	•	Start small: Person, Relationship, Event, Interest, Goal
	•	Add complexity only when it’s useful
	•	This works great in:
	•	Notion / Airtable
	•	SQLite + simple app
	•	Even Google Sheets (one table per sheet)

⸻

If you want, I can:
	•	Turn this into a Notion or Airtable template
	•	Draw an ER diagram
	•	Simplify it for a beginner version
	•	Customize it around school life, social life, or career planning

Just tell me 👍
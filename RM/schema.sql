/* =========================================================
   1. Core Tables (People, Relationships, Events)
   ========================================================= */

CREATE TABLE Person (
    person_id INT IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NULL,
    nickname VARCHAR(100) NULL,
    date_of_birth DATE NULL,
    notes VARCHAR(MAX) NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Relationship (
    relationship_id INT IDENTITY PRIMARY KEY,
    person_id INT NOT NULL,
    relationship_type VARCHAR(50) NOT NULL,
    closeness_level INT CHECK (closeness_level BETWEEN 1 AND 10),
    start_date DATE NULL,
    end_date DATE NULL,
    notes VARCHAR(MAX) NULL,
    CONSTRAINT FK_Relationship_Person
        FOREIGN KEY (person_id) REFERENCES Person(person_id),
    CONSTRAINT CK_Relationship_Type
        CHECK (relationship_type IN ('friend', 'family', 'mentor', 'classmate', 'coworker', 'other'))
);

CREATE TABLE Event (
    event_id INT IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(MAX) NULL,
    event_type VARCHAR(50) NOT NULL,
    start_datetime DATETIME2 NOT NULL,
    end_datetime DATETIME2 NULL,
    location VARCHAR(255) NULL,
    emotional_impact INT CHECK (emotional_impact BETWEEN -5 AND 5),
    notes VARCHAR(MAX) NULL,
    CONSTRAINT CK_Event_Type
        CHECK (event_type IN ('social', 'school', 'work', 'personal'))
);

CREATE TABLE Event_Participant (
    event_id INT NOT NULL,
    person_id INT NOT NULL,
    role VARCHAR(50) NULL,
    CONSTRAINT PK_Event_Participant PRIMARY KEY (event_id, person_id),
    CONSTRAINT FK_EventParticipant_Event
        FOREIGN KEY (event_id) REFERENCES Event(event_id),
    CONSTRAINT FK_EventParticipant_Person
        FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

/* =========================================================
   2. Preferences & Personality
   ========================================================= */

CREATE TABLE Interest (
    interest_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    CONSTRAINT CK_Interest_Category
        CHECK (category IN ('music', 'food', 'activity', 'topic', 'other'))
);

CREATE TABLE Person_Interest (
    person_id INT NOT NULL,
    interest_id INT NOT NULL,
    preference_level INT CHECK (preference_level BETWEEN -5 AND 5),
    notes VARCHAR(MAX) NULL,
    CONSTRAINT PK_Person_Interest PRIMARY KEY (person_id, interest_id),
    CONSTRAINT FK_PersonInterest_Person
        FOREIGN KEY (person_id) REFERENCES Person(person_id),
    CONSTRAINT FK_PersonInterest_Interest
        FOREIGN KEY (interest_id) REFERENCES Interest(interest_id)
);

CREATE TABLE Value (
    value_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(MAX) NULL
);

CREATE TABLE Person_Value (
    person_id INT NOT NULL,
    value_id INT NOT NULL,
    importance_level INT CHECK (importance_level BETWEEN 1 AND 10),
    CONSTRAINT PK_Person_Value PRIMARY KEY (person_id, value_id),
    CONSTRAINT FK_PersonValue_Person
        FOREIGN KEY (person_id) REFERENCES Person(person_id),
    CONSTRAINT FK_PersonValue_Value
        FOREIGN KEY (value_id) REFERENCES Value(value_id)
);

/* =========================================================
   3. Career / Education / Growth
   ========================================================= */

CREATE TABLE Role (
    role_id INT IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    organization VARCHAR(255) NULL,
    role_type VARCHAR(50) NOT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    notes VARCHAR(MAX) NULL,
    CONSTRAINT CK_Role_Type
        CHECK (role_type IN ('school', 'job', 'project'))
);

CREATE TABLE Skill (
    skill_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NULL
);

CREATE TABLE Person_Skill (
    person_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level INT CHECK (proficiency_level BETWEEN 1 AND 10),
    last_practiced DATE NULL,
    CONSTRAINT PK_Person_Skill PRIMARY KEY (person_id, skill_id),
    CONSTRAINT FK_PersonSkill_Person
        FOREIGN KEY (person_id) REFERENCES Person(person_id),
    CONSTRAINT FK_PersonSkill_Skill
        FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);

CREATE TABLE Goal (
    goal_id INT IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority INT NULL,
    start_date DATE NULL,
    target_date DATE NULL,
    status VARCHAR(50) NOT NULL,
    CONSTRAINT CK_Goal_Category
        CHECK (category IN ('career', 'personal', 'health')),
    CONSTRAINT CK_Goal_Status
        CHECK (status IN ('planned', 'active', 'completed'))
);

/* =========================================================
   4. Health, Mood & Habits
   ========================================================= */

CREATE TABLE Mood_Log (
    log_id INT IDENTITY PRIMARY KEY,
    log_date DATE NOT NULL,
    mood_level INT CHECK (mood_level BETWEEN 1 AND 10),
    energy_level INT CHECK (energy_level BETWEEN 1 AND 10),
    notes VARCHAR(MAX) NULL
);

CREATE TABLE Habit (
    habit_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    CONSTRAINT CK_Habit_Category
        CHECK (category IN ('health', 'study', 'social', 'other'))
);

CREATE TABLE Habit_Log (
    habit_id INT NOT NULL,
    log_date DATE NOT NULL,
    completed BIT NOT NULL,
    CONSTRAINT PK_Habit_Log PRIMARY KEY (habit_id, log_date),
    CONSTRAINT FK_HabitLog_Habit
        FOREIGN KEY (habit_id) REFERENCES Habit(habit_id)
);

/* =========================================================
   5. Reflection & Memory
   ========================================================= */

CREATE TABLE Journal_Entry (
    entry_id INT IDENTITY PRIMARY KEY,
    entry_date DATE NOT NULL,
    title VARCHAR(255) NULL,
    content VARCHAR(MAX) NOT NULL,
    related_event_id INT NULL,
    CONSTRAINT FK_JournalEntry_Event
        FOREIGN KEY (related_event_id) REFERENCES Event(event_id)
);
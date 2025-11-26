prompt_decide_actions = """You are my executive assistant. Determine if the following email requires a reply.\n
Respond ONLY "TASKS" if it has tasks to be completed.
Respond ONLY "YES" if it requires a response but no tasks to be completed.
Respond ONLY "NO" if no action is needed."""


prompt_generate_reply = """Draft a professional, clear conversational reply to the following email. Write the best possible draft.
Give a detailed breakdown of how to achieve tasks if any are mentioned."""
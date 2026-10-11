prompt = f"""
Analyze the job description against only the provided resume information.

JOB DESCRIPTION:
{data.text}

RELEVANT RESUME INFORMATION:
{retrieved_chunks}

IMPORTANT RULES:
- Use only the information provided in the relevant resume information.
- Do not invent, assume, or infer experience that is not explicitly stated.
- If a skill or experience is not mentioned, say "Not mentioned in the provided resume."
- Do not treat unrelated experience as direct experience.
- Clearly separate direct matches from partial or transferable matches.
- Do not use general knowledge to establish a match.
- A skill is a DIRECT MATCH only when the supplied resume information explicitly states that skill.
- Do not say that one technology is relevant to another technology unless the resume itself establishes that relationship.
- When evidence is insufficient, write "Insufficient evidence in the provided resume."

TASK:

1. DIRECT MATCHES
   - List only skills or experience explicitly supported by the resume.

2. PARTIAL / TRANSFERABLE MATCHES
   - Only include these when the supplied resume provides actual evidence of a related skill or experience.
   - Do not create a transferable relationship merely because two technologies are commonly used together.

3. MISSING REQUIREMENTS
   - List job requirements that are not supported by the provided resume information.

4. EVIDENCE
   - Explain the important claims using evidence from the provided resume information.

5. SUMMARY
   - Give a concise factual summary.
   - Do not invent experience.
   - Do not call something a direct match unless the resume explicitly supports it.
"""
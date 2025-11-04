def validate_mcq(mcq):
    
    keys = {"question", "choices", "answer_index", "explanation", "difficulty_score"}
    if not keys.issubset(mcq.keys()):
        return False, "Missing keys"
    if not isinstance(mcq["choices"], list) or len(mcq["choices"]) != 4:
        return False, "Choices must be list of 4"
    ai = mcq["answer_index"]
    if not (isinstance(ai, int) and 0 <= ai < 4):
        return False, "answer_index must be 0..3"
    # Basic content checks
    if len(set(mcq["choices"])) < 4:
        return False, "Duplicate choices"
    # Difficulty check
    if not (1 <= int(mcq["difficulty_score"]) <= 10):
        return False, "difficulty_score must be 1..10"
        
    return True, None
import T7Weighted
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Publication

/-- Exact crude-budget value at the reviewed beta exponent. -/
theorem beta564_budget : (2^54 : Rat)*(2^450/(2^564)) = 1/2^60 := by decide +kernel

/-- Reducing the exponent by one doubles this crude budget. -/
theorem beta563_budget : (2^54 : Rat)*(2^450/(2^563)) = 1/2^59 := by decide +kernel

/-- A conclusive inequality; the original audit's failed reduction did not establish this. -/
theorem beta563_exceeds_threshold : (1/2^60 : Rat) < (2^54 : Rat)*(2^450/(2^563)) := by decide +kernel

/-- This concerns the crude proof budget, not the truth of the headline at a changed beta. -/
theorem beta563_not_same_budget : (2^54 : Rat)*(2^450/(2^563)) ≠ 1/2^60 := by decide +kernel

end T7Publication
#print axioms T7Publication.beta564_budget
#print axioms T7Publication.beta563_budget
#print axioms T7Publication.beta563_exceeds_threshold
#print axioms T7Publication.beta563_not_same_budget

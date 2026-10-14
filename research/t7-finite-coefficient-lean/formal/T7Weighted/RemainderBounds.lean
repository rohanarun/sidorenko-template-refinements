import T7Weighted.SourceConstants
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

theorem non_orbit_term_lower (g : TypeMap) (hi : g ≠ identityMap) (hr : g ≠ reversalMap) :
    -(2^450/beta:Rat) ≤ weightedTerm g := by
  by_cases hm : score g.1 g.2 = 5066
  · rw [weightedTerm,maximum_coefficient_support g hm hi hr,Rat.zero_mul]
    have h : 0 < (2^450/beta:Rat) := Rat.mul_pos (by decide +kernel) (Rat.inv_pos.mpr beta_positive)
    grind only
  · have hs := score_le_max g.1 g.2
    have hlt : score g.1 g.2 < 5066 := by omega
    have hw := relativeWeight_lower_score g hlt
    have hp : 0 ≤ relativeWeight g := by have h := relativeWeight_positive g; grind only
    have hc := (generalCoefficient_bounds g.1 g.2).1
    have h1 := Rat.mul_le_mul_of_nonneg_right hc hp
    have h2 := Rat.mul_le_mul_of_nonneg_left hw (by decide +kernel : (0:Rat) ≤ 2^450)
    unfold weightedTerm
    grind only

/-- A two-sided bound on the concrete finite remainder, derived without a remainder premise. -/
theorem finiteRemainder_two_sided : -(1/2^60:Rat) < finiteRemainder ∧ finiteRemainder < 1/2^60 := by
  refine ⟨?_,finiteRemainder_bound⟩
  have hp : 0 < (2^450/beta:Rat) := Rat.mul_pos (by decide +kernel) (Rat.inv_pos.mpr beta_positive)
  have hterm (g : TypeMap) : -(2^450/beta:Rat) ≤ remainderTerm g := by
    unfold remainderTerm
    split
    · grind only
    · rename_i h
      exact non_orbit_term_lower g (fun hi => h (Or.inl hi)) (fun hr => h (Or.inr hr))
  have hs := rat_sum_le allTypeMaps (fun _ => -(2^450/beta:Rat)) remainderTerm (fun g _ => hterm g)
  rw [rat_sum_const] at hs
  have hc := Rat.mul_lt_mul_of_pos_right allTypeMaps_count hp
  have he : (2^54:Rat)*(2^450/beta) = 1/2^60 := by decide +kernel
  rw [he] at hc
  have hn := Rat.neg_lt_neg hc
  have hm : (allTypeMaps.length:Rat)*-(2^450/beta:Rat) = -((allTypeMaps.length:Rat)*(2^450/beta:Rat)) := by grind only
  rw [hm] at hs
  exact Std.lt_of_lt_of_le hn hs

end T7Weighted

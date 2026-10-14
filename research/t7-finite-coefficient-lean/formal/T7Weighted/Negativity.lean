import T7Weighted.ActualWeights
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

/-- Flattening the actual independent type expectation, with its original prior and thinning weights. -/
theorem averagedCoefficient_raw_sum : averagedCoefficient =
    (allTypeMaps.map fun g => rawMapWeight g*generalCoefficient g.1 g.2).sum := by
  rw [averagedCoefficient_exact]
  have hp : pointPrior.outcomes = List.finRange 7 := rfl
  have hf : facePrior.outcomes = List.finRange 10 := rfl
  rw [hp,hf]
  unfold allTypeMaps
  simp only [List.map_flatMap,List.map_map,Function.comp_def,rat_sum_flatMap]
  congr 1
  apply List.map_congr_left
  intro a _
  rw [← rat_sum_mul]
  congr 1
  apply List.map_congr_left
  intro b _
  unfold rawMapWeight
  grind only

/-- Exact identification with the score-normalized sum; the scale is separately proved positive. -/
theorem averagedCoefficient_normalized : averagedCoefficient = averagedScale*normalizedWeightedSum := by
  rw [averagedCoefficient_raw_sum]
  unfold normalizedWeightedSum
  rw [← rat_sum_mul]
  congr 1
  apply List.map_congr_left
  intro g _
  rw [actual_weight_relative]
  unfold weightedTerm
  grind only

/-- Source formula (5)'s explicit strictly positive margin. -/
def eta : Rat := decay 8314/(2^60*pointNormalizer^7*faceNormalizer^10)

theorem eta_eq_scale : eta = averagedScale*(1/2^60:Rat) := by
  unfold eta averagedScale
  simp only [Rat.div_def,Rat.inv_mul_rev,Rat.one_mul]
  grind only

theorem eta_positive : 0 < eta := by
  rw [eta_eq_scale]
  exact Rat.mul_pos averagedScale_positive (by decide +kernel)

/-- The actual averaged stochastic coefficient is strictly negative, with no negativity or remainder premise. -/
theorem averagedCoefficient_negative : averagedCoefficient < -eta := by
  rw [averagedCoefficient_normalized,eta_eq_scale]
  have h := Rat.mul_lt_mul_of_pos_left normalizedWeightedSum_negative averagedScale_positive
  have he : averagedScale * -(1/2^60:Rat) = -(averagedScale*(1/2^60:Rat)) := by grind only
  rw [he] at h
  exact h

theorem averagedCoefficient_lt_zero : averagedCoefficient < 0 := by
  have h := averagedCoefficient_negative
  have hp := eta_positive
  grind only

end T7Weighted

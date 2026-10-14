import T7Weighted.Negativity
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

theorem pointNormalizer_source : pointNormalizer =
    2*decay 333+2*decay 592+2*decay 925+decay 1332 := by
  have h : (List.finRange 7).map pointRawMass =
      [decay 333,decay 592,decay 925,decay 1332,decay 925,decay 592,decay 333] := by
    rw [fin7]
    rfl
  unfold pointNormalizer
  rw [h]
  simp only [List.sum_cons,List.sum_nil]
  grind only

theorem faceNormalizer_source : faceNormalizer = 8*decay 3+2*decay 5 := by
  have h : (List.finRange 10).map faceRawMass =
      [decay 3,decay 3,decay 3,decay 5,decay 3,decay 3,decay 5,decay 3,decay 3,decay 3] := by
    rw [fin10]
    rfl
  unfold faceNormalizer
  rw [h]
  simp only [List.sum_cons,List.sum_nil]
  grind only

/-- The source's printed rational margin, with its normalizers fully expanded. -/
theorem eta_source : eta = (1/beta^8314) /
    (2^60*(2/beta^333+2/beta^592+2/beta^925+1/beta^1332)^7*(8/beta^3+2/beta^5)^10) := by
  unfold eta
  rw [pointNormalizer_source,faceNormalizer_source]
  simp only [decay,Rat.div_def,Rat.one_mul]

/-- The negative source coefficient has no hypotheses: all distributions and scores are instantiated. -/
theorem source_weighted_negativity :
    0 < eta ∧ averagedCoefficient < -eta := ⟨eta_positive,averagedCoefficient_negative⟩

end T7Weighted

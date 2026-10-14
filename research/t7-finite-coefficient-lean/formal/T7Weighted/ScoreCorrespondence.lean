import T7Weighted.Scores
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

theorem fin7 : List.finRange 7 = [0,1,2,3,4,5,6] := by decide +kernel

theorem fin10 : List.finRange 10 = [0,1,2,3,4,5,6,7,8,9] := by decide +kernel

theorem fin30 : List.finRange 30 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29] := by decide +kernel

theorem degree_0 : degree 0 = 3 := by decide +kernel

theorem degree_1 : degree 1 = 4 := by decide +kernel

theorem degree_2 : degree 2 = 5 := by decide +kernel

theorem degree_3 : degree 3 = 6 := by decide +kernel

theorem degree_4 : degree 4 = 5 := by decide +kernel

theorem degree_5 : degree 5 = 4 := by decide +kernel

theorem degree_6 : degree 6 = 3 := by decide +kernel

/-- The score is precisely the source prior/pair exponent, not an independently chosen ranking. -/
theorem sourceScore_eq_score (a : Point → Point) (b : Face → Face) : sourceScore a b = score a b := by
  unfold sourceScore score pointLoss faceScore pairScore
  simp only [fin7,fin10,fin30,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,
    corner,face]
  simp only [degree_0,degree_1,degree_2,degree_3,degree_4,degree_5,degree_6,
    Int.natCast_add,Int.natCast_mul]
  grind only

end T7Weighted

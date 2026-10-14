import T7.Orbit
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7

/-- Product of the actual rational moments equals the numerator product divided by 4^length. -/
theorem product_common_denominator (xs : List Int) :
    (xs.map fun (x : Int) => (x : Rat)/4).prod = (xs.prod : Rat)/4^xs.length := by
  induction xs with
  | nil => decide +kernel
  | cons x xs ih =>
    simp only [List.map_cons, List.prod_cons, List.length_cons, Rat.intCast_mul, Rat.pow_succ]
    rw [ih]
    simp only [Rat.div_def, Rat.inv_mul_rev]
    grind

theorem sum_common_denominator (xs : List Int) (den : Rat) :
    (xs.map fun (x : Int) => (x : Rat)/den).sum = (xs.sum : Rat)/den := by
  induction xs with
  | nil => simp [Rat.div_def]
  | cons x xs ih =>
    simp only [List.map_cons, List.sum_cons, Rat.intCast_add]
    rw [ih]
    grind

theorem term_is_product (a : Labeling) : term a =
    ((List.finRange 30).map fun c => moment c (a (leftEdge c)) (a (rightEdge c))).prod := by
  have hp := product_common_denominator
    ((List.finRange 30).map fun c => momentNumerator c (a (leftEdge c)) (a (rightEdge c)))
  simp only [List.map_map, List.length_map] at hp
  exact hp.symm

theorem full_coefficient_is_sum_of_products : fullCoefficient =
    (allLabelings.map fun a =>
      ((List.finRange 30).map fun c => moment c (a (leftEdge c)) (a (rightEdge c))).prod).sum := by
  have hs := sum_common_denominator (allLabelings.map termNumerator) (4^30)
  simp only [List.map_map] at hs
  change fullCoefficient = (allLabelings.map fun a => _).sum
  unfold fullCoefficient
  rw [← hs]
  congr 1
  apply List.map_congr_left
  intro a _
  exact term_is_product a

def reverseTerm (a : Labeling) : Rat := (reverseTermNumerator a : Rat)/4^30

theorem reverse_term_is_product (a : Labeling) : reverseTerm a =
    ((List.finRange 30).map fun c => moment (reverseCorner c) (a (leftEdge c)) (a (rightEdge c))).prod := by
  have hp := product_common_denominator
    ((List.finRange 30).map fun c => momentNumerator (reverseCorner c) (a (leftEdge c)) (a (rightEdge c)))
  simp only [List.map_map, List.length_map] at hp
  exact hp.symm

theorem reverse_coefficient_is_sum_of_products : reverseFullCoefficient =
    (allLabelings.map fun a =>
      ((List.finRange 30).map fun c => moment (reverseCorner c) (a (leftEdge c)) (a (rightEdge c))).prod).sum := by
  have hs := sum_common_denominator (allLabelings.map reverseTermNumerator) (4^30)
  simp only [List.map_map] at hs
  change reverseFullCoefficient = (allLabelings.map fun a => _).sum
  unfold reverseFullCoefficient
  rw [← hs]
  congr 1
  apply List.map_congr_left
  intro a _
  exact reverse_term_is_product a

end T7

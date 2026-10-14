import T7Weighted.ScoreCorrespondence
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

theorem rat_sum_le (xs : List α) (f g : α → Rat) (h : ∀ x ∈ xs, f x ≤ g x) :
    (xs.map f).sum ≤ (xs.map g).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht := ih (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons,List.sum_cons]
    grind only

theorem mean_mono (law : FiniteLaw α) (f g : α → Rat)
    (h : ∀ x ∈ law.outcomes, f x ≤ g x) : law.mean f ≤ law.mean g := by
  apply rat_sum_le
  intro x hx
  exact Rat.mul_le_mul_of_nonneg_left (h x hx) (law.nonnegative x hx)

theorem pairFeature_values (p : Point) (j : Face) (a : Mask) (o : ActivationOutcome) :
    pairFeature p j a o = -1 ∨ pairFeature p j a o = 0 ∨ pairFeature p j a o = 1 := by
  unfold pairFeature phi
  split
  · split
    · have h := char_sign a o.2
      grind only
    · right; left; rfl
  · split
    · right; right; rfl
    · right; left; rfl

theorem pairMoment_bounds (p : Point) (j : Face) (a b : Mask) :
    -1 ≤ pairMoment p j a b ∧ pairMoment p j a b ≤ 1 := by
  have bounds (o : ActivationOutcome) : -1 ≤ pairFeature p j a o*pairFeature p j b o ∧
      pairFeature p j a o*pairFeature p j b o ≤ 1 := by
    have ha := pairFeature_values p j a o
    have hb := pairFeature_values p j b o
    rcases ha with ha | ha | ha <;> rcases hb with hb | hb | hb <;> rw [ha,hb] <;> decide +kernel
  have hlo := mean_mono (activationLaw (cornerIndex p j)) (fun _ => -1)
    (fun o => pairFeature p j a o*pairFeature p j b o) (fun o _ => (bounds o).1)
  have hhi := mean_mono (activationLaw (cornerIndex p j))
    (fun o => pairFeature p j a o*pairFeature p j b o) (fun _ => 1) (fun o _ => (bounds o).2)
  rw [FiniteLaw.mean_const] at hlo hhi
  exact ⟨hlo,hhi⟩

theorem product_unit_bounds (xs : List Rat) (h : ∀ x ∈ xs, -1 ≤ x ∧ x ≤ 1) :
    -1 ≤ xs.prod ∧ xs.prod ≤ 1 := by
  induction xs with
  | nil => simp; decide +kernel
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht := ih (fun y hy => h y (by simp [hy]))
    have hu := interval_product_upper x xs.prod 1 (by decide +kernel) hx.1 hx.2 ht.1 ht.2
    have hneg0 : -(1:Rat) ≤ -x := by grind only
    have hneg1 : -x ≤ (1:Rat) := by grind only
    have hl := interval_product_upper (-x) xs.prod 1 (by decide +kernel) hneg0 hneg1 ht.1 ht.2
    simp only [List.prod_cons]
    grind only

theorem rat_sum_const (xs : List α) (r : Rat) : (xs.map fun _ => r).sum = (xs.length:Rat)*r := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp only [List.map_cons,List.sum_cons,List.length_cons,ih]; grind only

theorem flatMap_length_uniform (xs : List α) (f : α → List β) (n : Nat)
    (h : ∀ x ∈ xs, (f x).length = n) : (xs.flatMap f).length = xs.length*n := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht := ih (fun y hy => h y (by simp [hy]))
    simp only [List.flatMap_cons,List.length_append,List.length_cons,hx,ht]
    grind only

theorem functions_length (xs : List α) (n : Nat) : (functions xs n).length = xs.length^n := by
  induction n with
  | zero => simp [functions]
  | succ n ih =>
    rw [functions,flatMap_length_uniform xs _ (xs.length^n)]
    · simp only [Nat.pow_succ]; grind only
    · intro x _
      rw [List.length_map,ih]

theorem labels_count_bound : allLabelings.length ≤ 2^450 := by
  have hm : nonemptyMasks.length ≤ 2^30 := by
    have h := List.length_filter_le (fun a => decide (NonemptyMask a)) allMasks
    change (allMasks.filter fun a => decide (NonemptyMask a)).length ≤ _ at h
    have hlen : allMasks.length = 2^30 := functions_length [false,true] 30
    rw [hlen] at h
    exact h
  change (functions nonemptyMasks 15).length ≤ _
  rw [functions_length]
  have h := Nat.pow_le_pow_left hm 15
  have he : (2^30:Nat)^15 = 2^450 := by decide +kernel
  rw [he] at h
  exact h

/-- Uniform finite bound for every full coefficient, derived from actual random features. -/
theorem generalCoefficient_bounds (a : Point → Point) (b : Face → Face) :
    -(2^450:Rat) ≤ generalCoefficient a b ∧ generalCoefficient a b ≤ 2^450 := by
  let term := fun labels : Labeling => ((List.finRange 30).map fun c =>
    pairMoment (a (corner c).1) (b (corner c).2) (labels (leftEdge c)) (labels (rightEdge c))).prod
  have ht (labels : Labeling) : -1 ≤ term labels ∧ term labels ≤ 1 := by
    apply product_unit_bounds
    intro x hx
    obtain ⟨c,hc,rfl⟩ := List.mem_map.mp hx
    exact pairMoment_bounds _ _ _ _
  have hl := rat_sum_le allLabelings (fun _ => -1) term (fun l _ => (ht l).1)
  have hh := rat_sum_le allLabelings term (fun _ => 1) (fun l _ => (ht l).2)
  rw [rat_sum_const] at hl hh
  have hn : (allLabelings.length:Rat) ≤ (2^450:Nat) := Rat.natCast_le_natCast.mpr labels_count_bound
  change (allLabelings.map term).sum ≥ -(2^450:Rat) ∧ (allLabelings.map term).sum ≤ 2^450
  grind only

end T7Weighted

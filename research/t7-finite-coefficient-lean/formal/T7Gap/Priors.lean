import T7Gap.ProductLaw
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

theorem rat_sum_pos (xs : List α) (w : α → Rat) (hn : ∀ x ∈ xs, 0 ≤ w x)
    (hp : ∃ x ∈ xs, 0 < w x) : 0 < (xs.map w).sum := by
  induction xs with
  | nil => simp at hp
  | cons x xs ih =>
    have h0 := hn x (by simp)
    have htail : ∀ y ∈ xs, 0 ≤ w y := fun y hy => hn y (by simp [hy])
    obtain ⟨y,hy,hyp⟩ := hp
    rcases List.mem_cons.mp hy with he | ht
    · subst y
      have hnon := sum_rat_nonneg xs w htail
      simp only [List.map_cons,List.sum_cons]
      grind only
    · have hpos := ih htail ⟨y,ht,hyp⟩
      simp only [List.map_cons,List.sum_cons]
      grind only

def normalizedLaw (xs : List α) (w : α → Rat)
    (hn : ∀ x ∈ xs, 0 ≤ w x) (hp : 0 < (xs.map w).sum) : FiniteLaw α where
  outcomes := xs
  weight := fun x => w x/(xs.map w).sum
  nonnegative := by
    intro x hx
    have hi := Rat.inv_pos.mpr hp
    have hni : 0 ≤ ((xs.map w).sum)⁻¹ := by grind only
    exact Rat.mul_nonneg (hn x hx) hni
  normalized := by
    rw [rat_sum_div]
    have hz : (xs.map w).sum ≠ 0 := by grind only
    exact Rat.mul_inv_cancel _ hz

def beta : Rat := 2^564

def faceHistogram (j : Face) (d : Nat) : Nat := ((face j).filter fun p => degree p == d).length
def faceNorm (j : Face) : Nat := ((List.range 4).map fun k => (faceHistogram j (k+3))^2).sum

def pointRawMass (p : Point) : Rat := 1/beta^(37*(degree p)^2)
def faceRawMass (j : Face) : Rat := 1/beta^(faceNorm j)

theorem beta_positive : 0 < beta := Rat.pow_pos (by decide +kernel)

theorem reciprocal_beta_power_positive (n : Nat) : 0 < 1/beta^n := by
  have h := Rat.inv_pos.mpr (Rat.pow_pos (n := n) beta_positive)
  simpa only [Rat.div_def,Rat.one_mul] using h

theorem pointMass_nonnegative (p : Point) : 0 ≤ pointRawMass p := by
  have h := reciprocal_beta_power_positive (37*(degree p)^2)
  change 0 ≤ 1/beta^(37*(degree p)^2)
  grind only

theorem faceMass_nonnegative (j : Face) : 0 ≤ faceRawMass j := by
  have h := reciprocal_beta_power_positive (faceNorm j)
  change 0 ≤ 1/beta^(faceNorm j)
  grind only

def pointPrior : FiniteLaw Point := normalizedLaw (List.finRange 7) pointRawMass
  (fun p _ => pointMass_nonnegative p) (rat_sum_pos _ _ (fun p _ => pointMass_nonnegative p)
    ⟨0,List.mem_finRange _,reciprocal_beta_power_positive _⟩)

def facePrior : FiniteLaw Face := normalizedLaw (List.finRange 10) faceRawMass
  (fun j _ => faceMass_nonnegative j) (rat_sum_pos _ _ (fun j _ => faceMass_nonnegative j)
    ⟨0,List.mem_finRange _,reciprocal_beta_power_positive _⟩)

theorem literal_face_norms : List.ofFn faceNorm = [3,3,3,5,3,3,5,3,3,3] := by decide +kernel

def pairScore (p : Point) (j : Face) : Nat := 74*degree p+2*faceHistogram j (degree p)
def thinning (p : Point) (j : Face) : Rat := 1/beta^(446-pairScore p j)

theorem pairScore_bound : ∀ p j, pairScore p j ≤ 446 := by decide +kernel

theorem power_ge_one (x : Rat) (hx : 1 ≤ x) (n : Nat) : 1 ≤ x^n := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hn : 0 ≤ x := by grind only
    have h := Rat.mul_le_mul_of_nonneg_right ih hn
    rw [Rat.pow_succ]
    grind only

theorem thinning_bounds (p : Point) (j : Face) : 0 < thinning p j ∧ thinning p j ≤ 1 := by
  have hp := reciprocal_beta_power_positive (446-pairScore p j)
  have hb : 1 ≤ beta := power_ge_one 2 (by decide +kernel) 564
  have hq := power_ge_one beta hb (446-pairScore p j)
  have hqi : 0 ≤ (beta^(446-pairScore p j))⁻¹ := by
    have h := Rat.inv_pos.mpr (Rat.pow_pos (n := 446-pairScore p j) beta_positive)
    grind only
  have hm := Rat.mul_le_mul_of_nonneg_right hq hqi
  have hn : beta^(446-pairScore p j) ≠ 0 := by
    have h := Rat.pow_pos (n := 446-pairScore p j) beta_positive
    grind only
  have hc := Rat.mul_inv_cancel (beta^(446-pairScore p j)) hn
  change 0 < 1/beta^(446-pairScore p j) ∧ 1/beta^(446-pairScore p j) ≤ 1
  grind only

end T7Gap

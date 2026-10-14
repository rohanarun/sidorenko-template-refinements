import T7Weighted.WeightedNumerator
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Weighted
open T7 T7Gap

def exponentCost (a : Point → Point) (b : Face → Face) : Nat :=
  ((List.finRange 7).map fun p => 37*(degree (a p))^2).sum +
  ((List.finRange 10).map fun j => faceNorm (b j)).sum +
  ((List.finRange 30).map fun c => 446-pairScore (a (corner c).1) (b (corner c).2)).sum

theorem int_sum_natCast (xs : List α) (f : α → Nat) :
    ((xs.map f).sum : Int) = (xs.map fun x => (f x : Int)).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons,List.sum_cons,Int.natCast_add,ih]

theorem thinning_exponent_int (p : Point) (j : Face) :
    ((446-pairScore p j : Nat):Int) = 446-(pairScore p j:Int) := by
  have h := pairScore_bound p j
  omega

/-- The nonnegative exponent cost comes from exactly the prior and thinning powers in the kernel. -/
theorem exponentCost_sourceScore (a : Point → Point) (b : Face → Face) :
    (exponentCost a b : Int)+sourceScore a b = 13380 := by
  unfold exponentCost sourceScore
  simp only [Int.natCast_add,int_sum_natCast,thinning_exponent_int,int_sum_sub]
  have hconst : ((List.finRange 30).map fun _ => (446:Int)).sum = 13380 := by decide +kernel
  rw [hconst]
  have he (p : Point) : ((37*(degree (a p))^2:Nat):Int) = (37:Int)*(degree (a p):Int)^2 := by grind only
  simp only [he]
  grind only

theorem exponentCost_gap (a : Point → Point) (b : Face → Face) :
    exponentCost a b = 8314+(5066-score a b).toNat := by
  have h := exponentCost_sourceScore a b
  rw [sourceScore_eq_score] at h
  have hb := score_le_max a b
  omega

def decay (n : Nat) : Rat := 1/beta^n

theorem decay_zero : decay 0 = 1 := by simp [decay]; decide +kernel

theorem rat_pow_add (x : Rat) (m n : Nat) : x^(m+n) = x^m*x^n := by
  induction n with
  | zero => simp
  | succ n ih => simp only [Nat.add_succ,Rat.pow_succ,ih]; exact Rat.mul_assoc _ _ _

theorem decay_add (m n : Nat) : decay (m+n) = decay m*decay n := by
  simp only [decay,rat_pow_add,Rat.div_def,Rat.one_mul,Rat.inv_mul_rev]
  exact Rat.mul_comm _ _

theorem decay_product (xs : List α) (f : α → Nat) :
    (xs.map fun x => decay (f x)).prod = decay (xs.map f).sum := by
  induction xs with
  | nil => exact decay_zero.symm
  | cons x xs ih => simp only [List.map_cons,List.sum_cons,List.prod_cons,ih,decay_add]

def pointNormalizer : Rat := ((List.finRange 7).map pointRawMass).sum
def faceNormalizer : Rat := ((List.finRange 10).map faceRawMass).sum

theorem pointNormalizer_positive : 0 < pointNormalizer :=
  rat_sum_pos _ _ (fun p _ => pointMass_nonnegative p) ⟨0,List.mem_finRange _,reciprocal_beta_power_positive _⟩

theorem faceNormalizer_positive : 0 < faceNormalizer :=
  rat_sum_pos _ _ (fun j _ => faceMass_nonnegative j) ⟨0,List.mem_finRange _,reciprocal_beta_power_positive _⟩

theorem productWeight_decay (law : FiniteLaw α) (f : α → Nat) (Z : Rat)
    (h : ∀ x, law.weight x = decay (f x)/Z) (n : Nat) (s : Fin n → α) :
    productWeight law s = decay ((List.finRange n).map fun i => f (s i)).sum / Z^n := by
  induction n with
  | zero => simp [productWeight,List.finRange,decay_zero]; decide +kernel
  | succ n ih =>
    simp only [productWeight,List.finRange_succ,List.map_cons,List.map_map,Function.comp_def,List.sum_cons]
    rw [h,ih,decay_add,Rat.pow_succ]
    simp only [Rat.div_def,Rat.inv_mul_rev]
    grind only

def rawMapWeight (g : TypeMap) : Rat :=
  productWeight pointPrior g.1*productWeight facePrior g.2*
  ((List.finRange 30).map fun c => thinning (g.1 (corner c).1) (g.2 (corner c).2)).prod

theorem rawMapWeight_formula (g : TypeMap) : rawMapWeight g =
    decay (exponentCost g.1 g.2)/(pointNormalizer^7*faceNormalizer^10) := by
  unfold rawMapWeight
  rw [productWeight_decay pointPrior (fun p => 37*(degree p)^2) pointNormalizer (fun _ => rfl),
      productWeight_decay facePrior faceNorm faceNormalizer (fun _ => rfl)]
  have he : ((List.finRange 30).map fun c => thinning (g.1 (corner c).1) (g.2 (corner c).2)).prod =
      decay ((List.finRange 30).map fun c => 446-pairScore (g.1 (corner c).1) (g.2 (corner c).2)).sum :=
    decay_product _ _
  rw [he]
  unfold exponentCost
  rw [decay_add,decay_add]
  simp only [Rat.div_def,Rat.inv_mul_rev]
  grind only

/-- The positive scale in source formula (5), before division by 2^60. -/
def averagedScale : Rat := decay 8314/(pointNormalizer^7*faceNormalizer^10)

theorem averagedScale_positive : 0 < averagedScale :=
  Rat.mul_pos (reciprocal_beta_power_positive _) (Rat.inv_pos.mpr
    (Rat.mul_pos (Rat.pow_pos pointNormalizer_positive) (Rat.pow_pos faceNormalizer_positive)))

theorem actual_weight_relative (g : TypeMap) : rawMapWeight g = averagedScale*relativeWeight g := by
  rw [rawMapWeight_formula,exponentCost_gap,decay_add]
  unfold averagedScale relativeWeight
  change decay 8314*decay (5066-score g.1 g.2).toNat/(pointNormalizer^7*faceNormalizer^10) =
    decay 8314/(pointNormalizer^7*faceNormalizer^10)*decay (5066-score g.1 g.2).toNat
  grind only

end T7Weighted

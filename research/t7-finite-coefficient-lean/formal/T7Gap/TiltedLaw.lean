import T7Gap.Hypercube
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

structure FiniteLaw (α : Type) where
  outcomes : List α
  weight : α → Rat
  nonnegative : ∀ s ∈ outcomes, 0 ≤ weight s
  normalized : (outcomes.map weight).sum = 1

def FiniteLaw.mean (law : FiniteLaw α) (f : α → Rat) : Rat :=
  (law.outcomes.map fun s => law.weight s*f s).sum

def BitsEq (a b : Bits n) : Prop := ∀ i, a i = b i
instance (a b : Bits n) : Decidable (BitsEq a b) := inferInstanceAs (Decidable (∀ i, a i = b i))

theorem xor_zero_iff (a b : Bits n) : IsZero (xorBits a b) ↔ BitsEq a b := by
  constructor
  · intro h i
    have hi := h i
    unfold xorBits at hi
    cases ha : a i <;> cases hb : b i <;> simp_all
  · intro h i
    simp [xorBits,h i]

theorem cubeAvg_const (n : Nat) (r : Rat) : cubeAvg n (fun _ => r) = r := by
  unfold cubeAvg
  rw [cubeSum_const]
  have hn : (2:Rat)^n ≠ 0 := by have h := Rat.pow_pos (n := n) (by decide +kernel : (0:Rat)<2); grind
  have hi := Rat.mul_inv_cancel ((2:Rat)^n) hn
  grind

theorem rat_sum_div (xs : List α) (f : α → Rat) (den : Rat) :
    (xs.map fun s => f s/den).sum = (xs.map f).sum/den := by
  induction xs with
  | nil => simp [Rat.div_def]
  | cons x xs ih => simp only [List.map_cons,List.sum_cons]; rw [ih]; grind

def tiltedWeight (d : Bits n) (bias : Rat) (s : Bits n) : Rat :=
  (1+bias*char d s)/2^n

def tiltedExpectation (d : Bits n) (bias : Rat) (f : Bits n → Rat) : Rat :=
  ((functions [false,true] n).map fun s => tiltedWeight d bias s*f s).sum

theorem tiltedExpectation_formula (d : Bits n) (bias : Rat) (f : Bits n → Rat) :
    tiltedExpectation d bias f = cubeAvg n f+bias*cubeAvg n (fun s => char d s*f s) := by
  have he : (fun s => tiltedWeight d bias s*f s) =
      (fun s => (f s+bias*(char d s*f s))/2^n) := by
    funext s
    unfold tiltedWeight
    grind
  unfold tiltedExpectation
  rw [he,rat_sum_div]
  change cubeSum n (fun s => f s+bias*(char d s*f s))/2^n = _
  rw [cubeSum_add,cubeSum_mul]
  unfold cubeAvg
  grind

theorem tiltedWeight_nonnegative (d : Bits n) (bias : Rat)
    (hlo : -1 ≤ bias) (hhi : bias ≤ 1) (s : Bits n) : 0 ≤ tiltedWeight d bias s := by
  have hc := char_sign d s
  have hnum : 0 ≤ 1+bias*char d s := by rcases hc with hc | hc <;> rw [hc] <;> grind
  have hpow := Rat.pow_pos (n := n) (by decide +kernel : (0:Rat)<2)
  have hi : 0 ≤ ((2:Rat)^n)⁻¹ := by have h := Rat.inv_pos.mpr hpow; grind
  exact Rat.mul_nonneg hnum hi

theorem tilted_normalized (d : Bits n) (bias : Rat) (hd : ¬ IsZero d) :
    tiltedExpectation d bias (fun _ => 1) = 1 := by
  rw [tiltedExpectation_formula,cubeAvg_const]
  have he : (fun s => char d s*1) = char d := by funext s; simp
  rw [he,cubeAvg_char]
  simp [hd]
  decide +kernel

theorem tilted_product (d a b : Bits n) (bias : Rat) :
    tiltedExpectation d bias (fun s => char a s*char b s) =
      (if IsZero (xorBits a b) then 1 else 0) +
      bias*(if BitsEq (xorBits a b) d then 1 else 0) := by
  rw [tiltedExpectation_formula]
  have he : (fun s => char a s*char b s) = char (xorBits a b) := funext (char_mul a b)
  have ht : (fun s => char d s*(char a s*char b s)) = char (xorBits d (xorBits a b)) := by
    funext s; rw [char_mul,char_mul]
  rw [he,ht,cubeAvg_char,cubeAvg_char]
  have hi : IsZero (xorBits d (xorBits a b)) ↔ BitsEq (xorBits a b) d := by
    rw [xor_zero_iff]
    exact ⟨fun h i => (h i).symm, fun h i => (h i).symm⟩
  simp only [hi]

def tiltedLaw (d : Bits n) (bias : Rat) (hd : ¬ IsZero d)
    (hlo : -1 ≤ bias) (hhi : bias ≤ 1) : FiniteLaw (Bits n) where
  outcomes := functions [false,true] n
  weight := tiltedWeight d bias
  nonnegative := fun s _ => tiltedWeight_nonnegative d bias hlo hhi s
  normalized := by
    have h := tilted_normalized d bias hd
    simpa only [tiltedExpectation,Rat.mul_one] using h

end T7Gap

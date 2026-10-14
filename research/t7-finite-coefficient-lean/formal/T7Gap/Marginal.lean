import T7Gap.Activation
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

def SubsetBits (a b : Bits n) : Prop := ∀ i, a i = true → b i = true

def AgreeOn (support s t : Bits n) : Prop := ∀ i, support i = true → s i = t i
instance (support s t : Bits n) : Decidable (AgreeOn support s t) :=
  inferInstanceAs (Decidable (∀ i, support i = true → s i = t i))

def bitCount : {n : Nat} → Bits n → Nat
  | 0, _ => 0
  | n+1, a => (if a 0 then 1 else 0)+bitCount (fun i : Fin n => a i.succ)

theorem char_agree (support d s t : Bits n) (hd : SubsetBits d support)
    (ha : AgreeOn support s t) : char d s = char d t := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have hh : bitFactor (d 0) (s 0) = bitFactor (d 0) (t 0) := by
      by_cases h : d 0 = true
      · rw [ha 0 (hd 0 h)]
      · simp [bitFactor,h]
    simp only [char]
    rw [hh]
    rw [ih (fun i => support i.succ) (fun i => d i.succ) (fun i => s i.succ) (fun i => t i.succ)
      (fun i h => hd i.succ h) (fun i h => ha i.succ h)]

theorem agreement_cons (support : Bits (n+1)) (s : Bits n) (t : Bits (n+1)) (b : Bool) :
    AgreeOn support (Fin.cases b s) t ↔
      (support 0 = true → b = t 0) ∧ AgreeOn (fun i => support i.succ) s (fun i => t i.succ) :=
  Fin.forall_fin_succ

theorem cubeSum_agreement (n : Nat) (support t : Bits n) :
    cubeSum n (fun s => if AgreeOn support s t then 1 else 0) = 2^n*(1/2)^bitCount support := by
  induction n with
  | zero =>
    have h : ∀ s : Bits 0, AgreeOn support s t := fun _ i => Fin.elim0 i
    simp [cubeSum,functions,h,bitCount]; decide +kernel
  | succ n ih =>
    rw [cubeSum_succ]
    have hb : ∀ b : Bool, (fun s : Bits n => if AgreeOn support (Fin.cases b s) t then (1:Rat) else 0) =
        (fun s => if support 0 = true → b = t 0 then
          (if AgreeOn (fun i => support i.succ) s (fun i => t i.succ) then 1 else 0) else 0) := by
      intro b
      funext s
      simp only [agreement_cons]
      split <;> split <;> simp_all
    rw [hb false,hb true]
    by_cases hs : support 0 = true
    · cases ht : t 0 <;> simp [hs,ht,bitCount,cubeSum_const,ih,Rat.pow_succ] <;> grind only
    · simp [hs,bitCount,cubeSum_const,ih,Rat.pow_succ]
      grind only

theorem cubeAvg_agreement (support t : Bits n) :
    cubeAvg n (fun s => if AgreeOn support s t then 1 else 0) = (1/2)^bitCount support := by
  unfold cubeAvg
  rw [cubeSum_agreement]
  have hn : (2:Rat)^n ≠ 0 := by have h := Rat.pow_pos (n := n) (by decide +kernel : (0:Rat)<2); grind only
  have hh := Rat.mul_inv_cancel ((2:Rat)^n) hn
  grind only

/-- Exact marginal law on any selected support, not just moment matching. -/
theorem tilted_marginal (support d t : Bits n) (bias : Rat) (hd : SubsetBits d support) :
    tiltedExpectation d bias (fun s => if AgreeOn support s t then 1 else 0) =
      (1/2)^bitCount support*(1+bias*char d t) := by
  rw [tiltedExpectation_formula,cubeAvg_agreement]
  have he : (fun s => char d s*(if AgreeOn support s t then (1:Rat) else 0)) =
      (fun s => char d t*(if AgreeOn support s t then 1 else 0)) := by
    funext s
    by_cases h : AgreeOn support s t
    · simp only [h,ite_true,Rat.mul_one]
      exact char_agree support d s t hd h
    · simp [h]
  rw [he]
  have hm : cubeAvg n (fun s => char d t*(if AgreeOn support s t then (1:Rat) else 0)) =
      char d t*cubeAvg n (fun s => if AgreeOn support s t then 1 else 0) := by
    unfold cubeAvg
    rw [cubeSum_mul]
    grind only
  rw [hm,cubeAvg_agreement]
  grind only

theorem active_support_counts : ∀ c : Corner, bitCount (M c) = 7 ∧ bitCount (D c) = 6 := by decide +kernel

theorem activation_M_sign_marginal (c : Corner) (t : Bits 30) :
    activationExpectation c (fun o => if o.1 = true ∧ AgreeOn (M c) o.2 t then 1 else 0) =
      (1/2)*(1/2)^7*(1+(sigma c:Rat)/2*char (D c) t) := by
  rw [activationExpectation_split]
  simp only [true_and,Bool.false_eq_true,false_and,ite_false]
  rw [tilted_marginal _ _ _ _ (diff_subset_union c)]
  rw [(active_support_counts c).1]
  have hz : tiltedExpectation (D c) (-(sigma c:Rat)/2) (fun _ => 0) = 0 := by
    unfold tiltedExpectation
    simp
    change cubeSum 30 (fun _ => 0) = 0
    rw [cubeSum_const]; simp
  rw [hz]
  grind only

theorem activation_D_sign_marginal (c : Corner) (t : Bits 30) :
    activationExpectation c (fun o => if o.1 = false ∧ AgreeOn (D c) o.2 t then 1 else 0) =
      (1/2)*(1/2)^6*(1-(sigma c:Rat)/2*char (D c) t) := by
  rw [activationExpectation_split]
  simp only [Bool.false_eq_true,true_and,Bool.true_eq_false,false_and,ite_false]
  rw [tilted_marginal _ _ _ _ (fun _ h => h)]
  rw [(active_support_counts c).2]
  have hz : tiltedExpectation (D c) ((sigma c:Rat)/2) (fun _ => 0) = 0 := by
    unfold tiltedExpectation
    simp
    change cubeSum 30 (fun _ => 0) = 0
    rw [cubeSum_const]; simp
  rw [hz]
  grind only

end T7Gap

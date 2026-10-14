import T7Gap.TiltedLaw
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace T7Gap
open T7

/-- A source-faithful lift: signs outside the active set are independent auxiliary signs.
Their exact marginal elimination is proved separately. True selects M, false selects D. -/
abbrev ActivationOutcome := Bool × Bits 30

def activationSupport (c : Corner) (branch : Bool) : Mask := if branch then M c else D c
def branchBias (c : Corner) (branch : Bool) : Rat :=
  if branch then (sigma c : Rat)/2 else -(sigma c : Rat)/2

def activationOutcomes : List ActivationOutcome := [true,false].flatMap fun branch =>
  (functions [false,true] 30).map fun s => (branch,s)

def activationWeight (c : Corner) (o : ActivationOutcome) : Rat :=
  (1/2)*tiltedWeight (D c) (branchBias c o.1) o.2

def activationExpectation (c : Corner) (f : ActivationOutcome → Rat) : Rat :=
  (activationOutcomes.map fun o => activationWeight c o*f o).sum

theorem branch_bias_bounds : ∀ c : Corner, ∀ b : Bool,
    -1 ≤ branchBias c b ∧ branchBias c b ≤ 1 := by decide +kernel

theorem D_nonzero (c : Corner) : ¬ IsZero (D c) := by
  intro h
  obtain ⟨i,hi⟩ := diff_nonempty c
  have hz := h i
  rw [hi] at hz
  contradiction

theorem activationWeight_nonnegative (c : Corner) (o : ActivationOutcome) :
    0 ≤ activationWeight c o :=
  Rat.mul_nonneg (by decide +kernel) (tiltedWeight_nonnegative _ _ (branch_bias_bounds c o.1).1
    (branch_bias_bounds c o.1).2 o.2)

theorem activationExpectation_split (c : Corner) (f : ActivationOutcome → Rat) :
    activationExpectation c f =
      (1/2)*tiltedExpectation (D c) ((sigma c:Rat)/2) (fun s => f (true,s)) +
      (1/2)*tiltedExpectation (D c) (-(sigma c:Rat)/2) (fun s => f (false,s)) := by
  simp only [activationExpectation,activationOutcomes,List.flatMap_cons,List.flatMap_nil,
    List.append_nil,List.map_append,List.sum_append,List.map_map,Function.comp_def,
    activationWeight,branchBias,ite_true,ite_false]
  unfold tiltedExpectation
  rw [← rat_sum_mul, ← rat_sum_mul]
  congr 1 <;> congr 1 <;> apply List.map_congr_left <;> intro s _ <;> grind only

theorem activation_normalized (c : Corner) :
    (activationOutcomes.map (activationWeight c)).sum = 1 := by
  have h := activationExpectation_split c (fun _ => 1)
  rw [tilted_normalized _ _ (D_nonzero c),tilted_normalized _ _ (D_nonzero c)] at h
  have hh : (1/2:Rat)+1/2=1 := by decide +kernel
  simp only [Rat.mul_one] at h
  rw [hh] at h
  simpa only [activationExpectation,Rat.mul_one] using h

def activationLaw (c : Corner) : FiniteLaw ActivationOutcome where
  outcomes := activationOutcomes
  weight := activationWeight c
  nonnegative := fun o _ => activationWeight_nonnegative c o
  normalized := activation_normalized c

/-- This is the source random feature: an activation indicator times its sign character. -/
def phi (c : Corner) (a : Mask) (o : ActivationOutcome) : Rat :=
  if SubsetMask a (activationSupport c o.1) then char a o.2 else 0

def activationMoment (c : Corner) (a b : Mask) : Rat :=
  (activationLaw c).mean (fun o => phi c a o*phi c b o)

theorem union_subset_iff (a b s : Mask) :
    SubsetMask (unionMask a b) s ↔ SubsetMask a s ∧ SubsetMask b s := by
  constructor
  · intro h
    exact ⟨fun i ha => h i (by simp [unionMask,ha]),fun i hb => h i (by simp [unionMask,hb])⟩
  · rintro ⟨ha,hb⟩ i hi
    have hor : a i = true ∨ b i = true := by simpa [unionMask] using hi
    exact hor.elim (ha i) (hb i)

theorem tilted_phi_product (c : Corner) (a b : Mask) (branch : Bool) :
    tiltedExpectation (D c) (branchBias c branch) (fun s => phi c a (branch,s)*phi c b (branch,s)) =
      if SubsetMask (unionMask a b) (activationSupport c branch) then
        (if maskEq (diffMask a b) emptyMask then 1 else 0) +
        branchBias c branch*(if maskEq (diffMask a b) (D c) then 1 else 0)
      else 0 := by
  by_cases ha : SubsetMask a (activationSupport c branch)
  · by_cases hb : SubsetMask b (activationSupport c branch)
    · have hu := (union_subset_iff a b _).mpr ⟨ha,hb⟩
      simp only [phi,ha,hb,ite_true]
      rw [tilted_product]
      simp only [hu,ite_true]
      rfl
    · have hu : ¬ SubsetMask (unionMask a b) (activationSupport c branch) :=
        fun h => hb ((union_subset_iff a b _).mp h).2
      simp only [phi,ha,hb,hu,ite_true,ite_false,Rat.mul_zero]
      unfold tiltedExpectation
      simp
      change cubeSum 30 (fun _ => 0) = 0
      rw [cubeSum_const]; simp
  · have hu : ¬ SubsetMask (unionMask a b) (activationSupport c branch) :=
      fun h => ha ((union_subset_iff a b _).mp h).1
    simp only [phi,ha,hu,ite_false,Rat.zero_mul]
    unfold tiltedExpectation
    simp
    change cubeSum 30 (fun _ => 0) = 0
    rw [cubeSum_const]; simp

/-- The substantive stochastic-to-algebraic bridge: no moment identity is assumed. -/
theorem activation_moment_eq_formula (c : Corner) (a b : Mask) :
    activationMoment c a b = moment c a b := by
  change activationExpectation c (fun o => phi c a o*phi c b o) = _
  rw [activationExpectation_split]
  change (1/2)*tiltedExpectation (D c) (branchBias c true) _ +
    (1/2)*tiltedExpectation (D c) (branchBias c false) _ = _
  rw [tilted_phi_product,tilted_phi_product]
  by_cases hM : SubsetMask (unionMask a b) (M c) <;>
    by_cases hD : SubsetMask (unionMask a b) (D c) <;>
    by_cases h0 : maskEq (diffMask a b) emptyMask <;>
    by_cases hE : maskEq (diffMask a b) (D c) <;>
    simp [activationSupport,branchBias,moment,momentNumerator,hM,hD,h0,hE] <;> grind only

end T7Gap
